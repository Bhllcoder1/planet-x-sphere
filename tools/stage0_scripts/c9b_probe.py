import requests
for u in ['https://vizier.cds.unistra.fr/viz-bin/votable?-source=I/355/gaiadr3&-c=269.452+4.693&-c.rd=0.01&-out.max=3&-out=Source,RA_ICRS,DE_ICRS,Gmag',
          'https://vizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=SELECT+TOP+1+*+FROM+%22I/355/gaiadr3%22',
          'https://cds.unistra.fr/', 'https://gea.esac.esa.int/tap-server/tap/sync',
          'https://mast.stsci.edu/vo-tap/api/v0.1/gaiadr3/sync',
          'https://irsa.ipac.caltech.edu/TAP/sync']:
    try:
        r = requests.get(u, timeout=20)
        print(r.status_code, u[:80], r.text[:200].replace('\n', ' '), flush=True)
    except Exception as e:
        print('ERR', u[:80], ascii(repr(e))[:100], flush=True)
