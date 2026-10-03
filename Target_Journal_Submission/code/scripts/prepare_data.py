"""Download (md5-verified) and preprocess all EasyGeSe datasets; write the data/leakage audit.

usage: python scripts/prepare_data.py [--datasets pine oyster ...] [--skip-download]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.data.easygese import (COMMON, DATASETS, SPECIES, download, easygese_folds, eligible_traits,  # noqa: E402
                                 read_cv_assignments, read_phenotypes)
from kincp.data.prepare import prepare  # noqa: E402
from kincp.preprocessing.genomic import near_duplicates, standardized_relationship  # noqa: E402
from kincp.utils import CACHE_DIR, RESULTS_DIR, dump_json  # noqa: E402


def audit(name: str) -> dict:
    g = prepare(name)
    Y = read_phenotypes(name)
    z = read_cv_assignments(name)
    traits = eligible_traits(Y)
    G = g["G"]
    Gstd = standardized_relationship(G)
    dups = near_duplicates(Gstd, 0.95)
    out = dict(dataset=name, species=SPECIES[name], common=COMMON[name], n=int(G.shape[0]),
               summary=json.load(open(CACHE_DIR / name / "geno_summary.json")),
               traits_selected=traits, n_traits_available=int(Y.shape[1]), near_dup_pairs_gt095=len(dups),
               cluster_sizes=np.bincount(g["clusters"]).tolist(), traits={})
    off = Gstd[np.triu_indices_from(Gstd, 1)]
    out["std_relationship_offdiag"] = dict(mean=float(off.mean()), p99=float(np.quantile(off, 0.99)),
                                           max=float(off.max()))
    for t in traits:
        y = Y[t].to_numpy(float)
        has = np.isfinite(y)
        unfolded = []
        for r in range(1, 6):
            lab = easygese_folds(z, t, g["ids"], r)
            unfolded.append(int((has & (lab < 0)).sum()))
        out["traits"][t] = dict(n=int(has.sum()), mean=float(np.nanmean(y)), sd=float(np.nanstd(y)),
                                skew=float(pd.Series(y).skew()), n_unique=int(pd.Series(y).nunique()),
                                phenotyped_without_easygese_fold=unfolded,
                                cluster_sizes_phenotyped=np.bincount(g["clusters"][has], minlength=5).tolist())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", nargs="*", default=DATASETS)
    ap.add_argument("--skip-download", action="store_true")
    a = ap.parse_args()
    rows = []
    for name in a.datasets:
        if not a.skip_download:
            download(name)
        rows.append(audit(name))
        print(name, "ok", flush=True)
    path = RESULTS_DIR / "data_audit.json"
    old = json.load(open(path)) if path.exists() else []
    keep = [r for r in old if r["dataset"] not in a.datasets]
    dump_json(keep + rows, path)


if __name__ == "__main__":
    main()
