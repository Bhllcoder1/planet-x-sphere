import requests, sys, io, csv, time
URL = "https://irsa.ipac.caltech.edu/TAP/sync"
RA, DEC = 269.446, 4.766   # Barnard's Star ~2025.5 (J2000 269.452,+4.694 + PM)
q = (f"SELECT a.*, p.time_bounds_lower, p.energy_bandpassname, p.provenance_version "
     f"FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid "
     f"WHERE 1=CONTAINS(POINT('ICRS',{RA},{DEC}),p.poly) ORDER BY p.time_bounds_lower")
t = time.time()
r = requests.post(URL, data={"QUERY": q, "FORMAT": "csv", "LANG": "ADQL"}, timeout=300)
print(r.status_code, len(r.text), round(time.time() - t, 1), "s")
open(sys.argv[1], "w", encoding="utf-8").write(r.text)
rows = list(csv.DictReader(io.StringIO(r.text)))
print(len(rows))
if rows:
    print(list(rows[0].keys()))
    for x in rows[:3]:
        print(x)
else:
    print(r.text[:800])
