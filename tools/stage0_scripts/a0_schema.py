import requests
r=requests.get("https://irsa.ipac.caltech.edu/TAP/sync",params={"QUERY":"SELECT table_name,column_name FROM TAP_SCHEMA.columns WHERE table_name IN ('spherex.plane','spherex.artifact')","FORMAT":"csv"},timeout=120)
print(r.status_code); print(r.text.replace("\n"," | "))
