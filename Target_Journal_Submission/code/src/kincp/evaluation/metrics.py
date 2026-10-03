"""Interval metrics: coverage, width, interval score, relatedness-conditional coverage."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_BINS = 5


def add_basic(rec: pd.DataFrame) -> pd.DataFrame:
    rec = rec.copy()
    rec["covered"] = (rec["y"] >= rec["lo"]) & (rec["y"] <= rec["hi"])
    rec["width"] = rec["hi"] - rec["lo"]
    a = rec["alpha"]
    rec["iscore"] = rec["width"] + (2 / a) * np.maximum(rec["lo"] - rec["y"], 0) + (2 / a) * np.maximum(rec["y"] - rec["hi"], 0)
    return rec


def assign_bins(rec: pd.DataFrame, col: str = "d", n_bins: int = N_BINS) -> pd.Series:
    """Quintiles of the relatedness covariate, defined once per job over all test records of one
    method (the covariate does not depend on the method), pooled over repeats and folds."""
    ref = rec.drop_duplicates(["rep", "fold", "idx"])[col]
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, n_bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    return pd.Series(np.digitize(rec[col], edges[1:-1]), index=rec.index)


def summarize(rec: pd.DataFrame, keys=("dataset", "trait", "regime", "base", "tag")) -> pd.DataFrame:
    """One row per (job keys, method, alpha)."""
    rec = add_basic(rec)
    rec["bin"] = assign_bins(rec)
    rows = []
    for (meth, a), g in rec.groupby(["method", "alpha"], sort=False):
        target = 1 - a
        cov = g["covered"].mean()
        finite = np.isfinite(g["width"])
        binc = g.groupby("bin")["covered"].mean().reindex(range(N_BINS))
        binw = g[finite].groupby("bin")["width"].mean().reindex(range(N_BINS))
        per_rep = g.groupby("rep")["covered"].mean()
        r = {k: g[k].iloc[0] for k in keys if k in g}
        r.update(method=meth, alpha=a, n=len(g), coverage=cov, cov_dev=abs(cov - target),
                 cov_sd_reps=float(per_rep.std(ddof=1)) if len(per_rep) > 1 else np.nan,
                 width=float(g.loc[finite, "width"].mean()), frac_inf=float(1 - finite.mean()),
                 iscore=float(g.loc[np.isfinite(g["iscore"]), "iscore"].mean()),
                 cond_err=float(np.nanmean(np.abs(binc.values - target))),
                 worst_bin_cov=float(np.nanmin(binc.values)),
                 under_bin=float(np.nanmax(target - binc.values)))
        for b in range(N_BINS):
            r[f"cov_b{b + 1}"] = binc.iloc[b]
            r[f"width_b{b + 1}"] = binw.iloc[b]
        rows.append(r)
    return pd.DataFrame(rows)
