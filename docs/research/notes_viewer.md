# Viewer technology research (SPHEREx pixel-exact blink) - 2026-11-14
Sources saved in sources_viewer\ (and subfolders b,c,d1,d2,d3,e,j,o,ff2). Tag: [V] = VERIFIED from page, [NV] = NOT VERIFIED.
Failed fetches: js9.si.edu (connect timeout), openseadragon.github.io options page (404-ish), ipyaladin GitHub page (FAIL), cds-astro/mapproj (404). Did not read: ipyaladin, deck.gl, regl, WebGPU spec.

## KEY CONCEPT (own reasoning, not from a page)
"1-px shift = exactly 1 px" is only guaranteed if every frame is shown on its OWN native pixel grid (screen px = integer multiple of detector px) or all frames are resampled once, server-side, onto a common grid with nearest-neighbour. Frames with different roll cannot be both native-grid and sky-aligned. Any viewer that rotates a frame to sky/North-up resamples (even with NEAREST) and a 1px shift may become 0.8/1.2 px. Recommended: show each frame native (no rotation); compute overlay positions by SIP pixel<->sky in float.

## Aladin Lite v3 (cds-astro/aladin-lite)
1 FITS: yes, loads FITS images (fitsrs crate; shaders src/glsl/webgl2/fits/{f32,i16,i32,u8}.frag) [V: github.com/cds-astro/aladin-lite; changelog "Starting fits support"].
2 SIP: changelog 3.9.0-beta "[feat] Support of SIP astrometry keywords in FITS file" [V: raw.githubusercontent.com/cds-astro/aladin-lite/master/CHANGELOG.md]. fitsrs README: "Simple Imaging Polynomial (SIP) supported but not well tested" [V: raw.githubusercontent.com/cds-astro/fitsrs/master/README.md]; wcs-rs: "SIP convention support / SIP not tested" [V: github.com/cds-astro/wcs-rs]. Code: image uses fitsrs::wcs::{ImgXY,WCS} in src/core/src/renderable/image/mod.rs [V]. Accuracy of SIP in Aladin = NV (needs numeric test vs astropy).
3 Nearest: texture params in src/core/src/renderable/image/mod.rs TEX_PARAMS: TEXTURE_MAG_FILTER = NEAREST, TEXTURE_MIN_FILTER = NEAREST_MIPMAP_NEAREST [V: raw.githubusercontent.com/cds-astro/aladin-lite/master/src/core/src/renderable/image/mod.rs]. BUT changelog also lists "Zoom smoothing using hermite cubic interpolation" (that is zoom animation, not pixels) [V]. Image is drawn as sky-sphere mesh patches (subdivided, via corner unproj_lonlat) [V same file] => positions are mesh-approximated and image gets re-projected to the view: not a guaranteed native-grid mapping. NV whether mesh is exact for 6.15"/px at high zoom.
4 Blink/per-frame WCS: each FITS layer has its own WCS and is placed on sky [V]; a blink loop = toggling layer visibility/opacity from JS: API NV (not read). Aladin view is sky-aligned so rolled frames are resampled by GPU.
5 Overlay: catalogs/shapes/footprints, float RA/Dec [V changelog: shapes, catalogs overlays]. 
6 Last commit 2026-06-01; release v3.9.0-beta / v3.8.1 [V: GitHub API pages]. License LGPL-3.0-or-later (changed from GPLv3 in 3.8.0) [V]. fitsrs last commit 2026-11-09 [V].
7 Embed: single script aladin.js, A.init(...) [V README]; URL params: easy via JS, NV for built-in.

## IRSA Firefly (Caltech-IPAC/firefly) - also the engine behind IRSA's SPHEREx Data Explorer
1 FITS: yes, native, server (Java) + client (React). 
2 SIP: YES in source, both sides. Java: src/firefly/java/edu/caltech/ipac/visualize/plot/ImageHeader.java (MAX_SIP_LENGTH=10, a/ap/b/bp arrays, "GNOMONIC projection (ctype1 ending in -SIP)") and projection/GnomonicProjection.java (map_distortion, a_order/ap_order loops); JS: src/firefly/js/visualize/projection/GnomonicProjection.js (same SIP loops, MAX_SIP_LENGTH) [V: files in sources_viewer/d1,d2 + ImageHeader]. Max order 9 (len 10) [V]; SPHEREx uses order <=? NV.
3 Nearest: tiles drawn to 2D canvas with ctx.imageSmoothingEnabled = false in src/firefly/js/visualize/rawData/RawTileDrawer.js (writeToCanvas and draw) [V: sources_viewer/ff2]. Help: "if you want to zoom in close enough to see individual original pixels, your best choice is FITS"; 1:1 zoom icon [V: irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/visualization.html]. Exact zoom semantics at non-integer/rotated views NV.
4 Multi-image: lock images, align by WCS / pixel origin / image center / target, "North up" rotation [V same help page]. A dedicated blink/flipbook mode NOT found [NV]; multi-image viewer exists (MultiImageViewer.jsx in tree) [V tree]. WCS-lock aligns frames with different roll by client rotation/scaling = resampling [inferred].
5 Overlay: catalogs, markers, regions layers [V help: "add a layer"]; float positions NV.
6 Last commit 2026-11-12, release 2026.4.0, BSD-3-Clause, 10,062 commits [V]. Very active. Has WebGPU compute (wgsl) for color mapping [V tree].
7 Embed: Docker `ipac/firefly:latest` [V README]; JS API / firefly_client Python [V-ish: help mentions Python implementation of Firefly tools]; URL params and embedding effort NV; heavy (Java server + Tomcat).

