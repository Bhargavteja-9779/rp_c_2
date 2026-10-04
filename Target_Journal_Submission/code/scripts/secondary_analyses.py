"""Secondary analyses computed from per-individual records (alpha = 0.10):
E8 error analysis (which units/strata fail and why) and E9 selection-decision analysis.

Writes results/error_analysis_units.csv, results/error_analysis.json,
       results/decision_analysis.csv, results/decision_summary.json
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.data.easygese import read_phenotypes  # noqa: E402
from kincp.utils import RESULTS_DIR, dump_json  # noqa: E402

JOBS = RESULTS_DIR / "jobs"
MAIN = ["Gauss-PEV", "SCP", "CV+", "CalPred-style", "KinCP", "KinCP-ABC"]
SEL_FRAC = 0.10


def unit_traits():
    s = pd.read_csv(RESULTS_DIR / "raw_results.csv")
    t = pd.read_csv(RESULTS_DIR / "timings.csv")
    t = t[t["alpha"].isna() & (t["tag"] == "main") & (t["base"] == "GBLUP")]
    agg = t.groupby(["dataset", "trait", "regime"]).agg(h2_reml=("h2_reml", "mean"), r_pred=("r_pred", "mean"),
                                                         n_train=("n_train", "mean")).reset_index()
    rows = []
    for (ds, tr), _ in agg.groupby(["dataset", "trait"]):
        y = read_phenotypes(ds)[tr].dropna()
        rows.append(dict(dataset=ds, trait=tr, skew=float(stats.skew(y)), exkurt=float(stats.kurtosis(y)),
                         n_unique_frac=float(y.nunique() / len(y))))
    tr = pd.DataFrame(rows)
    s = s[(s.tag == "main") & (s.base == "GBLUP") & (s.alpha == 0.10) & s.method.isin(MAIN)]
    m = s.merge(agg, on=["dataset", "trait", "regime"]).merge(tr, on=["dataset", "trait"])
    return m


def error_analysis():
    m = unit_traits()
    m.to_csv(RESULTS_DIR / "error_analysis_units.csv", index=False)
    out = {}
    for reg in ["R1", "R2"]:
        for meth in MAIN:
            g = m[(m.regime == reg) & (m.method == meth)]
            res = {}
            for cov in ["skew", "exkurt", "h2_reml", "r_pred", "n_train"]:
                x = g[cov].abs() if cov == "skew" else g[cov]
                rho, p = stats.spearmanr(x, g["cond_err"])
                res[cov] = dict(spearman_rho=float(rho), p_value=float(p), n=int(len(g)))
            res["coverage_signed_vs_exkurt"] = dict(zip(["rho", "p"], map(float, stats.spearmanr(g["exkurt"], g["coverage"]))))
            res["worst_units"] = g.nlargest(3, "cond_err")[["dataset", "trait", "coverage", "cond_err", "worst_bin_cov"]].to_dict("records")
            out[f"{reg}|{meth}"] = res
    dump_json(out, RESULTS_DIR / "error_analysis.json")


def decision_analysis():
    rows = []
    for f in sorted(JOBS.glob("GBLUP__*__main__12345__records.parquet")):
        parts = f.name.split("__")
        ds, tr, reg = parts[1], parts[2], parts[3]
        if reg not in ("R1", "R2"):
            continue
        r = pd.read_parquet(f)
        r = r[r.method.isin(MAIN)]
        for (meth, rep, fold), g in r.groupby(["method", "rep", "fold"]):
            k = max(1, int(round(SEL_FRAC * len(g))))
            by_point = g.nlargest(k, "yhat")
            by_lower = g.nlargest(k, "lo")
            cov_sel = ((by_point.y >= by_point.lo) & (by_point.y <= by_point.hi)).mean()
            below_lo = (by_point.y < by_point.lo).mean()
            rows.append(dict(dataset=ds, trait=tr, regime=reg, method=meth, rep=rep, fold=fold, k=k,
                             sel_coverage=cov_sel, sel_below_lower=below_lo,
                             gain_point=by_point.y.mean(), gain_lower=by_lower.y.mean(),
                             overlap=len(set(by_point.idx) & set(by_lower.idx)) / k))
    d = pd.DataFrame(rows)
    d.to_csv(RESULTS_DIR / "decision_analysis.csv", index=False)
    u = d.groupby(["regime", "method", "dataset", "trait"]).mean(numeric_only=True).reset_index()
    summ = {}
    for (reg, meth), g in u.groupby(["regime", "method"]):
        diff = (g["gain_lower"] - g["gain_point"]).to_numpy()
        p = float(stats.wilcoxon(diff).pvalue) if np.any(diff != 0) and len(diff) >= 5 else np.nan
        summ[f"{reg}|{meth}"] = dict(n_units=len(g), median_sel_coverage=float(g.sel_coverage.median()),
                                     median_sel_below_lower=float(g.sel_below_lower.median()),
                                     median_gain_point=float(g.gain_point.median()),
                                     median_gain_lower=float(g.gain_lower.median()),
                                     median_gain_diff=float(np.median(diff)), wilcoxon_p=p,
                                     median_overlap=float(g.overlap.median()))
    dump_json(summ, RESULTS_DIR / "decision_summary.json")


def pev_calibration():
    """Simulation diagnostic (Reviewer 1, M1): is d a calibrated measure of the *genetic* prediction error?
    On the standardised scale y* = (y - mu)/sd, E[y*|g] = g* = (g - mu)/sd, so the GBLUP prediction yhat
    (mu-hat + g-hat) predicts g* with error variance s2g*d (Eq. 1, universal-kriging form).
    We compare the realised mean squared error (g* - yhat)^2 with mean s2g*d by quintile of d."""
    rows = []
    t = pd.read_csv(RESULTS_DIR / "timings.csv")
    t = t[t.alpha.isna() & (t.tag == "sim")][["dataset", "trait", "regime", "rep", "fold", "s2g"]]
    for f in sorted(JOBS.glob("sim__*__records.parquet")):
        r = pd.read_parquet(f)
        r = r[r.method == "Gauss-PEV"].drop(columns=["base", "tag"], errors="ignore")
        r = r.merge(t, on=["dataset", "trait", "regime", "rep", "fold"], how="inner")
        if r.empty:
            continue
        r["sq"] = (r["g_true"] - r["ghat"]) ** 2
        r["pev"] = r["s2g"] * r["d"]
        r["bin"] = pd.qcut(r["d"], 5, labels=False, duplicates="drop")
        h2, nq = r.trait.iloc[0].split("_")[1:]
        for b, gb in r.groupby("bin"):
            rows.append(dict(genotypes=r.dataset.iloc[0], h2=float(h2[1:]), n_qtl=int(nq[1:]),
                             regime=r.regime.iloc[0], rep=int(r.rep.iloc[0]), bin=int(b) + 1,
                             mse=float(gb.sq.mean()), mean_pev=float(gb.pev.mean())))
    d = pd.DataFrame(rows)
    d.to_csv(RESULTS_DIR / "pev_calibration.csv", index=False)
    if len(d):
        d["ratio"] = d.mse / d.mean_pev
        summ = d.groupby(["regime", "bin"]).ratio.median().unstack()
        out = {reg: {f"Q{int(b)}": float(v) for b, v in row.items()} for reg, row in summ.iterrows()}
        out["n_analyses"] = int(d.groupby(["genotypes", "h2", "n_qtl", "regime", "rep"]).ngroups)
        dump_json(out, RESULTS_DIR / "pev_calibration_summary.json")


def alt_relatedness_endpoint():
    """Reviewer 3 (S1): conditional coverage error on quintiles of an *independent* relatedness measure
    that KinCP does not use: the maximum standardised genomic relationship to the training set (maxkin).
    Paired Wilcoxon tests (KinCP vs competitors), Holm within regime family."""
    from kincp.statistics.tests import holm, paired_compare
    rows = []
    meths = ["Gauss-PEV", "Gauss-homosc", "SCP", "NormCP", "CV+", "CalPred-style", "CalPred-style(rand)", "KinCP", "KinCP-ABC"]
    for f in sorted(JOBS.glob("*__main__*__records.parquet")):
        parts = f.name.split("__")
        base, ds, tr, reg = parts[0], parts[1], parts[2], parts[3]
        r = pd.read_parquet(f, columns=["method", "y", "lo", "hi", "maxkin", "rep", "fold", "idx"])
        r = r[r.method.isin(meths)]
        ref = r.drop_duplicates(["rep", "fold", "idx"])["maxkin"]
        edges = np.unique(np.quantile(ref, np.linspace(0, 1, 6)))[1:-1]
        r["bin"] = np.digitize(r["maxkin"], edges)
        r["cov"] = (r.y >= r.lo) & (r.y <= r.hi)
        for m, g in r.groupby("method"):
            bc = g.groupby("bin")["cov"].mean()
            rows.append(dict(base=base, dataset=ds, trait=tr, regime=reg, method=m,
                             cond_err_maxkin=float(np.mean(np.abs(bc.values - 0.9))),
                             worst_maxkin=float(bc.min()), cov_low_kin=float(bc.iloc[0]), cov_high_kin=float(bc.iloc[-1])))
    d = pd.DataFrame(rows)
    d.to_csv(RESULTS_DIR / "alt_relatedness_units.csv", index=False)
    st = []
    for (base, reg), g in d.groupby(["base", "regime"]):
        c = paired_compare(g, ["dataset", "trait"], "method", "KinCP", [m for m in meths if m != "KinCP"], "cond_err_maxkin", True)
        c["base"], c["regime"] = base, reg
        st.append(c)
    st = pd.concat(st, ignore_index=True)
    st["p_holm"] = np.nan
    for _, g in st.groupby("base"):
        ok = g.p_value.notna()
        st.loc[g.index[ok], "p_holm"] = holm(g.loc[ok, "p_value"].to_numpy())
    st.to_csv(RESULTS_DIR / "alt_relatedness_statistics.csv", index=False)
    means = d.groupby(["base", "regime", "method"])[["cond_err_maxkin", "worst_maxkin", "cov_low_kin", "cov_high_kin"]].mean()
    dump_json({f"{b}|{r}|{m}": v.to_dict() for (b, r, m), v in means.iterrows()}, RESULTS_DIR / "alt_relatedness_summary.json")


if __name__ == "__main__":
    alt_relatedness_endpoint()
    error_analysis()
    decision_analysis()
    pev_calibration()
