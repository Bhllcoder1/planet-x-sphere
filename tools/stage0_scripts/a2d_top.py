import requests,time,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for k,(ra,dec) in {"WISE0855":(133.76785,-7.24288),"RWAur":(76.95653,30.40144),"RDra":(248.16738,66.755)}.items():
    q="SELECT TOP 5 a.uri,p.time_bounds_lower FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE 1=CONTAINS(POINT('ICRS',%f,%f),p.poly)"%(ra,dec)
    t0=time.time()
    try:
        r=requests.post("https://irsa.ipac.caltech.edu/TAP/sync",data={"QUERY":q,"FORMAT":"csv","LANG":"ADQL"},timeout=300)
        print(k,r.status_code,round(time.time()-t0),r.text[:300].replace("\n"," | "),flush=True)
    except Exception as e: print(k,"ERR",e,flush=True)
