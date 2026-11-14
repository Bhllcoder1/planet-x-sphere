"""S0.4: parent-pixel rule x_orig = 1 + x_cut - CRPIX1A; two cutouts + S3 window of the same frame (uses s3win.npz from b8_explore.py)."""
import json, warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from photutils.centroids import centroid_2dg, centroid_com
warnings.filterwarnings("ignore")
B = r"stage0\data\B"
z = np.load(B + r"\s3win.npz"); wx0, wy0 = int(z["wx0"]), int(z["wy0"])
s3 = {n: z[n] for n in ("IMAGE", "FLAGS", "VARIANCE", "ZODI")}
fullhdr = fits.Header.fromtextfile(B + r"\full_image_header.txt") if hasattr(fits.Header, "fromtextfile") else None
fullhdr = fits.Header.fromstring(open(B + r"\full_image_header.txt").read(), sep="\n")
wfull = WCS(fullhdr)
print("S3 window origin (0-based parent x,y):", wx0, wy0)
print("full-frame IMAGE hdr: CRPIX1A/2A", fullhdr.get("CRPIX1A"), fullhdr.get("CRPIX2A"), "CRVAL1A/2A", fullhdr.get("CRVAL1A"), fullhdr.get("CRVAL2A"), "WCSNAMEA", fullhdr.get("WCSNAMEA"))
PRED = (1156.5, 1743.4)  # predicted Barnard parent pixel (0-based)

def centroids(img, ox, oy, label):
    """img array, (ox,oy)= parent 0-based coords of img[0,0]. Peak = max finite pixel within 8 px of PRED (core is NaN: saturated)."""
    d = np.array(img, float)
    yy, xx = np.mgrid[0:d.shape[0], 0:d.shape[1]]
    near = (np.hypot(xx + ox - PRED[0], yy + oy - PRED[1]) < 8) & np.isfinite(d)
    dd = np.where(near, d, -np.inf)
    yp, xp = np.unravel_index(np.argmax(dd), d.shape)
    h = 5
    sub = d[yp - h:yp + h + 1, xp - h:xp + h + 1]
    mask = ~np.isfinite(sub)
    bg = 0.30347755551338196   # FIXED background (median of the 100x100 S3 window) so only coordinates differ; per-array medians shifted COM by 1e-4..1e-2 px in the first run
    sub0 = np.where(mask, 0, sub - bg)
    cx, cy = centroid_com(sub0, mask=mask)
    gx, gy = centroid_2dg(sub0, mask=mask)
    out = dict(peakpix=(xp + ox, yp + oy), com=(cx + xp - h + ox, cy + yp - h + oy), g2d=(gx + xp - h + ox, gy + yp - h + oy))
    print(f"{label}: peak pixel (parent) {out['peakpix']} value {d[yp, xp]:.1f}; NaN in 11x11 stamp: {mask.sum()};  COM {out['com']}  2DG {out['g2d']}")
    return out

res = {"S3": centroids(s3["IMAGE"], wx0, wy0, "S3 100x100")}
for tag in ("A", "B"):
    h = fits.open(B + rf"\cut\f0_{tag}.fits")
    hh = h["IMAGE"].header
    print("cutout", tag, [x.name for x in h])
    print("  IMAGE NAXIS", hh["NAXIS1"], hh["NAXIS2"], "CRPIX1A/2A", hh["CRPIX1A"], hh["CRPIX2A"], "CRVAL1A/2A", hh["CRVAL1A"], hh["CRVAL2A"], "CRPIX1/2", hh["CRPIX1"], hh["CRPIX2"], "WCSNAMEA", hh.get("WCSNAMEA"))
    for n in ("FLAGS", "VARIANCE", "ZODI"):
        print("  ", n, "CRPIX1A/2A", h[n].header.get("CRPIX1A"), h[n].header.get("CRPIX2A"))
    print("  EPSF/WCS-WAVE CRPIX1A present:", "CRPIX1A" in h["EPSF"].header, "CRPIX1A" in h["WCS-WAVE"].header)
    off = (1 - hh["CRPIX1A"], 1 - hh["CRPIX2A"])   # x_orig = 1 + x_cut - CRPIX1A
    res[tag] = centroids(h["IMAGE"].data, off[0], off[1], f"cutout {tag} (rule offset {off})")
    wc = WCS(hh)
    ys, xs = np.mgrid[0:hh["NAXIS2"]:4, 0:hh["NAXIS1"]:4]
    sky = wc.all_pix2world(xs.ravel(), ys.ravel(), 0)
    xf, yf = wfull.all_world2pix(sky[0], sky[1], 0)
    dx = xf - (xs.ravel() + off[0]); dy = yf - (ys.ravel() + off[1])
    print(f"  independent celestial-WCS check (cutout SIP WCS -> sky -> full-frame SIP WCS vs rule): max|dx|={np.abs(dx).max():.2e} max|dy|={np.abs(dy).max():.2e} px; mean dx,dy = {dx.mean():+.2e},{dy.mean():+.2e}")
    ox, oy = int(round(off[0])), int(round(off[1])); ny, nx = hh["NAXIS2"], hh["NAXIS1"]
    for n in ("IMAGE", "VARIANCE", "ZODI", "FLAGS"):
        a = np.array(h[n].data)
        sub = s3[n][oy - wy0:oy - wy0 + ny, ox - wx0:ox - wx0 + nx]
        ok = sub.shape == a.shape
        eq = ok and np.array_equal(a, sub, equal_nan=True)
        fin = np.isfinite(a.astype(float)) & np.isfinite(sub.astype(float)) if ok else None
        mx = float(np.max(np.abs(a.astype(float)[fin] - sub.astype(float)[fin]))) if ok else None
        print(f"  {n}: cutout {a.shape} vs S3-overlap {sub.shape}: array_equal(equal_nan)={eq}, max|diff| on finite={mx}, dtype {a.dtype}/{sub.dtype}, NaN cutout/S3 {int(np.isnan(a.astype(float)).sum())}/{int(np.isnan(sub.astype(float)).sum())}")
# A vs B overlap
ha, hb = fits.open(B + r"\cut\f0_A.fits"), fits.open(B + r"\cut\f0_B.fits")
oa = (1 - ha["IMAGE"].header["CRPIX1A"], 1 - ha["IMAGE"].header["CRPIX2A"]); ob = (1 - hb["IMAGE"].header["CRPIX1A"], 1 - hb["IMAGE"].header["CRPIX2A"])
x0, x1 = int(max(oa[0], ob[0])), int(min(oa[0] + 29, ob[0] + 29)); y0, y1 = int(max(oa[1], ob[1])), int(min(oa[1] + 29, ob[1] + 29))
a = ha["IMAGE"].data[y0 - int(oa[1]):y1 - int(oa[1]), x0 - int(oa[0]):x1 - int(oa[0])]
b = hb["IMAGE"].data[y0 - int(ob[1]):y1 - int(ob[1]), x0 - int(ob[0]):x1 - int(ob[0])]
print("A/B overlap parent x", x0, x1, "y", y0, y1, "shape", a.shape, "IMAGE array_equal:", np.array_equal(a, b, equal_nan=True))
print("\nPARENT 0-based centroid differences (pixels):")
for m in ("peakpix", "com", "g2d"):
    print(m, {k: tuple(round(float(v), 6) for v in res[k][m]) for k in ("S3", "A", "B")})
    for (i, j) in (("A", "S3"), ("B", "S3"), ("A", "B")):
        print(f"   {i}-{j}: dx={res[i][m][0]-res[j][m][0]:+.3e} dy={res[i][m][1]-res[j][m][1]:+.3e}")
