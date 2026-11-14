import requests,re
q="SELECT TOP 2 a.uri FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid WHERE (1=CONTAINS(POINT('ICRS',269.4,4.7),p.poly) OR 1=CONTAINS(POINT('ICRS',269.5,4.8),p.poly))"
r=requests.post("https://irsa.ipac.caltech.edu/TAP/sync",data={"QUERY":q,"FORMAT":"csv","LANG":"ADQL"},timeout=300)
print(r.status_code,r.text[:900])
