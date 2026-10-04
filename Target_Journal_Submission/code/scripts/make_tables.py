"""Generate all manuscript tables from machine-readable results (CSV + Markdown in tables/)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.data.easygese import COMMON, SPECIES  # noqa: E402
from kincp.utils import RESULTS_DIR, TAB_DIR  # noqa: E402

BASELINES = ["Gauss-PEV", "Gauss-homosc", "SCP", "NormCP", "CV+", "CalPred-style(rand)", "CalPred-style", "KinCP"]
ABL = ["KinCP", "KinCP-A", "KinCP-B", "KinCP-C", "KinCP-AB", "KinCP-AC", "KinCP-BC", "KinCP-ABC"]
ABL_NAME = {"KinCP": "A+B+C (KinCP)", "KinCP-A": "B+C", "KinCP-B": "A+C", "KinCP-C": "A+B", "KinCP-AB": "C",
            "KinCP-AC": "B", "KinCP-BC": "A", "KinCP-ABC": "none"}


def write(df: pd.DataFrame, name: str, floatfmt=3):
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(TAB_DIR / f"{name}.csv", index=False)
    (TAB_DIR / f"{name}.md").write_text(df.to_markdown(index=False, floatfmt=f".{floatfmt}f"))


def mean_sd(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return f"{x.mean():.3f} ± {x.std(ddof=1):.3f}" if len(x) > 1 else (f"{x.mean():.3f}" if len(x) else "NA")


def table1():
    a = json.load(open(RESULTS_DIR / "data_audit.json"))
    t = pd.read_csv(RESULTS_DIR / "timings.csv")
    t = t[t.alpha.isna() & (t.base == "GBLUP") & (t.tag == "main") & (t.regime == "R1")]
    h2 = t.groupby(["dataset", "trait"]).agg(h2=("h2_reml", "mean"), r=("r_pred", "mean")).reset_index()
    rows = []
    for r in sorted(a, key=lambda r: COMMON[r["dataset"]]):
        for tr in r["traits_selected"]:
            hh = h2[(h2.dataset == r["dataset"]) & (h2.trait == tr)]
            rows.append({"Species": f"{COMMON[r['dataset']]} ({SPECIES[r['dataset']]})", "Trait": tr,
                         "n phenotyped": r["traits"][tr]["n"], "Markers": r["summary"]["m_polymorphic"],
                         "Near-duplicate pairs (>0.95)": r["near_dup_pairs_gt095"],
                         "Cluster sizes (k-means, k=5)": "/".join(map(str, r["traits"][tr]["cluster_sizes_phenotyped"])),
                         "REML h² (R1)": float(hh.h2.iloc[0]) if len(hh) else np.nan,
                         "GBLUP r (R1)": float(hh.r.iloc[0]) if len(hh) else np.nan})
    write(pd.DataFrame(rows), "Table1_datasets")


def summary_table(s, methods, name, base="GBLUP", namemap=None):
    rows = []
    for reg in ["R1", "R2", "R3"]:
        g = s[(s.tag == "main") & (s.base == base) & (s.regime == reg) & (s.alpha == 0.10)]
        if g.empty:
            continue
        for m in methods:
            v = g[g.method == m]
            if v.empty:
                continue
            rows.append({"Regime": reg, "Method": (namemap or {}).get(m, m), "Units": len(v),
                         "Coverage": mean_sd(v.coverage), "Abs. cov. deviation": mean_sd(v.cov_dev),
                         "Cond. error": mean_sd(v.cond_err), "Worst-quintile cov.": mean_sd(v.worst_bin_cov),
                         "Width (SD units)": mean_sd(v.width), "Interval score": mean_sd(v.iscore)})
    write(pd.DataFrame(rows), name)


def table_stats():
    st = pd.read_csv(RESULTS_DIR / "statistics_table.csv")
    st = st[st.base == "GBLUP"]
    st = st[["regime", "endpoint", "family", "competitor", "n_units", "ref_median", "comp_median", "median_diff",
             "ci_low", "ci_high", "rank_biserial", "wins_ref", "wins_comp", "p_value", "p_holm"]]
    st = st.rename(columns={"regime": "Regime", "endpoint": "Endpoint", "family": "Family", "competitor": "Competitor",
                            "n_units": "Units", "ref_median": "KinCP median", "comp_median": "Competitor median",
                            "median_diff": "Median diff.", "ci_low": "CI low", "ci_high": "CI high",
                            "rank_biserial": "Rank-biserial r", "wins_ref": "KinCP better", "wins_comp": "Competitor better",
                            "p_value": "P", "p_holm": "P (Holm)"})
    st["Endpoint"] = st["Endpoint"].map({"cond_err": "Cond. error", "cov_dev": "Abs. cov. deviation", "iscore": "Interval score"})
    write(st, "Table3_statistics_GBLUP", 4)
    st2 = pd.read_csv(RESULTS_DIR / "statistics_table.csv")
    write(st2[st2.base != "GBLUP"], "TableS_statistics_other_bases", 4)


def table_bases(s):
    rows = []
    for b in ["GBLUP", "RKHS", "LightGBM"]:
        for reg in ["R1", "R2"]:
            g = s[(s.tag == "main") & (s.base == b) & (s.regime == reg) & (s.alpha == 0.10)]
            for m in ["SCP", "CV+", "CalPred-style", "KinCP"] + (["Gauss-PEV"] if b == "GBLUP" else []):
                v = g[g.method == m]
                if v.empty:
                    continue
                rows.append({"Base": b, "Regime": reg, "Method": m, "Units": len(v), "Coverage": mean_sd(v.coverage),
                             "Cond. error": mean_sd(v.cond_err), "Worst-quintile cov.": mean_sd(v.worst_bin_cov),
                             "Width": mean_sd(v.width)})
    write(pd.DataFrame(rows), "Table5_base_predictors")


def table_sim(s):
    g = s[(s.tag == "sim") & (s.alpha == 0.10)]
    if g.empty:
        return
    rows = []
    for (reg, h2, nq), gg in g.groupby(["regime", "h2", "n_qtl"]):
        for m in ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]:
            v = gg[gg.method == m]
            rows.append({"Regime": reg, "h²": h2, "QTL": int(nq), "Method": m, "Replicates×genotype sets": len(v),
                         "Coverage": mean_sd(v.coverage), "Cond. error": mean_sd(v.cond_err),
                         "Worst-quintile cov.": mean_sd(v.worst_bin_cov), "Width": mean_sd(v.width)})
    write(pd.DataFrame(rows), "Table6_simulation")


def table_runtime():
    t = pd.read_csv(RESULTS_DIR / "timings.csv")
    f = t[t.alpha.isna() & (t.tag == "main") & (t.regime == "R1")].copy()
    ti = t[t.alpha.notna() & (t.tag == "main") & (t.regime == "R1") & (t.alpha == 0.10)]
    f["pools"] = f.t_pool_rand + f.t_pool_clus
    rows = []
    for (b, ds), g in f.groupby(["base", "dataset"]):
        gi = ti[(ti.base == b) & (ti.dataset == ds)]
        rows.append({"Base": b, "Dataset": COMMON[ds], "n train": round(g.n_train.mean()),
                     "Single fit (s)": g.t_outer_fit.mean(), "Random-fold pool (s)": g.t_pool_rand.mean(),
                     "Cluster-fold pool (s)": g.t_pool_clus.mean(), "Split-conformal refit (s)": g.t_scp.mean(),
                     "All interval computations, α=0.10 (s)": gi.t_interval_all_methods.mean(),
                     "KinCP overhead vs single fit (×)": (g.pools.mean()) / max(g.t_outer_fit.mean(), 1e-9)})
    write(pd.DataFrame(rows), "Table7_runtime", 3)


def table_sens(s):
    var = ["KinCP[h=0.25]", "KinCP", "KinCP[h=1.0]", "KinCP[h=2.0]", "KinCP[fixed-h]", "KinCP[nmin=25]", "KinCP[nmin=100]"]
    rows = []
    for reg in ["R1", "R2"]:
        g = s[(s.tag == "main") & (s.base == "GBLUP") & (s.regime == reg) & (s.alpha == 0.10)]
        for v in var:
            x = g[g.method == v]
            rows.append({"Regime": reg, "Variant": v, "Coverage": mean_sd(x.coverage), "Cond. error": mean_sd(x.cond_err),
                         "Width": mean_sd(x.width), "Share infinite": float(x.frac_inf.mean())})
    for reg in ["R1", "R2"]:
        for a in [0.05, 0.10, 0.20]:
            g = s[(s.tag == "main") & (s.base == "GBLUP") & (s.regime == reg) & (s.alpha == a)]
            for m in ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]:
                x = g[g.method == m]
                rows.append({"Regime": reg, "Variant": f"{m} @ 1−α={1 - a:.2f}", "Coverage": mean_sd(x.coverage),
                             "Cond. error": mean_sd(x.cond_err), "Width": mean_sd(x.width), "Share infinite": float(x.frac_inf.mean())})
    write(pd.DataFrame(rows), "Table8_sensitivity")


def table_dedup(s):
    rows = []
    for reg in ["R1", "R2"]:
        for tag in ["main", "dedup"]:
            g = s[(s.tag == tag) & (s.base == "GBLUP") & (s.regime == reg) & (s.alpha == 0.10)]
            if tag == "main":
                g = g[g.job_id.str.endswith("12345")]
            for m in ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]:
                x = g[g.method == m]
                rows.append({"Regime": reg, "Data": "all individuals" if tag == "main" else "near-duplicates removed",
                             "Method": m, "Units": len(x), "Coverage": mean_sd(x.coverage), "Cond. error": mean_sd(x.cond_err),
                             "Width": mean_sd(x.width)})
    write(pd.DataFrame(rows), "TableS_dedup")


def table_units(s):
    g = s[(s.tag == "main") & (s.alpha == 0.10)]
    cols = ["base", "regime", "dataset", "trait", "method", "n", "coverage", "cov_sd_reps", "cond_err", "worst_bin_cov",
            "width", "iscore", "frac_inf"] + [f"cov_b{i}" for i in range(1, 6)]
    write(g[cols].sort_values(["base", "regime", "dataset", "trait", "method"]), "TableS_all_units", 4)


def table_decision():
    p = RESULTS_DIR / "decision_summary.json"
    if not p.exists():
        return
    d = json.load(open(p))
    rows = [dict(Regime=k.split("|")[0], Method=k.split("|")[1], **v) for k, v in d.items()]
    write(pd.DataFrame(rows), "Table9_selection", 3)


def main():
    s = pd.read_csv(RESULTS_DIR / "raw_results.csv")
    table1()
    summary_table(s, BASELINES, "Table2_main_GBLUP")
    table_stats()
    summary_table(s, ABL, "Table4_ablation", namemap=ABL_NAME)
    table_bases(s)
    table_sim(s)
    table_runtime()
    table_sens(s)
    table_dedup(s)
    table_units(s)
    table_decision()


if __name__ == "__main__":
    main()
