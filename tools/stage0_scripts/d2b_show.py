import json
r=json.load(open(r"stage0\data\D\flagstats.json"))
print(len(r))
names=list(r[0]["frac"].keys())
for x in r: print(x["field"],x["det"],x["mjd"],x["ver"],x["tag"][-40:])
print("%-15s"%"bit"+" ".join("%8s"%(x["field"][:2]+x["det"][-1]) for x in r))
for n in names: print("%-15s"%n+" ".join("%8.5f"%(100*x["frac"][n]) for x in r))
for k in r[0]:
    if k.startswith(("ncomp","maxcomp")): print("%-22s"%k+" ".join("%8d"%x.get(k,0) for x in r))
