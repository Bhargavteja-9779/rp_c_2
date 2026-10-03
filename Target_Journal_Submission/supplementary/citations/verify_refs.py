"""Verify references against Crossref (bibliographic query); writes verified_refs.json."""
import json, sys, time, urllib.parse, urllib.request
Q = json.load(open("queries.json"))
H = {"User-Agent": "kincp-citation-audit/1.0 (mailto:research@example.org)"}
def get(u):
    for i in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read())
        except Exception: time.sleep(2 ** i)
out = {}
for key, q in Q.items():
    if q.get("doi"):
        m = get("https://api.crossref.org/works/" + urllib.parse.quote(q["doi"]))
        it = m["message"] if m else None
    else:
        m = get("https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q["q"], "rows": 3}))
        it = m["message"]["items"][0] if m and m["message"]["items"] else None
    if not it: out[key] = {"status": "NOT FOUND", "query": q}; continue
    au = [f"{a.get('family','')} {''.join(x[0] for x in a.get('given','').replace('-',' ').split())}".strip() for a in it.get("author", [])]
    y = (it.get("published-print") or it.get("published-online") or it.get("issued"))["date-parts"][0][0]
    out[key] = dict(status="OK", doi=it.get("DOI"), title=(it.get("title") or [""])[0], authors=au,
                    year=y, journal=(it.get("container-title") or [""])[0], volume=it.get("volume"),
                    issue=it.get("issue"), pages=it.get("page") or it.get("article-number"), type=it.get("type"))
    print(key, "|", y, "|", ", ".join(au[:3]), "|", out[key]["title"][:90], "|", out[key]["journal"][:40], out[key]["volume"], out[key]["pages"], "|", it.get("DOI"))
json.dump(out, open("verified_refs.json", "w"), indent=1)
