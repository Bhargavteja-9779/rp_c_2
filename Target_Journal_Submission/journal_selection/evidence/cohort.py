import json,urllib.request,urllib.parse,xml.etree.ElementTree as ET,statistics,sys
from datetime import date
B="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def g(u): return urllib.request.urlopen(u,timeout=120).read()
def cohort(j,n=5000):
    term=f'"{j}"[jour] AND 2025/01/01:2026/12/31[dp] AND journal article[pt]'
    ids=json.loads(g(B+"esearch.fcgi?"+urllib.parse.urlencode(dict(db="pubmed",term=term,retmax=n,retmode="json"))))["esearchresult"]["idlist"]
    d=[]
    for i in range(0,len(ids),300):
        root=ET.fromstring(g(B+"efetch.fcgi?"+urllib.parse.urlencode(dict(db="pubmed",id=",".join(ids[i:i+300]),retmode="xml"))))
        for a in root.findall(".//PubmedArticle"):
            h={}
            for p in a.findall(".//History/PubMedPubDate"):
                try: h[p.get("PubStatus")]=date(int(p.findtext("Year")),int(p.findtext("Month")),int(p.findtext("Day")))
                except: pass
            if "received" in h and "accepted" in h and date(2025,1,1)<=h["received"]<=date(2025,6,30):
                v=(h["accepted"]-h["received"]).days
                if 0<=v<2000: d.append(v)
    d.sort()
    if not d: print(j,"no data"); return
    print(json.dumps(dict(journal=j,cohort="received 2025-01..2025-06",n=len(d),median=statistics.median(d),p25=d[len(d)//4],p75=d[3*len(d)//4],le72=round(sum(v<=72 for v in d)/len(d),3),le60=round(sum(v<=60 for v in d)/len(d),3),le30=round(sum(v<=30 for v in d)/len(d),3))),flush=True)
for j in sys.argv[1:]: cohort(j)
