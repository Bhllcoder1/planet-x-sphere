"""Async TAP retry for targets whose sync query timed out. usage: a2b_async.py TARGET"""
import sys,time,io,csv,re,requests
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
sys.path.insert(0,r"stage0\scripts")
import math
T={"WISE0855":(133.795129,-7.245147,-8118.0,680.0,2014.0),"RWAur":(76.95653,30.40144,0,0,2000.0),"RDra":(248.16738,66.75500,0,0,2016.0)}
k=sys.argv[1]; ra,dec,pa,pd_,ep=T[k]; dt=2026.0-ep
ra2=ra+pa*dt/3.6e6/math.cos(math.radians(dec)); dec2=dec+pd_*dt/3.6e6
q="SELECT a.uri,a.producttype,a.releasetype,p.planeid,p.productid,p.metarelease,p.datarelease,p.calibrationlevel,p.dataproducttype,p.quality_flag,p.energy_bandpassname,p.time_bounds_lower,p.time_bounds_upper,p.provenance_version,p.provenance_name FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE (1=CONTAINS(POINT('ICRS',%.6f,%.6f),p.poly))"%(ra2,dec2)
B="https://irsa.ipac.caltech.edu/TAP/async"
for _i in range(4):
    r=requests.post(B,data={"QUERY":q,"LANG":"ADQL","FORMAT":"csv","PHASE":"RUN","MAXREC":"100000"},allow_redirects=False,timeout=120)
    if r.headers.get("Location"): break
    print(k,"submit retry",r.status_code,flush=True); time.sleep(20*(_i+1))
loc=r.headers.get("Location"); print(k,"submit",r.status_code,loc,flush=True)
if not loc: print(k,"NOT COMPLETED submit failed"); sys.exit(1)
t0=time.time()
while time.time()-t0<600:
    try: ph=requests.get(loc+"/phase",timeout=60).text.strip()
    except Exception as e: ph="POLLERR"
    print(k,round(time.time()-t0),ph,flush=True)
    if ph in("COMPLETED","ERROR","ABORTED"): break
    time.sleep(20)
if ph=="COMPLETED":
    txt=requests.get(loc+"/results/result",timeout=300).text
    open(rf"stage0\data\A\tap_{k}.csv","w",encoding="utf-8").write(txt)
    print(k,len(list(csv.DictReader(io.StringIO(txt)))),"rows",flush=True)
else: print(k,"NOT COMPLETED",ph,flush=True)
