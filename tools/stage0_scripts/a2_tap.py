import sys,time,io,csv,math,requests
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
T={"Barnard":(269.44850,4.73942,-801.55,10362.39,2016.0),
"EpsInd_A":(330.87241,-56.79725,3966.66,-2536.19,2016.0),
"EpsInd_B":(331.07645,-56.79381,3981.98,-2466.83,2016.0),
"WISE0855":(133.795129,-7.245147,-8118.0,680.0,2014.0),
"RWAur":(76.95653,30.40144,0,0,2000.0),
"RDra":(248.16738,66.75500,0,0,2016.0)}
def prop(ra,dec,pmra,pmdec,ep,to=2026.0):
    dt=to-ep
    return ra+pmra*dt/3.6e6/math.cos(math.radians(dec)), dec+pmdec*dt/3.6e6
def tap(q):
    for i in range(3):
        try:
            r=requests.post("https://irsa.ipac.caltech.edu/TAP/sync",data={"QUERY":q,"FORMAT":"csv","LANG":"ADQL"},timeout=400)
            if r.status_code==200 and 'value="ERROR"' not in r.text: return r.text
            print("HTTP",r.status_code,r.text[:300],flush=True)
        except Exception as e: print("ERR",e,flush=True)
        time.sleep(5*2**i)
    return None
for k,(ra,dec,pa,pd_,ep) in [(n,T[n]) for n in (sys.argv[1:] or T)]:
    cond="1=CONTAINS(POINT('ICRS',%.6f,%.6f),p.poly)"%prop(ra,dec,pa,pd_,ep,2026.0)
    q="SELECT a.uri,a.producttype,a.releasetype,p.planeid,p.productid,p.metarelease,p.datarelease,p.calibrationlevel,p.dataproducttype,p.quality_flag,p.energy_bandpassname,p.time_bounds_lower,p.time_bounds_upper,p.provenance_version,p.provenance_name FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE ("+cond+")"
    t0=time.time(); txt=tap(q)
    if txt is None: print(k,"FAILED",flush=True); continue
    open(f"data/A/tap_{k}.csv","w",encoding="utf-8").write(txt)
    rows=list(csv.DictReader(io.StringIO(txt))); print(k,len(rows),"rows",round(time.time()-t0),"s",flush=True)

