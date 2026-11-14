import s3fs, sys
fs = s3fs.S3FileSystem(anon=True)
for p in ['nasa-irsa-spherex', 'nasa-irsa-spherex/dr1', 'nasa-irsa-spherex/dr1/level2']:
    try:
        print(p, fs.ls(p)[:10], flush=True)
    except Exception as e:
        print(p, 'ERR', repr(e)[:200], flush=True)
