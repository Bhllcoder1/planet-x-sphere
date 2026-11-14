import requests,sys
ra,dec=269.446,4.768
qs={"cols":"SELECT TOP 3 a.uri,a.producttype,a.releasetype,p.planeid,p.productid,p.metarelease,p.datarelease,p.calibrationlevel,p.dataproducttype,p.quality_flag,p.energy_bandpassname,p.time_bounds_lower,p.time_bounds_upper,p.provenance_version,p.provenance_name,p.provenance_runid FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE 1=CONTAINS(POINT('ICRS',%f,%f),p.poly)"%(ra,dec),
"inter":"SELECT TOP 3 a.uri FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE 1=INTERSECTS(CIRCLE('ICRS',%f,%f,0.1),p.poly)"%(ra,dec)}
for k,q in qs.items():
    r=requests.post("https://irsa.ipac.caltech.edu/TAP/sync",data={"QUERY":q,"FORMAT":"csv","LANG":"ADQL"},timeout=300)
    print(k,r.status_code,r.text[:700])
