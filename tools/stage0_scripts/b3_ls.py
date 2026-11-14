import s3fs, csv
fs = s3fs.S3FileSystem(anon=True)
for p in ["nasa-irsa-spherex", "nasa-irsa-spherex/dr1", "nasa-irsa-spherex/spherex", "nasa-irsa-spherex/qr3"]:
    try:
        print(p, fs.ls(p)[:12])
    except Exception as e:
        print(p, "ERR", repr(e)[:150])
rows = list(csv.DictReader(open(r"stage0\data\B\tap.csv", encoding="utf-8")))
from collections import Counter
print(Counter(r["uri"].split("/")[3] + "/" + r["uri"].split("/")[5] for r in rows))
print(Counter(r["energy_bandpassname"] for r in rows))
print(rows[0]["uri"])
