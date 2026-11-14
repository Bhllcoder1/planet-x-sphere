import fitz,sys
d=fitz.open(r"sources_pdf\SPHEREx_Expsupp.pdf")
out=open(r"stage0\data\D\expsupp.txt","w",encoding="utf8")
for i,p in enumerate(d,1):
    out.write(f"\n=====PAGE {i}=====\n"+p.get_text())
print(len(d))
