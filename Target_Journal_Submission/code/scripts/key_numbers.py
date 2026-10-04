"""Derive every number quoted in the manuscript text from the machine-generated results.

Writes results/key_numbers.json: {token: formatted string}. The manuscript builder refuses to run
if a {{token}} in the text is not defined here, so no number can be typed by hand.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.utils import RESULTS_DIR, dump_json  # noqa: E402

K = {}


def f3(x):
    return f"{x:.3f}"


def f2(x):
    return f"{x:.2f}"


def pfmt(p):
    if not np.isfinite(p):
        return "NA"
    return "< 0.001" if p < 0.001 else f"= {p:.3f}"


def main():
    s = pd.read_csv(RESULTS_DIR / "raw_results.csv")
    st = pd.read_csv(RESULTS_DIR / "statistics_table.csv")
    tim = pd.read_csv(RESULTS_DIR / "timings.csv")
    audit = json.load(open(RESULTS_DIR / "data_audit.json"))
    dec = json.load(open(RESULTS_DIR / "decision_summary.json"))
    err = json.load(open(RESULTS_DIR / "error_analysis.json"))
    main_ = s[(s.tag == "main") & (s.alpha == 0.10)]
    g = main_[main_.base == "GBLUP"]
    units = g[["dataset", "trait"]].drop_duplicates()
    K["n_units"] = str(len(units))
    K["n_individuals_min"] = f"{min(r['n'] for r in audit):,}"
    K["n_individuals_max"] = f"{max(r['n'] for r in audit):,}"
    K["n_markers_min"] = f"{min(r['summary']['m_polymorphic'] for r in audit):,}"
    K["n_markers_max"] = f"{max(r['summary']['m_polymorphic'] for r in audit):,}"
    K["n_jobs"] = str(s.job_id.nunique())
    # per regime x method means (GBLUP)
    meths = {"KinCP": "kincp", "Gauss-PEV": "pev", "SCP": "scp", "CV+": "cvp", "CalPred-style": "calp",
             "CalPred-style(rand)": "calpr", "NormCP": "normcp", "Gauss-homosc": "homo", "KinCP-ABC": "oof",
             "KinCP-A": "abA", "KinCP-B": "abB", "KinCP-C": "abC", "KinCP-AB": "abAB", "KinCP-AC": "abAC", "KinCP-BC": "abBC"}
    for reg in ["R1", "R2", "R3"]:
        for m, tok in meths.items():
            v = g[(g.regime == reg) & (g.method == m)]
            if v.empty:
                continue
            K[f"{tok}_{reg}_cov"] = f3(v.coverage.mean())
            K[f"{tok}_{reg}_covsd"] = f3(v.coverage.std(ddof=1))
            K[f"{tok}_{reg}_covmin"] = f3(v.coverage.min())
            K[f"{tok}_{reg}_cond"] = f3(v.cond_err.mean())
            K[f"{tok}_{reg}_worst"] = f3(v.worst_bin_cov.mean())
            K[f"{tok}_{reg}_width"] = f2(v.width.mean())
            K[f"{tok}_{reg}_is"] = f2(v.iscore.mean())
            K[f"{tok}_{reg}_q1"] = f3(v.cov_b1.mean())
            K[f"{tok}_{reg}_q5"] = f3(v.cov_b5.mean())
            K[f"{tok}_{reg}_nbelow85"] = str(int((v.coverage < 0.85).sum()))
    K["null_cond"] = f3(g.null_cond_err.mean())
    K["null_worst"] = f3(g.null_worst_bin_cov.mean())
    # statistics (GBLUP, baseline family)
    sb = st[(st.base == "GBLUP")]
    for reg in ["R1", "R2", "R3"]:
        for ep, e in [("cond_err", "cond"), ("cov_dev", "dev"), ("iscore", "is")]:
            for comp, tok in meths.items():
                r = sb[(sb.regime == reg) & (sb.endpoint == ep) & (sb.competitor == comp)]
                if r.empty:
                    continue
                r = r.iloc[0]
                K[f"st_{tok}_{reg}_{e}_d"] = f3(r.median_diff)
                K[f"st_{tok}_{reg}_{e}_ci"] = f"{r.ci_low:.3f} to {r.ci_high:.3f}"
                K[f"st_{tok}_{reg}_{e}_p"] = pfmt(r.p_holm)
                K[f"st_{tok}_{reg}_{e}_rb"] = f2(r.rank_biserial)
                K[f"st_{tok}_{reg}_{e}_wins"] = f"{int(r.wins_ref)}/{int(r.n_units)}"
    # other bases
    for b, bt in [("RKHS", "rk"), ("LightGBM", "lg")]:
        gb = main_[main_.base == b]
        K[f"{bt}_n_units"] = str(gb[["dataset", "trait"]].drop_duplicates().shape[0])
        for reg in ["R1", "R2"]:
            for m, tok in [("KinCP", "kincp"), ("SCP", "scp"), ("CV+", "cvp"), ("CalPred-style", "calp")]:
                v = gb[(gb.regime == reg) & (gb.method == m)]
                if v.empty:
                    continue
                K[f"{bt}_{tok}_{reg}_cov"] = f3(v.coverage.mean())
                K[f"{bt}_{tok}_{reg}_cond"] = f3(v.cond_err.mean())
                K[f"{bt}_{tok}_{reg}_worst"] = f3(v.worst_bin_cov.mean())
            r = st[(st.base == b) & (st.regime == reg) & (st.endpoint == "cond_err") & (st.competitor == "CV+")]
            if len(r):
                K[f"st_{bt}_cvp_{reg}_cond_p"] = pfmt(r.iloc[0].p_holm)
                K[f"st_{bt}_cvp_{reg}_cond_d"] = f3(r.iloc[0].median_diff)
            r = st[(st.base == b) & (st.regime == reg) & (st.endpoint == "cond_err") & (st.competitor == "CalPred-style")]
            if len(r):
                K[f"st_{bt}_calp_{reg}_cond_p"] = pfmt(r.iloc[0].p_holm)
                K[f"st_{bt}_calp_{reg}_cond_d"] = f3(r.iloc[0].median_diff)
    # simulation
    sim = s[(s.tag == "sim") & (s.alpha == 0.10)]
    for reg in ["R1", "R2"]:
        for m, tok in [("KinCP", "kincp"), ("SCP", "scp"), ("CV+", "cvp"), ("Gauss-PEV", "pev"), ("CalPred-style", "calp")]:
            v = sim[(sim.regime == reg) & (sim.method == m)]
            if v.empty:
                continue
            K[f"sim_{tok}_{reg}_cov"] = f3(v.coverage.mean())
            K[f"sim_{tok}_{reg}_worst"] = f3(v.worst_bin_cov.mean())
            K[f"sim_{tok}_{reg}_cond"] = f3(v.cond_err.mean())
            K[f"sim_{tok}_{reg}_covmin"] = f3(v.coverage.min())
    K["sim_n_runs"] = str(sim[sim.method == "KinCP"].shape[0])
    # dedup
    dd = s[(s.tag == "dedup") & (s.alpha == 0.10)]
    for reg in ["R1", "R2"]:
        for m, tok in [("KinCP", "kincp"), ("SCP", "scp"), ("CV+", "cvp"), ("Gauss-PEV", "pev")]:
            v = dd[(dd.regime == reg) & (dd.method == m)]
            if len(v):
                K[f"dd_{tok}_{reg}_cov"] = f3(v.coverage.mean())
                K[f"dd_{tok}_{reg}_cond"] = f3(v.cond_err.mean())
    K["dup_pairs_barley"] = f"{next(r for r in audit if r['dataset'] == 'barley')['near_dup_pairs_gt095']:,}"
    K["dup_pairs_soybean"] = f"{next(r for r in audit if r['dataset'] == 'soybean')['near_dup_pairs_gt095']:,}"
    K["dup_pairs_lentil"] = f"{next(r for r in audit if r['dataset'] == 'lentil')['near_dup_pairs_gt095']:,}"
    # sensitivity
    for reg in ["R1", "R2"]:
        for v_, tok in [("KinCP[h=0.25]", "h025"), ("KinCP[h=1.0]", "h1"), ("KinCP[h=2.0]", "h2"),
                        ("KinCP[fixed-h]", "fixed"), ("KinCP[nmin=25]", "n25"), ("KinCP[nmin=100]", "n100")]:
            v = g[(g.regime == reg) & (g.method == v_)]
            K[f"sens_{tok}_{reg}_cond"] = f3(v.cond_err.mean())
            K[f"sens_{tok}_{reg}_inf"] = f3(v.frac_inf.mean())
        for a in [0.05, 0.20]:
            v = s[(s.tag == "main") & (s.base == "GBLUP") & (s.regime == reg) & (s.alpha == a) & (s.method == "KinCP")]
            K[f"kincp_{reg}_cov_a{int(a * 100):02d}"] = f3(v.coverage.mean())
            v = s[(s.tag == "main") & (s.base == "GBLUP") & (s.regime == reg) & (s.alpha == a) & (s.method == "CV+")]
            K[f"cvp_{reg}_cov_a{int(a * 100):02d}"] = f3(v.coverage.mean())
    # runtime
    t = tim[tim.alpha.isna() & (tim.tag == "main") & (tim.regime == "R1")].copy()
    t["ratio"] = (t.t_pool_rand + t.t_pool_clus) / t.t_outer_fit
    for b, bt in [("GBLUP", "gb"), ("RKHS", "rk"), ("LightGBM", "lg")]:
        tb = t[t.base == b]
        if len(tb):
            K[f"rt_{bt}_ratio_med"] = f"{tb.ratio.median():.1f}"
            K[f"rt_{bt}_pool_max"] = f"{(tb.t_pool_rand + tb.t_pool_clus).max():.1f}"
    ti = tim[tim.alpha.notna() & (tim.alpha == 0.10) & (tim.tag == "main")]
    K["rt_interval_max"] = f"{ti.t_interval_all_methods.max():.2f}"
    tm = t[(t.base == "GBLUP") & (t.dataset == "maize")]
    if len(tm):
        K["rt_maize_fit"] = f"{tm.t_outer_fit.mean():.1f}"
        K["rt_maize_pool"] = f"{(tm.t_pool_rand + tm.t_pool_clus).mean():.1f}"
    # REML / predictive ability context
    tg = tim[tim.alpha.isna() & (tim.tag == "main") & (tim.base == "GBLUP") & (tim.regime == "R1")]
    pa = tg.groupby(["dataset", "trait"]).r_pred.mean()
    K["r_min"], K["r_max"], K["r_med"] = f2(pa.min()), f2(pa.max()), f2(pa.median())
    tg2 = tim[tim.alpha.isna() & (tim.tag == "main") & (tim.base == "GBLUP") & (tim.regime == "R2")]
    pa2 = tg2.groupby(["dataset", "trait"]).r_pred.mean()
    K["r2_med"] = f2(pa2.median())
    # decision analysis
    for reg in ["R1", "R2"]:
        for m, tok in [("KinCP", "kincp"), ("SCP", "scp"), ("CV+", "cvp"), ("Gauss-PEV", "pev"), ("CalPred-style", "calp")]:
            d = dec.get(f"{reg}|{m}")
            if d:
                K[f"sel_{tok}_{reg}_cov"] = f3(d["median_sel_coverage"])
                K[f"sel_{tok}_{reg}_below"] = f3(d["median_sel_below_lower"])
                K[f"sel_{tok}_{reg}_gaindiff"] = f3(d["median_gain_diff"])
                K[f"sel_{tok}_{reg}_gainp"] = pfmt(d["wilcoxon_p"])
                K[f"sel_{tok}_{reg}_overlap"] = f2(d["median_overlap"])
    # error analysis correlations
    for reg in ["R2", "R1"]:
        for m, tok in [("KinCP", "kincp"), ("Gauss-PEV", "pev")]:
            e = err[f"{reg}|{m}"]
            K[f"err_{tok}_{reg}_kurt_rho"] = f2(e["coverage_signed_vs_exkurt"]["rho"])
            K[f"err_{tok}_{reg}_kurt_p"] = pfmt(e["coverage_signed_vs_exkurt"]["p"])
            K[f"err_{tok}_{reg}_r_rho"] = f2(e["r_pred"]["spearman_rho"])
            K[f"err_{tok}_{reg}_r_p"] = pfmt(e["r_pred"]["p_value"])
            K[f"err_{tok}_{reg}_h2_rho"] = f2(e["h2_reml"]["spearman_rho"])
            K[f"err_{tok}_{reg}_h2_p"] = pfmt(e["h2_reml"]["p_value"])
            w = e["worst_units"][0]
            K[f"err_{tok}_{reg}_worst_unit"] = f"{w['dataset']} {w['trait']}".replace("_", " ")
            K[f"err_{tok}_{reg}_worst_cov"] = f3(w["coverage"])
    # per-unit extremes used in the text
    for reg in ["R1", "R2"]:
        for m, tok in [("Gauss-PEV", "pev"), ("KinCP", "kincp"), ("CV+", "cvp"), ("SCP", "scp")]:
            v = g[(g.regime == reg) & (g.method == m)].sort_values("coverage")
            K[f"{tok}_{reg}_minunit"] = f"{v.iloc[0].dataset} {v.iloc[0].trait}".replace("_", " ")
    # exploratory KinCP-G (Phase 19, D6)
    ex = s[(s.tag == "explore") & (s.alpha == 0.10)]
    for reg in ["R1", "R2"]:
        for m, tok in [("KinCP", "kincp"), ("KinCP-G", "kincpg"), ("KinCP-G+", "kincpgp"), ("CalPred-style-G", "calpg"), ("Mondrian-d", "mondrian")]:
            v = ex[(ex.regime == reg) & (ex.method == m)]
            if len(v):
                K[f"ex_{tok}_{reg}_cov"] = f3(v.coverage.mean())
                K[f"ex_{tok}_{reg}_cond"] = f3(v.cond_err.mean())
                K[f"ex_{tok}_{reg}_worst"] = f3(v.worst_bin_cov.mean())
                K[f"ex_{tok}_{reg}_width"] = f2(v.width.mean())
    # PEV calibration diagnostic (simulation) and species-level tests (Reviewer 1)
    pc = RESULTS_DIR / "pev_calibration_summary.json"
    if pc.exists():
        pcj = json.load(open(pc))
        for reg in ["R1", "R2"]:
            vals = list(pcj[reg].values())
            K[f"pevcal_{reg}_min"], K[f"pevcal_{reg}_max"] = f2(min(vals)), f2(max(vals))
    sp = pd.read_csv(RESULTS_DIR / "statistics_species.csv")
    for reg in ["R1", "R2", "R3"]:
        for comp, tok in meths.items():
            r = sp[(sp.regime == reg) & (sp.endpoint == "cond_err") & (sp.competitor == comp)]
            if len(r):
                K[f"sp_{tok}_{reg}_cond_wins"] = f"{int(r.iloc[0].wins_ref)}/{int(r.iloc[0].n_units)}"
                K[f"sp_{tok}_{reg}_cond_praw"] = pfmt(r.iloc[0].p_value)
                K[f"sp_{tok}_{reg}_cond_p"] = pfmt(r.iloc[0].p_holm)
    # independent relatedness endpoint (Reviewer 3, S1)
    ar = RESULTS_DIR / "alt_relatedness_summary.json"
    if ar.exists():
        arj = json.load(open(ar))
        ast = pd.read_csv(RESULTS_DIR / "alt_relatedness_statistics.csv")
        for reg in ["R1", "R2", "R3"]:
            for m, tok in [("KinCP", "kincp"), ("Gauss-PEV", "pev"), ("CV+", "cvp"), ("SCP", "scp"), ("CalPred-style", "calp"), ("NormCP", "normcp")]:
                v = arj.get(f"GBLUP|{reg}|{m}")
                if v:
                    K[f"mk_{tok}_{reg}_cond"] = f3(v["cond_err_maxkin"])
                    K[f"mk_{tok}_{reg}_high"] = f3(v["cov_high_kin"])
                    K[f"mk_{tok}_{reg}_low"] = f3(v["cov_low_kin"])
                r = ast[(ast.base == "GBLUP") & (ast.regime == reg) & (ast.competitor == m)]
                if len(r):
                    K[f"mk_st_{tok}_{reg}_p"] = pfmt(r.iloc[0].p_holm)
                    K[f"mk_st_{tok}_{reg}_wins"] = f"{int(r.iloc[0].wins_ref)}/{int(r.iloc[0].n_units)}"
        r1 = ast[(ast.base == "GBLUP") & (ast.regime == "R1") & ast.competitor.isin(["Gauss-PEV", "Gauss-homosc", "SCP", "NormCP", "CV+", "CalPred-style", "CalPred-style(rand)"])]
        K["mk_st_cvp_R1_p_num"] = f2(r1.p_holm.min())
    t_all = tim[tim.alpha.isna() & (tim.tag == "main") & (tim.base == "GBLUP")]
    K["n_folds_r2_pine"] = str(int(t_all[(t_all.dataset == "pine") & (t_all.regime == "R2")].groupby("trait").size().iloc[0]))
    # granularity (k = 3, 10) and real families (Reviewer 5)
    for tag, regs in [("granularity", ["R2k3", "R2k10"]), ("families", ["R2fam"])]:
        gg = s[(s.tag == tag) & (s.alpha == 0.10)]
        for reg in regs:
            for m, tok in [("KinCP", "kincp"), ("CV+", "cvp"), ("SCP", "scp"), ("Gauss-PEV", "pev"), ("CalPred-style", "calp")]:
                v = gg[(gg.regime == reg) & (gg.method == m)]
                if len(v):
                    K[f"gr_{tok}_{reg}_cov"] = f3(v.coverage.mean())
                    K[f"gr_{tok}_{reg}_cond"] = f3(v.cond_err.mean())
                    K[f"gr_{tok}_{reg}_worst"] = f3(v.worst_bin_cov.mean())
        if tag == "granularity":
            from scipy import stats as _st
            for reg in regs:
                w = gg[gg.regime == reg].pivot_table(index=["dataset", "trait"], columns="method", values="cond_err")
                for comp, tok in [("CV+", "cvp"), ("Gauss-PEV", "pev"), ("CalPred-style", "calp")]:
                    dlt = (w[comp] - w["KinCP"]).dropna()
                    K[f"gr_st_{tok}_{reg}_wins"] = f"{int((dlt > 0).sum())}/{len(dlt)}"
                    K[f"gr_st_{tok}_{reg}_p"] = pfmt(float(_st.wilcoxon(dlt).pvalue))
    # scaling benchmark (Reviewer 6)
    sc_p = RESULTS_DIR / "scaling.csv"
    if sc_p.exists():
        sc = pd.read_csv(sc_p).groupby("n_train").mean(numeric_only=True)
        big = sc.loc[sc.index.max()]
        K["sc_n_max"] = f"{int(sc.index.max()):,}"
        K["sc_fit"] = f"{big.t_fit:.1f}"
        K["sc_pools"] = f"{big.t_pool_rand + big.t_pool_clus:.1f}"
        K["sc_int"] = f"{big.t_intervals:.2f}"
        K["sc_mem"] = f"{big.peak_mem_mb:.0f}"
        slope = np.polyfit(np.log(sc.index.values), np.log((sc.t_pool_rand + sc.t_pool_clus).values), 1)[0]
        K["sc_slope"] = f"{slope:.1f}"
        mslope = np.polyfit(np.log(sc.index.values), np.log(sc.peak_mem_mb.values), 1)[0]
        K["sc_mslope"] = f"{mslope:.1f}"
    # narrative numbers file can be extended by text tokens defined in manuscript/src/text_tokens.json
    tt = Path(__file__).resolve().parents[2] / "manuscript" / "src" / "text_tokens.json"
    if tt.exists():
        templ = json.load(open(tt))
        for k, v in templ.items():
            try:
                K[k] = v.format(**K) if isinstance(v, str) else v
            except KeyError as e:
                print("WARNING: text token", k, "needs", e)
                K[k] = f"[PENDING: {k}]"
    dump_json(K, RESULTS_DIR / "key_numbers.json")
    print(len(K), "numbers written")


if __name__ == "__main__":
    main()
