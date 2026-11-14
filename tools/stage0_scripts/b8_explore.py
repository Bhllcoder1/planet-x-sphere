import json, warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from photutils.detection import DAOStarFinder
warnings.filterwarnings("ignore")
B = r"stage0\data\B"
cands = json.load(open(B + r"\cands.json")); c = cands[4]
path = "s3://nasa-irsa-spherex/" + c["key"]
IDX = {"IMAGE": 1, "FLAGS": 2, "VARIANCE": 3, "ZODI": 4}
wx0, wy0 = int(c["x0"]) - 50, int(c["y0"]) - 50
hd = fits.open(path, fsspec_kwargs={"anon": True, "default_cache_type": "readahead", "default_block_size": 2**20}, lazy_load_hdus=True)
s3 = {n: np.array(hd[i].section[wy0:wy0 + 100, wx0:wx0 + 100]) for n, i in IDX.items()}
fullhdr = hd[1].header.copy()
fullhdr.tofile(B + r"\full_image_header.txt", sep="\n", endcard=True, padding=False, overwrite=True)
np.savez(B + r"\s3win.npz", wx0=wx0, wy0=wy0, **s3)
data = s3["IMAGE"].astype(float)
bg = np.nanmedian(data); sd = 1.4826 * np.nanmedian(np.abs(data - bg))
print("S3 IMAGE bg", bg, "sd", sd, "max", np.nanmax(data), "nan", np.isnan(data).sum())
t = DAOStarFinder(fwhm=2.0, threshold=5 * sd)(np.nan_to_num(data - bg))
t.sort("peak", reverse=True)
xc = "x_centroid" if "x_centroid" in t.colnames else "xcentroid"; yc = xc.replace("x", "y")
for r in t[:6]:
    print("S3 det parent x,y", round(r[xc] + wx0, 2), round(r[yc] + wy0, 2), "peak", round(r["peak"], 2))
print("predicted Barnard parent x,y (0-based)", c["x0"], c["y0"], " value there:", data[int(c["y0"]) - wy0, int(c["x0"]) - wx0], " max in +-3 px box:", np.nanmax(data[int(c["y0"]) - wy0 - 3:int(c["y0"]) - wy0 + 4, int(c["x0"]) - wx0 - 3:int(c["x0"]) - wx0 + 4]))
for tag in "AB":
    h = fits.open(B + rf"\cut\f0_{tag}.fits")
    hh = h["IMAGE"].header
    d = h["IMAGE"].data.astype(float)
    ox, oy = 1 - hh["CRPIX1A"], 1 - hh["CRPIX2A"]
    print("cutout", tag, "origin parent", ox, oy, "shape", d.shape, "max", np.nanmax(d), "median", np.nanmedian(d), "argmax parent", np.unravel_index(np.nanargmax(d), d.shape)[::-1], "+origin")
# where would the S3 star be in cutouts?
print("S3 brightest star parent x,y vs cutout A y range 1729..1757, B", )
