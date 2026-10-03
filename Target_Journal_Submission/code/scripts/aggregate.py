"""Aggregate per-job outputs into machine-readable result files and run the pre-specified statistics.

Writes: results/raw_results.csv, results/timings.csv, results/metrics.json, results/statistics.json,
        results/statistics_table.csv
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.statistics.tests import holm, paired_compare  # noqa: E402
from kincp.utils import RESULTS_DIR, dump_json  # noqa: E402

JOBS = RESULTS_DIR / "jobs"
COMPETITORS = ["Gauss-PEV", "Gauss-homosc", "SCP", "NormCP", "CV+", "CalPred-style", "CalPred-style(rand)"]
ABLATIONS = ["KinCP-A", "KinCP-B", "KinCP-C", "KinCP-AB", "KinCP-AC", "KinCP-BC", "KinCP-ABC"]
ENDPOINTS = [("cond_err", True), ("cov_dev", True), ("iscore", True)]


def load(mode: str = "full"):
    """Load only the jobs that belong to the requested mode's job list (prevents quick-mode duplicates)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
    from run_experiments import job_id, job_specs
    ids = [job_id(sp) for sp in job_specs(mode)]
    have = [i for i in ids if (JOBS / f"{i}__summary.csv").exists()]
    missing = sorted(set(ids) - set(have))
    s = pd.concat([pd.read_csv(JOBS / f"{i}__summary.csv") for i in have], ignore_index=True)
    t = pd.concat([pd.read_csv(JOBS / f"{i}__timing.csv") for i in have], ignore_index=True)
    s["job_id"] = np.repeat(have, [len(pd.read_csv(JOBS / f"{i}__summary.csv")) for i in have])
    return s, t, missing


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    s, t, missing = load(mode)
    dump_json(dict(mode=mode, n_jobs_loaded=int(s["job_id"].nunique()), missing_jobs=missing),
              RESULTS_DIR / "aggregation_manifest.json")
    s.to_csv(RESULTS_DIR / "raw_results.csv", index=False)
    t.to_csv(RESULTS_DIR / "timings.csv", index=False)
    real = s[(s["tag"] == "main")]
    units = ["dataset", "trait"]
    stats_rows = []
    for base in ["GBLUP", "RKHS", "LightGBM"]:
        for reg in ["R1", "R2", "R3"]:
            sub = real[(real.base == base) & (real.regime == reg) & (real.alpha == 0.10)]
            if sub.empty:
                continue
            for ep, lib in ENDPOINTS:
                comp = paired_compare(sub, units, "method", "KinCP", COMPETITORS + ABLATIONS, ep, lib)
                comp["base"], comp["regime"] = base, reg
                stats_rows.append(comp)
    st = pd.concat(stats_rows, ignore_index=True)
    # Holm correction within each (base, endpoint) family, separately for baselines and ablations
    st["family"] = np.where(st["competitor"].isin(ABLATIONS), "ablation", "baseline")
    st["p_holm"] = np.nan
    for _, g in st.groupby(["base", "endpoint", "family"]):
        ok = g["p_value"].notna()
        st.loc[g.index[ok], "p_holm"] = holm(g.loc[ok, "p_value"].to_numpy())
    st.to_csv(RESULTS_DIR / "statistics_table.csv", index=False)
    dump_json(dict(
        test="two-sided Wilcoxon signed-rank (zero_method='wilcox'), paired by dataset x trait",
        rationale="units are heterogeneous dataset-trait combinations; endpoint differences are not assumed normal",
        assumptions="independence across units (traits of one dataset share genotypes - see limitations); symmetric differences",
        multiplicity="Holm within (base predictor, endpoint, family) where family = baselines or ablations",
        effect_size="median paired difference (competitor - KinCP; positive favours KinCP for lower-is-better endpoints) with 95% bootstrap CI (10,000 resamples) and matched-pairs rank-biserial correlation",
        rows=st.to_dict(orient="records")), RESULTS_DIR / "statistics.json")
    # metrics.json: median over units of each endpoint per base/regime/method at alpha = 0.10
    m = (real[real.alpha == 0.10].groupby(["base", "regime", "method"])
         [["coverage", "cov_dev", "cond_err", "worst_bin_cov", "width", "iscore", "frac_inf"]].median())
    dump_json({f"{b}|{r}|{meth}": row.to_dict() for (b, r, meth), row in m.iterrows()}, RESULTS_DIR / "metrics.json")
    print("summaries:", len(s), "jobs:", s.groupby(["base", "regime", "tag"]).size().to_dict())


if __name__ == "__main__":
    main()
