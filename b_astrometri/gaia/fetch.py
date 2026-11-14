"""Task 01-03: complete, validated Gaia DR3 tiles; no partial catalogue output."""
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import tempfile
import time
import xml.etree.ElementTree as ET

import requests
from astropy.io import fits
from astropy.io.votable import parse_single_table
from astropy.table import Table, unique, vstack
from astropy.wcs import WCS

COLUMNS = (
    "source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec",
    "phot_g_mean_mag", "ruwe", "ref_epoch", "astrometric_params_solved",
)
PROVIDERS = {
    "mast": ("https://mast.stsci.edu/vo-tap/api/v0.1/gaiadr3/sync", "dbo.gaia_source"),
    "esa": ("https://gea.esac.esa.int/tap-server/tap/sync", "gaiadr3.gaia_source"),
}


def parse_catalogue(content):
    # QUERY_STATUS can follow TABLE; parsing only the table misses truncation.
    root = ET.fromstring(content)
    if any(e.tag.rsplit("}", 1)[-1].upper() == "STREAM"
           and any(k.rsplit("}", 1)[-1].lower() == "href" for k in e.attrib)
           for e in root.iter()):
        raise ValueError("External VOTable STREAM references are forbidden")
    statuses = [e.attrib.get("value", "").upper() for e in root.iter()
                if e.tag.rsplit("}", 1)[-1] == "INFO"
                and e.attrib.get("name", "").upper() == "QUERY_STATUS"]
    if not statuses or any(s != "OK" for s in statuses):
        raise ValueError(f"TAP query incomplete or failed: {statuses}")
    # ESA gives source_id the XML ID SOURCE_ID; ADQL column names live in name.
    table = parse_single_table(io.BytesIO(content)).to_table(use_names_over_ids=True)
    missing = set(COLUMNS) - set(table.colnames)
    if missing:
        raise ValueError(f"Missing Gaia columns: {sorted(missing)}")
    if any(getattr(table[c], "mask", False).any() for c in ("source_id", "ra", "dec")
           if hasattr(getattr(table[c], "mask", False), "any")):
        raise ValueError("Missing source identity or coordinates")
    if any(not math.isfinite(float(value)) for name in ("ra", "dec") for value in table[name]):
        raise ValueError("Non-finite source coordinates")
    if any(not 0 <= float(value) < 360 for value in table["ra"]):
        raise ValueError("Source RA outside [0,360)")
    if any(not -90 <= float(value) <= 90 for value in table["dec"]):
        raise ValueError("Source Dec outside [-90,90]")
    return table[list(COLUMNS)]


def atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".gaia-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def query_for(provider, ra, dec, radius):
    return (f"SELECT {', '.join(COLUMNS)} FROM {PROVIDERS[provider][1]} "
            f"WHERE 1=CONTAINS(POINT('ICRS',ra,dec),"
            f"CIRCLE('ICRS',{ra:.8f},{dec:.8f},{radius:.8f})) "
            "AND phot_g_mean_mag<18")


def fetch_tile(provider, query, cache, *, attempts=2, timeout=45, session=None):
    if attempts < 1 or timeout <= 0:
        raise ValueError("attempts and timeout must be positive")
    endpoint = PROVIDERS[provider][0]
    identity = {"version": 1, "provider": provider, "endpoint": endpoint, "query": query}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    cache = Path(cache)
    data_path, meta_path = cache / f"{key}.xml", cache / f"{key}.json"
    try:
        content = data_path.read_bytes()
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        if (metadata.get("identity") == identity
                and metadata.get("sha256") == hashlib.sha256(content).hexdigest()):
            return parse_catalogue(content), {"provider": provider, "cache": True, "key": key}
    except (OSError, ValueError, ET.ParseError):
        pass  # Invalid/legacy cache is never evidence of a completed query.
    requester = session or requests
    started = time.monotonic()
    for attempt in range(attempts):
        try:
            response = requester.post(endpoint, data={"REQUEST": "doQuery", "LANG": "ADQL",
                "FORMAT": "votable", "MAXREC": "2000000", "QUERY": query},
                timeout=(min(10, timeout), timeout))
            response.raise_for_status()
            content = response.content
            table = parse_catalogue(content)
            atomic_write(data_path, content)
            atomic_write(meta_path, json.dumps({"identity": identity,
                "sha256": hashlib.sha256(content).hexdigest(),
                "fetched_at_unix": time.time(), "rows": len(table)}).encode())
            return table, {"provider": provider, "cache": False, "key": key,
                           "seconds": round(time.monotonic() - started, 3)}
        except (ValueError, ET.ParseError) as error:
            raise RuntimeError(f"{provider} invalid catalogue: {error}") from error
        except requests.HTTPError as error:
            # 4xx errors are permanent (server understood the request but refused/can't serve it).
            # 429 Too Many Requests is transient and may be retried like any other network error.
            # Note: timeout=(connect, read) limits time between bytes, not total transfer time;
            # a server streaming data very slowly can still exceed the intended budget.
            status = error.response.status_code if error.response is not None else None
            if status is not None and 400 <= status < 500 and status != 429:
                raise RuntimeError(
                    f"{provider} permanent HTTP {status} (not retried): {error}"
                ) from error
            if attempt + 1 == attempts:
                raise RuntimeError(f"{provider} failed after {attempts} attempts: {error}") from error
            time.sleep(min(2 ** attempt, 8))
        except requests.RequestException as error:
            if attempt + 1 == attempts:
                raise RuntimeError(f"{provider} failed after {attempts} attempts: {error}") from error
            time.sleep(min(2 ** attempt, 8))


