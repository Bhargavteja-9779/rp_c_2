import sys, json, time, urllib.request, urllib.parse, statistics
from datetime import date
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"research-timeline-check/1.0 (mailto:research@example.org)"})
    for i in range(4):
        try: return json.loads(urllib.request.urlopen(req,timeout=90).read())
        except Exception as e: time.sleep(2**i)
    raise RuntimeError(url)
def parse(s):
    for fmt in ("%Y-%m-%d","%d %B %Y","%d %b %Y","%B %d, %Y"):
        try:
            from datetime import datetime
            return datetime.strptime(s.strip(),fmt).date()
        except: pass
    return None
def timeline(issn, frm="2025-07-01", until="2026-09-30", rows=600):
    url=f"https://api.crossref.org/journals/{issn}/works?"+urllib.parse.urlencode({"filter":f"from-pub-date:{frm},until-pub-date:{until},type:journal-article","rows":rows,"select":"DOI,assertion,container-title"})
    r=get(url)["message"]; items=r["items"]; d=[]; name=None
    for it in items:
        name=name or (it.get("container-title") or [None])[0]
        a={x.get("name","").lower():x.get("value","") for x in it.get("assertion",[]) or []}
        rec=a.get("received") or a.get("date_received") or a.get("received_date")
        acc=a.get("accepted") or a.get("date_accepted") or a.get("accepted_date")
        if rec and acc:
            r1,a1=parse(rec),parse(acc)
            if r1 and a1 and 0<=(a1-r1).days<2000: d.append((a1-r1).days)
    if not d: return dict(issn=issn,name=name,n_items=len(items),n=0)
    d.sort(); q=lambda p:d[int(p*(len(d)-1))]
    return dict(issn=issn,name=name,total=r["total-results"],n=len(d),median=statistics.median(d),p25=q(.25),p75=q(.75),frac_le72=round(sum(v<=72 for v in d)/len(d),2))
if __name__=="__main__":
    for s in sys.argv[1:]:
        try: print(json.dumps(timeline(s)),flush=True)
        except Exception as e: print(s,"ERR",e,flush=True)
