import sys,s3fs
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
fs=s3fs.S3FileSystem(anon=True)
uri="ibe/data/spherex/dr1/level2/2025W33_2C/l2b-v27-2026-228/3/level2_2025W33_2C_0321_1D3_spx_l2b-v27-2026-228.fits"
for key in [uri[len("ibe/data/spherex/"):]]:
    p="nasa-irsa-spherex/"+key
    try: print(p, fs.info(p)["size"])
    except Exception as e: print(p,"FAIL",type(e).__name__,str(e)[:100])
print(fs.ls("nasa-irsa-spherex/")[:10])

