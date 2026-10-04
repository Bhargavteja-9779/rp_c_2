"""EasyGeSe data access (Quesada-Traver et al. 2025, BMC Genomics; Zenodo record 15348871, CC-BY 4.0).

Each dataset has three files:
  <name>X.csv  genotypes, individuals x markers (first column = individual id)
  <name>Y.csv  phenotypes, individuals x traits
  <name>Z.json EasyGeSe's own 5 x 5-fold CV assignments per trait
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

from ..utils import DATA_DIR, get_logger

ZENODO_RECORD = "15348871"
ZENODO_URL = "https://zenodo.org/api/records/{rec}/files/{fn}/content"
DATASETS = ["barley", "bean", "lentil", "pine", "oyster", "maize", "pig", "rice", "soybean", "wheatG"]
SPECIES = {
    "barley": "Hordeum vulgare", "bean": "Phaseolus vulgaris", "lentil": "Lens culinaris",
    "pine": "Pinus taeda", "oyster": "Crassostrea virginica", "maize": "Zea mays",
    "pig": "Sus scrofa", "rice": "Oryza sativa", "soybean": "Glycine max", "wheatG": "Triticum aestivum",
}
COMMON = {
    "barley": "Barley", "bean": "Common bean", "lentil": "Lentil", "pine": "Loblolly pine",
    "oyster": "Eastern oyster", "maize": "Maize", "pig": "Pig", "rice": "Rice",
    "soybean": "Soybean", "wheatG": "Wheat",
}
log = get_logger("kincp.data")


def raw_dir() -> Path:
    d = DATA_DIR / "raw" / "easygese"
    d.mkdir(parents=True, exist_ok=True)
    return d


def zenodo_manifest() -> dict:
    """File name -> (size, md5) from the Zenodo record API."""
    url = f"https://zenodo.org/api/records/{ZENODO_RECORD}"
    with urllib.request.urlopen(url, timeout=120) as r:
        rec = json.loads(r.read())
    return {f["key"]: (int(f["size"]), f["checksum"].split(":")[-1]) for f in rec["files"]}


def download(name: str, force: bool = False, verify: bool = True, retries: int = 3) -> None:
    """Download the three files of one dataset from Zenodo (idempotent, md5-verified)."""
    manifest = zenodo_manifest() if verify else {}
    for suffix in ("X.csv", "Y.csv", "Z.json"):
        fn = f"{name}{suffix}"
        dest = raw_dir() / fn
        expect = manifest.get(fn)
        if dest.exists() and not force:
            if expect is None or dest.stat().st_size == expect[0]:
                continue
            log.warning("%s has wrong size; re-downloading", fn)
        url = ZENODO_URL.format(rec=ZENODO_RECORD, fn=fn)
        for attempt in range(retries):
            log.info("downloading %s (attempt %d)", url, attempt + 1)
            tmp = dest.with_suffix(dest.suffix + ".part")
            with urllib.request.urlopen(url, timeout=3600) as r, open(tmp, "wb") as fh:
                while True:
                    chunk = r.read(1 << 22)
                    if not chunk:
                        break
                    fh.write(chunk)
            if expect is None or md5(tmp) == expect[1]:
                tmp.rename(dest)
                break
            log.warning("md5 mismatch for %s", fn)
        else:
            raise IOError(f"could not download a verified copy of {fn}")


def verify_all() -> dict:
    """Check every local file against the Zenodo manifest (size + md5)."""
    manifest = zenodo_manifest()
    out = {}
    for fn, (size, h) in manifest.items():
        p = raw_dir() / fn
        if fn.endswith(".png"):
            continue
        out[fn] = bool(p.exists() and p.stat().st_size == size and md5(p) == h)
    return out


def md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def read_genotypes(name: str) -> tuple[np.ndarray, np.ndarray]:
    """Stream-parse <name>X.csv into an int8 dosage matrix coded 0/1/2.

    EasyGeSe codes some inbred datasets as {0,2} (kept as is) and wheat as {-2,0,2};
    the latter is shifted to {0,1,2}. No genotype is imputed (EasyGeSe files have no missing calls).
    """
    path = raw_dir() / f"{name}X.csv"
    ids, rows = [], []
    with open(path) as fh:
        fh.readline()  # header: marker names
        for line in fh:
            parts = line.rstrip("\n").split(",")
            ids.append(parts[0].strip('"'))
            rows.append(np.asarray(parts[1:], dtype=np.float32).astype(np.int8))
    X = np.vstack(rows)
    if X.min() < 0:  # {-2,0,2} -> {0,1,2}
        X = ((X.astype(np.int16) - X.min()) // 2).astype(np.int8)
    return np.asarray(ids, dtype=object), X


def read_phenotypes(name: str) -> pd.DataFrame:
    Y = pd.read_csv(raw_dir() / f"{name}Y.csv", index_col=0)
    Y.index = Y.index.astype(str)
    return Y


def read_cv_assignments(name: str) -> dict:
    with open(raw_dir() / f"{name}Z.json") as fh:
        return json.load(fh)


def easygese_folds(z: dict, trait: str, ids: np.ndarray, repeat: int) -> np.ndarray:
    """Return a fold label (0..4) per individual for EasyGeSe repeat `repeat` (1..5).

    EasyGeSe stores, per trait and individual, indicators 'Split{k}CV{r}' = 1 if the individual is in
    test fold k of CV repeat r (verified: every phenotyped individual has exactly one k per r).
    Individuals without a phenotype for that trait have no entry -> label -1.
    """
    zt = z[trait]
    out = np.full(len(ids), -1, dtype=int)
    for i, iid in enumerate(ids):
        rec = zt.get(str(iid))
        if rec is None:
            continue
        for k in range(1, 6):
            if rec.get(f"Split{k}CV{repeat}", 0) == 1:
                out[i] = k - 1
    return out


def eligible_traits(Y: pd.DataFrame, min_n: int | None = None, min_unique: int | None = None,
                    max_traits: int | None = None) -> list[str]:
    """Pre-specified, results-blind trait selection rule (see S0_preregistered_design.md; config/study.yaml)."""
    from ..utils import STUDY
    rule = STUDY["data"]["trait_rule"]
    min_n = rule["min_n"] if min_n is None else min_n
    min_unique = rule["min_unique"] if min_unique is None else min_unique
    max_traits = rule["max_traits"] if max_traits is None else max_traits
    stats = [(c, int(Y[c].notna().sum()), int(Y[c].nunique()), j) for j, c in enumerate(Y.columns)]
    ok = [s for s in stats if s[1] >= min_n and s[2] >= min_unique]
    ok.sort(key=lambda s: (-s[1], s[3]))
    return [s[0] for s in ok[:max_traits]]
