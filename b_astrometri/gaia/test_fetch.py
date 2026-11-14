"""Offline checks. Run directly with python -I; no service calls."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import requests
from astropy.table import Table
from astropy.wcs import WCS

spec = importlib.util.spec_from_file_location("gaia_fetch", Path(__file__).with_name("fetch.py"))
fetch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)


def document(ids=(1,), status="OK", trailing="", missing=None, ra=269.452, dec=4.693):
    values = {"ra": ra, "dec": dec}
    table = Table({c: list(ids) if c == "source_id" else [values.get(c, 2016.0)] * len(ids)
                   for c in fetch.COLUMNS if c != missing})
    buffer = io.BytesIO()
    table.write(buffer, format="votable")
    xml = buffer.getvalue().decode()
    xml = xml.replace('<RESOURCE type="results">', '<RESOURCE type="results">'
                      f'<INFO name="QUERY_STATUS" value="{status}"/>')
    if trailing:
        xml = xml.replace('</RESOURCE>', f'<INFO name="QUERY_STATUS" value="{trailing}"/></RESOURCE>')
    return xml.encode()


class Response:
    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        pass


class ErrorResponse:
    """Simulates a non-2xx HTTP response that raises HTTPError on raise_for_status."""
    def __init__(self, status_code):
        self.status_code = status_code
        self.content = b""

    def raise_for_status(self):
        err = requests.HTTPError(f"{self.status_code}")
        err.response = self
        raise err


def http_error(status_code):
    """Return an HTTPError with the given status code, for use in Session responses."""
    err = requests.HTTPError(f"{status_code}")
    err.response = type("FakeResp", (), {"status_code": status_code})()
    return err


class Session:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def post(self, endpoint, **kwargs):
        self.calls.append((endpoint, kwargs))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return Response(response)


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        wcs = WCS(naxis=2)
        wcs.wcs.crpix = [1024, 1024]
        wcs.wcs.cdelt = [-6.15 / 3600, 6.15 / 3600]
        wcs.wcs.crval = [269.452, 4.693]
        wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
        self.header = wcs.to_header()

    def test_status_and_columns(self):
        self.assertEqual(len(fetch.parse_catalogue(document())), 1)
        for content in (document(status="ERROR"), document(trailing="OVERFLOW"),
                        document(missing="ruwe"), b"not XML"):
            with self.subTest(content=content[-100:]):
                with self.assertRaises((ValueError, fetch.ET.ParseError)):
                    fetch.parse_catalogue(content)

    def test_empty_catalogue_valid(self):
        output = self.root / "empty.fits"
        result = fetch.fetch_frame(self.header, 1016, 1016, self.root / "cache", output,
            session=Session([document(())] * 4), attempts=1)
        self.assertEqual(result["rows"], 0)
        self.assertEqual(Table.read(output).colnames, list(fetch.COLUMNS))

    def test_esa_field_id_can_differ_from_column_name(self):
        content = document((123,)).replace(b'ID="source_id"', b'ID="SOURCE_ID"')
        self.assertIn(b'ID="SOURCE_ID"', content)
        table = fetch.parse_catalogue(content)
        self.assertEqual(table.colnames, list(fetch.COLUMNS))
        self.assertEqual(int(table["source_id"][0]), 123)

    def test_four_tiles_dedup_and_provenance(self):
        output = self.root / "merged.fits"
        session = Session([document((1, 2)), document((2, 3)), document((4,)), document((5,))])
        result = fetch.fetch_frame(self.header, 1016, 1016, self.root / "cache", output,
                                  session=session, attempts=1)
        self.assertEqual(len(result["tiles"]), 4)
        self.assertEqual(result["rows"], 5)
        self.assertEqual(Table.read(output).meta["NTILES"], 4)
        self.assertEqual(len(session.calls), 4)
        self.assertEqual(session.calls[0][1]["timeout"], (10, 45))

    def test_small_tiles_cover_same_window_and_all_are_required(self):
        tiles = list(fetch.frame_tiles(self.header, 0, 0, tile_half=128))
        centers = {(t["qx"], t["qy"]) for t in tiles}
        expected = {(x, y) for x in (128, 384, 640, 896) for y in (128, 384, 640, 896)}
        self.assertEqual(centers, expected)
        self.assertEqual(len(tiles), 16)
        self.assertEqual(min(x - 128 for x, y in centers), 0)
        self.assertEqual(max(x + 128 for x, y in centers), 1024)
        self.assertEqual(min(y - 128 for x, y in centers), 0)
        self.assertEqual(max(y + 128 for x, y in centers), 1024)
        self.assertAlmostEqual(tiles[0]["radius"], 128 * 1.4143 * (6.2 / 3600) + 0.01)
        result = fetch.fetch_frame(self.header, 0, 0, self.root / "cache",
            self.root / "small.fits", tile_half=128, attempts=1,
            session=Session([document((i,)) for i in range(16)]))
        self.assertEqual(len(result["tiles"]), 16)
        self.assertEqual(result["rows"], 16)
        with self.assertRaises(ValueError):
            list(fetch.frame_tiles(self.header, 0, 0, tile_half=64))

    def test_incomplete_keeps_previous_output(self):
        output = self.root / "previous.fits"
        output.write_bytes(b"previous successful catalogue")
        session = Session([document(), document(), document(trailing="OVERFLOW")])
        with self.assertRaisesRegex(RuntimeError, "output unchanged"):
            fetch.fetch_frame(self.header, 0, 0, self.root / "cache", output,
                              providers=("mast",), session=session, attempts=1)
        self.assertEqual(output.read_bytes(), b"previous successful catalogue")

    def test_cache_identity_integrity_and_provider(self):
        cache = self.root / "cache"
        first = Session([document((8,))])
        _, record = fetch.fetch_tile("mast", "query-A", cache, session=first)
        self.assertFalse(record["cache"])
        _, record = fetch.fetch_tile("mast", "query-A", cache, session=Session([]))
        self.assertTrue(record["cache"])
        (cache / f"{record['key']}.xml").write_bytes(document((99,)))
        replacement = Session([document((9,))])
        table, record = fetch.fetch_tile("mast", "query-A", cache, session=replacement)
        self.assertFalse(record["cache"])
        self.assertEqual(int(table["source_id"][0]), 9)
        other = Session([document((10,)), document((11,))])
        fetch.fetch_tile("mast", "query-B", cache, session=other)
        fetch.fetch_tile("esa", "query-A", cache, session=other)
        self.assertEqual(len(other.calls), 2)
        metadata = json.loads(next(cache.glob("*.json")).read_text())
        self.assertIn("endpoint", metadata["identity"])

    def test_retry_and_fallback(self):
        session = Session([requests.Timeout("timeout"), document()])
        with patch.object(fetch.time, "sleep") as sleep:
            fetch.fetch_tile("esa", "q", self.root / "cache", session=session, attempts=2)
            sleep.assert_called_once_with(1)
        session = Session([document(trailing="OVERFLOW"), document()] * 4)
        result = fetch.fetch_frame(self.header, 0, 0, self.root / "other-cache",
            self.root / "fallback.fits", providers=("mast", "esa"), attempts=1, session=session)
        self.assertTrue(all(r["provider"] == "esa" for r in result["tiles"]))
        self.assertTrue(all(len(r["failures"]) == 1 for r in result["tiles"]))

    def test_rejects_nan_coordinates_without_retry(self):
        content = document(ra=float("nan"))
        session = Session([content])
        with self.assertRaisesRegex(RuntimeError, "coordinates"):
            fetch.fetch_tile("esa", "nan", self.root / "cache", session=session)
        self.assertEqual(len(session.calls), 1)

    def test_rejects_out_of_bounds_coordinates(self):
        for ra, dec in ((-0.1, 0), (360, 0), (0, -90.1), (0, 90.1)):
            with self.subTest(ra=ra, dec=dec), self.assertRaisesRegex(ValueError, "outside"):
                fetch.parse_catalogue(document(ra=ra, dec=dec))
        fetch.parse_catalogue(document(ra=0, dec=-90))
        fetch.parse_catalogue(document(ra=359.9, dec=90))

    def test_permanent_http_error_not_retried(self):
        """4xx errors (except 429) must raise immediately without retry."""
        for status in (400, 403, 404, 422):
            session = Session([http_error(status), document()])
            with self.subTest(status=status), \
                 self.assertRaisesRegex(RuntimeError, f"permanent HTTP {status}"):
                fetch.fetch_tile("esa", "q", self.root / "cache", session=session, attempts=2)
            # Only one call was made — the permanent error stopped retry
            self.assertEqual(len(session.calls), 1,
                             f"Expected exactly 1 call for HTTP {status}, got {len(session.calls)}")

    def test_429_is_retried_like_transient_error(self):
        """429 Too Many Requests is transient and must be retried."""
        session = Session([http_error(429), document()])
        with patch.object(fetch.time, "sleep"):
            fetch.fetch_tile("esa", "q", self.root / "cache", session=session, attempts=2)
        self.assertEqual(len(session.calls), 2, "429 should trigger a retry")

    def test_external_stream_rejected_before_astropy(self):
        for href in ("file:///private/data", "https://example.invalid/data"):
            content = document().replace(b"</TABLE>",
                f'<STREAM href="{href}"/></TABLE>'.encode())
            with patch.object(fetch, "parse_single_table") as parse:
                with self.assertRaisesRegex(ValueError, "External VOTable"):
                    fetch.parse_catalogue(content)
                parse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
