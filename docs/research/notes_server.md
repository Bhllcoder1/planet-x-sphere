# Server/infra research notes (2026-11-14)
Tags: [V:file] = verified from scraped page text (file in sources/ or sources_server/); [NV] = not verified.

## 1. IRSA cloud access
- Bucket `nasa-irsa-spherex`, region us-east-1. [V: sources_server/irsa-ipac-caltech-edu-cloud-access.md, https://irsa.ipac.caltech.edu/cloud_access/]
- Hosted via AWS Open Data Sponsorship; "downloaded or accessed directly without credentials or egress charges"; anonymous (`--no-sign-request` / `anonymous=True`). [V: same page]
- Browse: https://nasa-irsa-spherex.s3.us-east-1.amazonaws.com/index.html ; products found by prepending the S3 prefix to the "Browsable Directories" names. Calibration files (ePSF, solid-angle pixel maps) live there, e.g. qr3/epsf/cal-epsf-v1-2026-191/1/epsf_D1_...fits. [V: sources/irsa-tut-spherex-psf.md l.393-406]
- SIA/TAP results carry a `cloud_access` JSON column (aws.bucket_name + aws.key); tutorial opens `fits.open(f's3://{bucket}/{key}', fsspec_kwargs={"anon": True})` and reads "IMAGE" and "FLAGS" by name. [V: sources/irsa-tut-spherex-source-discovery.md l.325-345]
- HDU layout: IMAGE ImageHDU 2040x2040 float32, FLAGS CompImageHDU int32, VARIANCE and ZODI ImageHDU float32. [V: sources/irsa-tut-spherex-intro.md l.282-285] Uncompressed float32 HDUs are contiguous bytes (about 16.6 MB each by arithmetic), so partial reads are structurally possible.
- Spectral Image MEFs "several hundred megabytes" (full file). [V: sources/irsa-spherex-docs-cutout-tool.md l.15]
- Byte-range reads of one HDU via astropy+fsspec: astropy lazily seeks through fsspec so only needed HDU bytes should be fetched [NV: not confirmed on a page; test empirically by logging S3 GET ranges]. Reading a sub-window of an uncompressed HDU with `hdul["IMAGE"].section[y0:y1, x0:x1]` should fetch only those row-spans [NV]. Important: a cutout needs the WCS header, so first HDU headers (small) + a pixel window; FLAGS is tile-compressed (also tile-addressable, [NV]). Note IRSA's own cutout service also handles the per-HDU WCS differences (spectral WCS, ePSF cube); replicating that yourself is work [V: cutout-tool.md l.15].
- Same-region VM: bucket in us-east-1, so renting an AWS EC2 instance in us-east-1 gives in-region reads; egress to the internet is waived for the bucket by the sponsorship statement, but intra-region EC2<->S3 cost is AWS's own pricing [NV]. Speed gain is likely but [NV: not measured]. A non-AWS VPS reads over the public internet (still no egress charge to us per the page, but latency/throughput limited by provider).

## 1b. Cutout tool, limits, policy
- On-prem cutouts: append `?center=RA,DEC&size=0.1` to an `/ibe/data/spherex/...fits` URL; cutouts preserve MEF structure. [V: sources/irsa-spherex-docs-cutout-tool.md l.32-34]
- No documented numeric rate limit or per-user quota found on cutout-tool, cutouts tutorial, SIA, TAP, IBE cutouts pages. [V by absence: grep of those files]
- Documented limits: TAP sync times out at 5 min, async 3 days [V: sources_server/irsa-ipac-caltech-edu-docs-program-interface-tap-html.md l.125-131]; SIA jobs >5 min cancelled, use TAP for larger [V: ...-ibe-sia-html.md l.264-268].
- Tutorial guidance: parallel cutouts with max_workers 7-12 on an 8-core machine, "depends ... on the number of parallel calls that can be digested by the IRSA server"; serial run took 2.26 min for the example; some cutouts fail (HTTPError/timeout/IncompleteRead) so retry logic needed. [V: sources/irsa-tut-spherex-cutouts.md l.254-275, 343-348]
- IBE cutout page says per-detector extensions are not supported by the generic IBE cutout service (SPHEREx has its own). [V: sources_server/irsa-ipac-caltech-edu-ibe-cutouts-html.md l.56]
- https://irsa.ipac.caltech.edu/docs/program_interface/ returned 403 [FAIL page]. No formal "usage policy" page found/read; [NV] for any hidden throttling.
- Recommendation: use S3 for pixel data (not subject to IBE server load), TAP/SIA only for the small metadata query, and cache.

## 2. GPU: where it helps (engineering judgment, [NV] as web claims; no benchmark done)
- IO/CPU-bound, GPU useless: HTTP/S3 downloads, FITS parsing, astropy WCS transforms, TAP queries, FastAPI, JSON/PNG encoding for a single cutout. Per-request data is ~4 MB, small.
- Marginal: reprojection of a handful of 100x100-ish cutouts (CPU `reproject` interp is ms-seconds); photutils aperture photometry on small stamps; per-source PSF fitting for a few sources. Transfer overhead dominates.
- Possible GPU wins only at scale: batched PSF fitting for thousands of sources, whole-detector (2040^2 x many exposures) stacking/convolution (CuPy/cuCIM), KBMOD-style moving-object stacking (KBMOD is GPU-based by design [NV: not read]), ML inference (PyTorch).
- Rendering: client-side WebGL/WebGPU in the user's browser does the display for free; server headless GPU rendering is rarely needed. Decision: for a first public version with per-request cutouts, a GPU is NOT worth paying for; start CPU-only (4-8 vCPU), profile, add GPU only if a measured step (batched fitting/stacking) exceeds budget.

## 3. Backend stack (design suggestion, [NV] by nature)
- FastAPI + uvicorn; heavy work in a task queue (arq or RQ with Redis; Celery if you need more features); job status endpoint + polling/SSE.
- Cache: content-addressed key = (obs file key, HDU, window, version); store .npy/.fits or float16/uint8 tiles on disk first, move to object storage (S3/MinIO) later; set max-age + immutable headers (releases are versioned in path).
- Binary frames: serve raw little-endian float32/uint16 arrays with Content-Type application/octet-stream (+ gzip/zstd at Caddy) and metadata in a header/JSON; browser uses typed arrays + WebGL.
- Caddy for automatic HTTPS, reverse proxy to uvicorn, `encode zstd gzip`, static file serving of cache dir.
- Politeness: global semaphore of ~4-6 concurrent IRSA requests (tutorial ceiling 7-12 for batch use [V]), per-user job limit, dedupe in-flight identical requests, exponential backoff retries, identify via User-Agent contact string, contact IRSA helpdesk before public launch [NV].

## 4. Provider pricing (pages scraped 2026-11-14)
- Hetzner Cloud: "Cost-Optimized from EUR 5.99/mo excl. VAT"; "Regular Performance from EUR 5.49/mo excl. VAT" [VERIFIED from page: https://www.hetzner.com/cloud/, 2026-11-14] (CPU baseline; entry plans are tiny; exact vCPU/RAM per plan not read; third-party search results claimed 2026 price hikes and US regions pricier, [NV]).
- Hetzner dedicated GPU GEX45: EUR 214.00/mo or EUR 0.3429/h excl. VAT + EUR 209 setup; 14 cores i5-13500, 64 GB RAM, RTX PRO 4000 Blackwell SFF 24 GB. GEX63: EUR 999.00/mo, RTX PRO 6000 Blackwell Max-Q 96 GB [VERIFIED from page: https://www.hetzner.com/dedicated-rootserver/matrix-gpu/, 2026-11-14]. Located in EU, so not same region as us-east-1 [NV].
- Lambda: A10 24 GB $1.29/GPU/h; A6000 48 GB $1.09/GPU/h (dedicated listed); A100 40GB $1.99; H100 PCIe $3.79 [VERIFIED from page: https://lambda.ai/pricing, 2026-11-14] (instance table; per-hour, other-section rows exist).
- RunPod: RTX 4090 24 GB $0.89/hr; L40S 48 GB $1.09/hr; L40 $0.82/hr [VERIFIED from page: https://www.runpod.io/pricing, 2026-11-14] (a GPU pod; community vs secure tier not distinguished by me).
- Vast.ai: pricing page is live-marketplace, no static price captured [NOT VERIFIED].
- AWS g4dn/g4: official page https://aws.amazon.com/ec2/instance-types/g4/ scraped, shows no prices [NOT VERIFIED]. Third-party sites (search snippets only) listed g4dn.xlarge ~$0.526/h on-demand us-east-1 [NOT VERIFIED]. AWS matters because only it is guaranteed same-region (us-east-1) as the bucket.
- DigitalOcean, Vultr pages scraped but prices not extracted [NOT VERIFIED].
- Monthly math (derived from verified numbers): 4090 pod at $0.89/h x 730 h = about $650/mo if always on; GEX45 EUR 214/mo flat; CPU Hetzner EUR 5.49-5.99 entry. Hourly GPU only when jobs run (serverless/on-demand) is far cheaper for a low-traffic site.

## Failed pages
- https://irsa.ipac.caltech.edu/docs/program_interface/ (403).
