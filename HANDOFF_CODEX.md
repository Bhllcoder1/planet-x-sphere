# Codex handoff — Aladin Lite CDN issue

Date: 2026-11-15

## Finding

The browser error is explained by the CDS incident notice dated 2026-11-09: Aladin image services at Strasbourg are degraded. This is an upstream outage, not a WISE coordinate bug. The old D-site page loaded the viewer JavaScript only from the affected CDS URL and asked the CDS registry for HiPS surveys.

## Change on `d/05-14-aladin-resilience`

- Vendor `aladin-lite@3.8.2` from npm into `d_site/vendor/`, retaining upstream license files.
- Remove the runtime script dependency on the CDS CDN.
- Replace CDS survey IDs with direct mirror URLs; WISE W1 now uses IRSA's AllWISE W1 HiPS at 3.4 µm.
- Show that survey tiles still require an online archive mirror and remain context-only.
- Updated survey metadata endpoints were reachable from this machine (HTTP 200); this does not verify an in-browser render.

## Verification and handoff

- `git diff --check` passed.
- Per Behlül's instruction, no tests or browser preview were run.
- D-site is owned by `@furkand69` (`.github/CODEOWNERS`). Keep the change in a D-owned PR and request their review before merge.
- Remaining limitation: without network access to the selected HiPS mirror, map tiles cannot load even though the Aladin code is local.

Sources: https://aladin.cds.unistra.fr/ ; https://irsa.ipac.caltech.edu/data/hips/CDS/AllWISE/W1/ ; https://github.com/cds-astro/aladin-lite
