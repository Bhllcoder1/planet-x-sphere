import s3fs
fs=s3fs.S3FileSystem(anon=True)
print(fs.ls("nasa-irsa-spherex")[:20])
