import sys, json, time, urllib.request, urllib.parse, statistics, xml.etree.ElementTree as ET
from datetime import date
BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def get(url):
    for i in range(4):
        try:
            return urllib.request.urlopen(url, timeout=60).read()
        except Exception as e:
            time.sleep(2**i)
    raise RuntimeError(url)
def timeline(journal, years="2025:2026", n=300):
    term=f'"{journal}"[jour] AND {years.split(":")[0]}/01/01:{years.split(":")[1]}/12/31[dp] AND journal article[pt]'
    q=BASE+"esearch.fcgi?"+urllib.parse.urlencode(dict(db="pubmed",term=term,retmax=n,retmode="json"))
    ids=json.loads(get(q))["esearchresult"]["idlist"]
    if not ids: return None
    x=get(BASE+"efetch.fcgi?"+urllib.parse.urlencode(dict(db="pubmed",id=",".join(ids),retmode="xml")))
    root=ET.fromstring(x); d=[]
    for art in root.findall(".//PubmedArticle"):
        h={}
        for p in art.findall(".//History/PubMedPubDate"):
            s=p.get("PubStatus")
            try: h[s]=date(int(p.findtext("Year")),int(p.findtext("Month")),int(p.findtext("Day")))
            except: pass
        if "received" in h and "accepted" in h:
            v=(h["accepted"]-h["received"]).days
            if 0<=v<2000: d.append(v)
    if not d: return dict(journal=journal,n_ids=len(ids),n=0)
    d.sort()
    q=lambda p: d[int(p*(len(d)-1))]
    return dict(journal=journal,n_ids=len(ids),n=len(d),median=statistics.median(d),p25=q(.25),p75=q(.75),mean=round(statistics.mean(d),1),frac_le72=round(sum(v<=72 for v in d)/len(d),2))
if __name__=="__main__":
    for j in sys.argv[1:]:
        try: print(json.dumps(timeline(j)),flush=True)
        except Exception as e: print(j,"ERR",e,flush=True)
        time.sleep(0.5)
