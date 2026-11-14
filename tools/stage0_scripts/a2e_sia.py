"""SIA coverage fallback (DIFFERENT service from TAP). Writes data/A/tap_<T>.csv in the same column layout (uri,producttype,...,time_bounds_lower/upper,provenance_version) + sia_<T>_raw.csv"""
import sys,io,csv,time,math,re,requests
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
T={"WISE0855":(133.795129,-7.245147,-8118.0,680.0,2014.0),"RWAur":(76.95653,30.40144,0,0,2000.0),"RDra":(248.16738,66.75500,0,0,2016.0)}
k=sys.argv[1]; ra,dec,pa,pd_,ep=T[k]; dt=2026.0-ep
ra2=ra+pa*dt/3.6e6/math.cos(math.radians(dec)); dec2=dec+pd_*dt/3.6e6
rows=[]
for coll in ("spherex_dr1","spherex_qr3","spherex_qr2"):
    url=f"https://irsa.ipac.caltech.edu/SIA?COLLECTION={coll}&POS=circle+{ra2:.6f}+{dec2:.6f}+0.1&RESPONSEFORMAT=CSV"
    for i in range(3):
        try:
            r=requests.get(url,timeout=300)
            if r.status_code==200 and "<html" not in r.text[:200].lower() and "<?xml" not in r.text[:50]:
                rr=list(csv.DictReader(io.StringIO(r.text))); print(k,coll,len(rr),"rows",flush=True)
                for x in rr: x["_coll"]=coll
                rows+=rr; break
            print(k,coll,"HTTP",r.status_code,r.text[:150].replace("\n"," "),flush=True)
        except Exception as e: print(k,coll,"ERR",str(e)[:150],flush=True)
        time.sleep(10*2**i)
    else: print(k,coll,"FAILED after 3 tries",flush=True)
if rows: print(k,"sample access_url:",rows[0]["access_url"],rows[0]["t_min"],rows[0]["t_max"],flush=True)
w=csv.writer(open(rf"stage0\data\A\sia_{k}_raw.csv","w",newline="",encoding="utf-8"))
if rows:
    w.writerow(rows[0].keys()); [w.writerow(x.values()) for x in rows]
out=[]
for x in rows:
    m=re.search(r"(ibe/data/spherex/.*?\.fits)",x["access_url"]); 
    if not m: continue
    out.append({"uri":m.group(1),"producttype":"science","releasetype":x["_coll"],"planeid":"","productid":"","metarelease":"","datarelease":"","calibrationlevel":x.get("calib_level",""),"dataproducttype":x.get("dataproduct_type",""),"quality_flag":"","energy_bandpassname":x.get("energy_bandpassname",""),"time_bounds_lower":x["t_min"],"time_bounds_upper":x["t_max"],"provenance_version":"(SIA: not available)","provenance_name":"SIA"})
print(k,"converted",len(out),"of",len(rows),flush=True)
if out:
    cw=csv.DictWriter(open(rf"stage0\data\A\tap_{k}.csv","w",newline="",encoding="utf-8"),fieldnames=list(out[0].keys())); cw.writeheader(); cw.writerows(out)