## JS9 (ericmandel/js9) + forks
1 FITS: yes (cfitsio compiled to wasm via astroem) [V: tree astroem/include/fitsio.h].
2 SIP: WCS lib is Doug Mink's WCSTools libwcs (astroem/lib/libwcs.a; wcslib.h header history "Doug Mink - Update for WCSLIB 2.8.2") [V]; JS9.initwcs / wcsinit in js9.js [V]. SIP support in that libwcs: NV (no mention found in help/changelog).
3 Nearest: this.offscreen.context.imageSmoothingEnabled = false and context.imageSmoothingEnabled = false in js9.js (lines ~979, 1906, 6999) [V: raw js9.js]. Zoom is arbitrary float; rotation by arbitrary angle on displayed pixels [V help/user.html].
4 Blink: changelog "sync images: sync all images to facilitate blinking" [V help/changelog.html]; "align pan/zoom" ignores rotation, "wcs reproject" menu reprojects data [V help/user.html] (interpolation method NV).
5 Overlay: regions (JS9 regions) [V help list: help/regions.html]; catalogs plugin NV.
6 Last commit 2024-12-31 (GitHub API), MIT, release "Security/Archive release v3.9" [V]. Effectively low-activity.
7 Embed: JS9 page + optional helper; public API JS9.Load etc. (publicapi.html in tree) ; URL params NV.

## OpenSeadragon
1 No FITS (deep-zoom tiles; needs server-made PNG/tiles) [V README purpose; FITS NV].
2 No WCS at all [inferred]; WCS must be handled by own code/server.
3 Option imageSmoothingEnabled (default true) passed to each TiledImage, setImageSmoothingEnabled on drawer [V: raw src/openseadragon.js lines 232-236, 1441]. Also smoothTileEdgesMinZoom [V]. => set false for nearest (canvas drawer).
4 Blink: multi-image via addTiledImage/opacity; per-frame WCS not applicable.
5 Overlays: HTML/SVG overlays at float image coords [NV not read; known feature].
6 Last commit 2026-11-10, release v6.1.1, BSD-3-Clause [V].
7 Easy embed; URL via own JS.

## Custom WebGL2 / WebGPU / canvas2D / PixiJS / deck.gl
- Canvas2D: imageSmoothingEnabled=false documented [V MDN]. Simple, exact for integer scale if zoom is integer and canvas devicePixelRatio handled; CSS `image-rendering: pixelated` NV.
- WebGL2: gl.TEXTURE_MAG_FILTER NEAREST (default LINEAR) and MIN_FILTER NEAREST [V MDN texParameter]. Fragment shader with texelFetch(ivec2) gives exact no-filter reads; float32 R32F texture + stretch in shader (Aladin and Firefly both do GPU-side scaling [V]). Per-frame WCS: own uniform; SIP: implement in JS/shader (or precompute grid server-side). Maintenance: you own it. PixiJS/deck.gl/regl/three.js: wrappers around same texture filters; NV (not read).
- Server-side PNG: with GPU server, render each frame on common grid with nearest (astropy/reproject interp 'nearest-neighbor' NV not read) and send PNG; browser shows with imageSmoothingEnabled=false. Zero client WCS risk; pixel-exact by construction; limited interactivity.

## ipyaladin: page fetch FAILED; NV. Wrapper of Aladin Lite (so inherits its behaviour).

## RANKING
1. Custom thin client (Canvas2D or WebGL2 texelFetch) on top of server-prepared per-frame float/PNG data, with SIP evaluated by server (astropy) -> exact, controllable. Effort moderate (days).
2. Firefly (for features/IRSA-parity, SIP verified in source, imageSmoothingEnabled=false verified) - heavy deployment, blink not found.
3. Aladin Lite v3 (NEAREST mag filter verified; SIP new/"not well tested"; sky-mesh re-projection is the risk).
Also: OpenSeadragon as pan/zoom shell only if tiled PNGs; JS9 last (stale, SIP NV).

## CHEAP TESTS
A. Custom viewer / any: synthetic FITS 64x64 with single-pixel-wide checkerboard + one bright pixel at (10,10); second frame shifted by exactly 1 px. Screenshot at zooms 1, 3, 7, 16.5 (+ devicePixelRatio 1.25/2); measure bright-block width in screen px (must equal zoom) and offset between blink frames (must equal zoom px). Pass: all blocks equal width, no intermediate grey.
B. Firefly: load the same synthetic FITS (and a real SPHEREx cutout with TAN-SIP) in a local Docker Firefly; zoom to max; screenshot; check block uniformity at integer zooms and 1:1; then WCS-lock two frames with 1 px offset, confirm offset = zoom px. Compare Firefly's pixel->RA/Dec readout vs astropy SIP at 5 pixels (<0.01 px). Fail if alignment by WCS rotates canvas with smoothing/ragged blocks.
C. Aladin Lite: displayFITS the synthetic file at high zoom; screenshot; measure block widths (non-uniform widths => mesh/subdivision error). Then real TAN-SIP cutout: compare sky position of 5 stars/corner pixels against astropy (all_pix2world with SIP) — expect <0.1 px; also run with a pure TAN header (SIP stripped) to see how much SIP matters. Fail if >0.1 px residual or non-uniform blocks.