def frame_tiles(header, x0, y0, tile_half=256):
    if tile_half not in (128, 256):
        raise ValueError("Tile half-size must be 128 or 256 pixels")
    if not all(math.isfinite(v) for v in (x0, y0)):
        raise ValueError("Window origin must be finite")
    wcs = WCS(header)
    # Smaller cones cover the same 1024-square window without recursive queries.
    radius = tile_half * 1.4143 * (6.2 / 3600) + 0.01
    for qx in range(tile_half, 1024, 2 * tile_half):
        for qy in range(tile_half, 1024, 2 * tile_half):
            ra, dec = map(float, wcs.all_pix2world(x0 + qx, y0 + qy, 0))
            if not all(math.isfinite(v) for v in (ra, dec)):
                raise ValueError("WCS returned non-finite sky coordinates")
            yield {"qx": qx, "qy": qy, "ra": ra, "dec": dec, "radius": radius}


def fetch_frame(header, x0, y0, cache, output, *, providers=("esa", "mast"), attempts=2,
                timeout=45, session=None, tile_half=256):
    if not providers or any(p not in PROVIDERS for p in providers):
        raise ValueError("Choose mast and/or esa providers")
    tables, records = [], []
    for tile in frame_tiles(header, x0, y0, tile_half):
        failures = []
        for provider in providers:
            try:
                table, record = fetch_tile(provider, query_for(provider, tile["ra"],
                    tile["dec"], tile["radius"]), cache, attempts=attempts,
                    timeout=timeout, session=session)
                tables.append(table)
                records.append({**tile, **record, "rows": len(table), "failures": failures})
                break
            except RuntimeError as error:
                failures.append(str(error))
        else:
            raise RuntimeError(f"Tile {tile['qx']},{tile['qy']} missing; output unchanged: {failures}")
    combined = vstack(tables, metadata_conflicts="silent")
    if len(combined):
        combined = unique(combined, keys="source_id")
    combined.meta = {"GAIAREL": "DR3", "NTILES": len(records),
                     "PROVIDRS": ",".join(sorted({r['provider'] for r in records}))}
    # Serialize before replacing: an interrupted/failed run preserves old output.
    buffer = io.BytesIO()
    combined.write(buffer, format="fits")
    atomic_write(output, buffer.getvalue())
    return {"complete": True, "tile_half": tile_half, "tiles": records,
            "rows": len(combined), "output": str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--header", type=Path, help="FITS header text file")
    source.add_argument("--stage0-data", type=Path, help="External stage0/data/C directory")
    parser.add_argument("--frame", choices=list("ABC"), default="B")
    parser.add_argument("--x0", type=int)
    parser.add_argument("--y0", type=int)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--providers", nargs="+", choices=list(PROVIDERS), default=["esa", "mast"],
                        help="Ordered providers; ESA first because current MAST probes overflow")
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--tile-half", type=int, choices=(128, 256), default=256,
                        help="Half tile width in pixels; 128 uses sixteen smaller cones")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    if any(p.resolve().is_relative_to(repo) for p in (args.cache, args.output)):
        parser.error("Cache and output must be outside the source repository")
    if args.stage0_data:
        import numpy as np
        with np.load(args.stage0_data / f"frame_{args.frame}.npz", allow_pickle=False) as frame:
            x0, y0 = int(frame["x0"]), int(frame["y0"])
        header_path = args.stage0_data / f"hdr_{args.frame}.txt"
    else:
        if args.x0 is None or args.y0 is None:
            parser.error("--header requires --x0 and --y0")
        x0, y0, header_path = args.x0, args.y0, args.header
    header = fits.Header.fromstring(header_path.read_text(encoding="utf-8"), sep="\n")
    result = fetch_frame(header, x0, y0, args.cache, args.output,
        providers=args.providers,
        attempts=args.attempts, timeout=args.timeout, tile_half=args.tile_half)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
