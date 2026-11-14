import requests, io, csv, sys, json
D=r"stage0\data\D"
fields={"sparse_ecl":(180.0,0.0)}
for name,(ra,dec) in fields.items():
    q=f"SELECT a.uri, p.energy_bandpassname, p.time_bounds_lower, p.provenance_version, p.quality_flag, p.metrics_sourcenumberdensity FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE 1=CONTAINS(POINT('ICRS',{ra},{dec}),p.poly) ORDER BY p.time_bounds_lower"
    r=requests.get("https://irsa.ipac.caltech.edu/TAP/sync",params={"QUERY":q,"FORMAT":"csv"},timeout=300)
    print(name,r.status_code,len(r.text.splitlines()))
    open(f"{D}\\frames_{name}.csv","w",encoding="utf8").write(r.text)
    print("\n".join(r.text.splitlines()[:4]))

