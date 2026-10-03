"""Paired, non-parametric comparisons of interval methods across dataset x trait units."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def holm(p: np.ndarray) -> np.ndarray:
    """Holm (1979) step-down adjusted p-values."""
    p = np.asarray(p, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, (m - r) * p[i])
        adj[i] = min(1.0, run)
    return adj


def rank_biserial(diff: np.ndarray) -> float:
    """Matched-pairs rank-biserial correlation (Kerby 2014): (R+ - R-) / (R+ + R-), zero differences dropped."""
    d = diff[diff != 0]
    if len(d) == 0:
        return 0.0
    r = stats.rankdata(np.abs(d))
    rp, rm = r[d > 0].sum(), r[d < 0].sum()
    return float((rp - rm) / (rp + rm))


def bootstrap_median_ci(diff: np.ndarray, n_boot: int = 10000, seed: int = 2026, level: float = 0.95):
    rng = np.random.default_rng(seed)
    b = np.median(rng.choice(diff, size=(n_boot, len(diff)), replace=True), axis=1)
    a = (1 - level) / 2
    return float(np.quantile(b, a)), float(np.quantile(b, 1 - a))


def paired_compare(df: pd.DataFrame, unit_cols, method_col: str, ref: str, competitors, endpoint: str,
                   lower_is_better: bool = True) -> pd.DataFrame:
    """Wilcoxon signed-rank test of ref vs each competitor on `endpoint`, paired by unit.
    diff = competitor - ref (positive = ref better when lower_is_better)."""
    wide = df.pivot_table(index=list(unit_cols), columns=method_col, values=endpoint, aggfunc="mean")
    rows = []
    for c in competitors:
        if c not in wide or ref not in wide:
            continue
        sub = wide[[ref, c]].dropna()
        sub = sub[np.isfinite(sub).all(axis=1)]
        diff = (sub[c] - sub[ref]).to_numpy()
        if not lower_is_better:
            diff = -diff
        if len(diff) < 5 or np.all(diff == 0):
            p = np.nan
        else:
            p = float(stats.wilcoxon(diff, zero_method="wilcox", alternative="two-sided").pvalue)
        lo, hi = bootstrap_median_ci(diff) if len(diff) else (np.nan, np.nan)
        rows.append(dict(endpoint=endpoint, reference=ref, competitor=c, n_units=len(diff),
                         ref_median=float(sub[ref].median()), comp_median=float(sub[c].median()),
                         median_diff=float(np.median(diff)) if len(diff) else np.nan, ci_low=lo, ci_high=hi,
                         rank_biserial=rank_biserial(diff), wins_ref=int((diff > 0).sum()),
                         wins_comp=int((diff < 0).sum()), ties=int((diff == 0).sum()), p_value=p))
    return pd.DataFrame(rows)
