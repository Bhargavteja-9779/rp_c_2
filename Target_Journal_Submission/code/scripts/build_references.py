"""Build the CSE name-year reference list from verified metadata and audit in-text citations.

Inputs: supplementary/citations/verified_refs.json (Crossref-verified), manual_refs.json (verified by
publisher page / arXiv / Zenodo / JSTOR). Output: manuscript/src/04_references.md and
supplementary/citations/citation_audit.json (cited-but-missing and listed-but-uncited checks).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[2]
CIT = PKG / "supplementary" / "citations"
SRC = PKG / "manuscript" / "src"

# key -> in-text form used in the manuscript (CSE name-year)
CITED = {
    "meuwissen2001": "Meuwissen *et al.* 2001", "crossa2017": "Crossa *et al.* 2017",
    "ahlinder2026": "Ahlinder and Waldmann (2026)", "habier2007": "Habier *et al.* 2007",
    "clark2012": "Clark *et al.* 2012", "pszczola2012": "Pszczola *et al.* 2012",
    "wientjes2013": "Wientjes *et al.* 2013", "werner2020": "Werner *et al.* 2020",
    "henderson1975": "Henderson 1975", "vanraden2008": "VanRaden 2008", "vovk2005": "Vovk *et al.* 2022",
    "lei2018": "Lei *et al.* 2018", "angelopoulos2023": "Angelopoulos and Bates 2023",
    "hou2024": "Hou *et al.* 2024", "predinterval": "Xu *et al.* 2025", "kumar2026": "Kumar 2026",
    "ding2023": "Ding *et al.* 2023", "tibshirani2019": "Tibshirani *et al.* 2019",
    "barber2023": "Barber *et al.* 2023", "guan2023": "Guan 2023", "gibbs2025cc": "Gibbs *et al.* 2025",
    "quesada2025": "Quesada-Traver *et al.* 2025", "haile2020": "Haile *et al.* 2020",
    "resende2012": "Resende *et al.* 2012", "washburn2025": "Washburn *et al.* 2025",
    "zhao2011": "Zhao *et al.* 2011", "kaler2017": "Kaler *et al.* 2017", "gogna2022": "Gogna *et al.* 2022",
    "kang2008": "Kang *et al.* (2008)", "gianola2008": "Gianola and van Kaam 2008",
    "delos2010": "de los Campos *et al.* 2010", "ke2017": "Ke *et al.* 2017",
    "barber2021": "Barber *et al.* 2021", "gneiting2007": "Gneiting and Raftery 2007",
    "wilcoxon1945": "Wilcoxon 1945", "holm1979": "Holm 1979", "efron1979": "Efron 1979",
    "kerby2014": "Kerby 2014", "jin2023": "Jin and Candès 2023", "legarra2018": "Legarra and Reverter (2018)",
    "sun2021": "Sun *et al.* 2021", "kodji2026": "Kodji *et al.* 2026", "vovk2013": "Vovk 2013",
    "papadopoulos2002": "Papadopoulos *et al.* 2002", "dunn2023": "Dunn *et al.* 2023",
    "bhattacharyya2024": "Bhattacharyya and Barber 2026",
}


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "")


def fmt(r: dict) -> str:
    def norm(name):
        parts = name.split(" ")
        if len(parts) >= 2 and " ".join(parts[:-1]).isupper():
            sur = " ".join(parts[:-1]).title()
            sur = re.sub(r"^De Los ", "de los ", sur)
            return f"{sur} {parts[-1]}"
        return name
    au = [norm(x) for x in r["authors"]]
    a = ", ".join(au[:10]) + (", et al" if len(au) > 10 else "")
    title = strip_tags(r["title"]).rstrip(".")
    j = r.get("journal") or ""
    vol = r.get("volume")
    iss = r.get("issue")
    pg = r.get("pages")
    s = f"{a}. {r['year']}. {title}."
    if j:
        s += f" {j}."
    if vol:
        s += f" {vol}"
        if iss:
            s += f"({iss})"
        if pg:
            s += f":{pg.replace('-', '–')}"
        s += "."
    elif pg:
        s += f" {pg}."
    if r.get("doi"):
        s += f" doi:{r['doi']}"
    elif r.get("url"):
        s += f" {r['url']}"
    return s


def main():
    v = json.load(open(CIT / "verified_refs.json"))
    m = json.load(open(CIT / "manual_refs.json"))
    v.update(m)
    # Vovk et al. book: Crossref returns the 2nd edition (2022, Springer)
    v["vovk2005"]["journal"] = "Springer, Cham (2nd edition)"
    text = "\n".join(p.read_text() for p in sorted(SRC.glob("0[1-3]*.md")))
    entries, audit = [], {"missing_in_text": [], "not_verified": [], "uncited_name_year_strings": []}
    for k, intext in CITED.items():
        r = v.get(k)
        if not r or not str(r.get("status", "")).startswith("OK"):
            audit["not_verified"].append(k)
            continue
        if intext.replace("*", "") not in text.replace("*", "") and intext.split(" (")[0].replace("*", "") not in text.replace("*", ""):
            audit["missing_in_text"].append(k)
        entries.append((r["authors"][0].lower(), r["year"], fmt(r)))
    # find name-year strings in text that are not in CITED
    known = {c.replace("*", "").replace("(", "").replace(")", "") for c in CITED.values()}
    for mm in re.finditer(r"([A-Z][A-Za-z\-ü]+(?: (?:and|et al\.) ?[A-Za-zè\-]*)?)\s\(?(\d{4})\)?", text.replace("*", "")):
        s = f"{mm.group(1).strip()} {mm.group(2)}"
        if 1900 < int(mm.group(2)) < 2030 and not any(s in kk or kk in s for kk in known):
            audit["uncited_name_year_strings"].append(s)
    audit["uncited_name_year_strings"] = sorted(set(audit["uncited_name_year_strings"]))
    entries.sort()
    out = "## Literature cited\n\n" + "\n\n".join(e[2] for e in entries) + "\n"
    (SRC / "04_references.md").write_text(out)
    json.dump(audit, open(CIT / "citation_audit.json", "w"), indent=1)
    print(len(entries), "references;", json.dumps(audit, indent=1))


if __name__ == "__main__":
    main()
