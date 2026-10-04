"""Publication figures, generated only from machine-readable result files.

Output: figures/Fig*.pdf (vector, for GENETICS submission) and figures/Fig*.png (600 dpi, for the DOCX).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kincp.data.easygese import COMMON  # noqa: E402
from kincp.utils import FIG_DIR, RESULTS_DIR  # noqa: E402

# validated categorical palette (dataviz reference instance, light mode); fixed method -> colour mapping
COL = {"KinCP": "#2a78d6", "Gauss-PEV": "#eb6834", "CalPred-style": "#1baf7a", "CV+": "#eda100",
       "SCP": "#e87ba4", "NormCP": "#008300", "Gauss-homosc": "#4a3aa7", "CalPred-style(rand)": "#e34948",
       "KinCP-ABC": "#e34948"}
MRK = {"KinCP": "o", "Gauss-PEV": "s", "CalPred-style": "D", "CV+": "^", "SCP": "v", "NormCP": "P",
       "Gauss-homosc": "X", "CalPred-style(rand)": "*", "KinCP-ABC": "*"}
LABEL = {"KinCP-ABC": "OOF-quantile (PredInterval-like)", "CalPred-style": "CalPred-style (pool A)",
         "CalPred-style(rand)": "CalPred-style (random pool)"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
REG = {"R1": "R1 random CV", "R2": "R2 cluster-out", "R3": "R3 random CV, 50% training"}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
                     "lines.linewidth": 1.6, "pdf.fonttype": 42})


def save(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{name}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def lab(m):
    return LABEL.get(m, m)


def load():
    s = pd.read_csv(RESULTS_DIR / "raw_results.csv")
    return s


def boot_ci(x, n=2000, seed=1):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    b = rng.choice(x, (n, len(x))).mean(1)
    return np.quantile(b, 0.025), np.quantile(b, 0.975)


# ---------------------------------------------------------------- Fig 1: method schematic
def fig1():
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    ax.set_xlim(-2, 100)
    ax.set_ylim(2, 46)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#f3f2ee", ec=INK2, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=0.8))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.3, color=INK,
                fontweight="bold" if bold else "normal")

    def arrow(x0, y0, x1, y1):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=8, color=INK2, lw=0.8))

    box(0, 30, 19, 12, "Genotypes of training\nset T and candidates U\n(GRM, VanRaden)")
    box(0, 12, 19, 12, "Phenotypes of T\n(standardised with\ntraining statistics)")
    box(23, 21, 17, 12, "Outer fit on T\nREML: $\\sigma^2_g,\\sigma^2_e$\nbase predictor $\\hat y$")
    box(45, 33, 22, 10, "(A) random 5-fold\ncross-fitting in T", fc="#e6effa")
    box(45, 21, 22, 10, "(A) genomic-cluster\n5-fold cross-fitting in T", fc="#e6effa")
    box(45, 6, 22, 11, "Relatedness covariate\n$d_j$ = GBLUP PEV$/\\sigma^2_g$\nw.r.t. training subset", fc="#fdf0e9")
    box(72, 27, 26, 15, "(B) normalised scores\n$s_i = |r_i| / \\sqrt{\\sigma^2_g d_i+\\sigma^2_e}$\n(C) kernel weights in $\\log d$\n$w_i(j)=\\exp(-\\Delta^2/2h^2)$", fc="#e6effa")
    box(72, 6, 26, 15, "Interval for candidate j:\n$\\hat{y}_j \\pm \\hat{q}_{1-\\alpha}(d_j)\\,\\sqrt{\\sigma^2_g d_j+\\sigma^2_e}$\nweighted conformal quantile\n(test mass at $+\\infty$)", fc="#dfeee5", bold=False)
    arrow(18, 36, 23, 30)
    arrow(18, 18, 23, 24)
    arrow(40, 29, 45, 37)
    arrow(40, 26, 45, 26)
    arrow(40, 23, 45, 13)
    arrow(67, 38, 72, 36)
    arrow(67, 26, 72, 32)
    arrow(67, 11, 72, 13)
    arrow(85, 27, 85, 21)
    ax.text(56, 44.5, "pool of out-of-fold residuals $(r_i, d_i)$ spanning close and distant relatives", ha="center",
            fontsize=6.5, color=INK2)
    save(fig, "Fig1_KinCP_schematic")


# ---------------------------------------------------------------- Fig 2: data overview
def fig2():
    audit = json.load(open(RESULTS_DIR / "data_audit.json"))
    rec = []
    import secondary_analyses as _sa
    for f in _sa.main_gblup_records():
        p = f.name.split("__")
        if p[3] not in ("R1", "R2"):
            continue
        r = pd.read_parquet(f, columns=["method", "d", "rep", "fold", "idx"])
        r = r[(r.method == "KinCP")]
        rec.append(pd.DataFrame(dict(dataset=p[1], trait=p[2], regime=p[3], d=r.d.values)))
    d = pd.concat(rec)
    first_trait = d.groupby("dataset").trait.first()
    d = d[d.trait == d.dataset.map(first_trait)]
    order = sorted(d.dataset.unique(), key=lambda x: COMMON[x])
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw=dict(width_ratios=[1.0, 1.6]))
    a = {r["dataset"]: r for r in audit}
    names = [COMMON[o] for o in order]
    ns = [a[o]["n"] for o in order]
    ms = [a[o]["summary"]["m_polymorphic"] for o in order]
    y = np.arange(len(order))
    axes[0].barh(y, ns, color=COL["KinCP"], height=0.6)
    for i, (n, m) in enumerate(zip(ns, ms)):
        axes[0].text(n + 60, i, f"n={n:,}; m={m/1000:.0f}k", va="center", fontsize=6.5, color=INK2)
    axes[0].set_yticks(y, names)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("Individuals")
    axes[0].set_xlim(0, max(ns) * 1.75)
    axes[0].set_title("a  Datasets (EasyGeSe)", loc="left", fontsize=8, color=INK)
    pos = 0
    for i, o in enumerate(order):
        for k, reg in enumerate(["R1", "R2"]):
            v = np.log10(d[(d.dataset == o) & (d.regime == reg)].d.values)
            bp = axes[1].boxplot(v, positions=[i + (k - 0.5) * 0.36], widths=0.3, orientation="horizontal", showfliers=False,
                                 patch_artist=True, medianprops=dict(color=INK, lw=1))
            bp["boxes"][0].set(facecolor=[COL["KinCP"], COL["Gauss-PEV"]][k], alpha=0.85, edgecolor=INK2)
    axes[1].set_yticks(y, names)
    axes[1].invert_yaxis()
    axes[1].set_xlabel(r"$\log_{10} d$  (GBLUP PEV of candidates, $\sigma^2_g$ units)")
    axes[1].set_title("b  Relatedness covariate of test candidates", loc="left", fontsize=8, color=INK)
    from matplotlib.patches import Patch
    axes[1].legend(handles=[Patch(fc=COL["KinCP"], label="R1 random CV"), Patch(fc=COL["Gauss-PEV"], label="R2 cluster-out")],
                   loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=6.5)
    axes[0].grid(axis="y", visible=False)
    axes[1].grid(axis="y", visible=False)
    fig.tight_layout()
    save(fig, "Fig2_data_relatedness")


# ---------------------------------------------------------------- Fig 3: conditional coverage
def fig3(s):
    meths = ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]
    g = s[(s.tag == "main") & (s.base == "GBLUP") & (s.alpha == 0.10) & s.method.isin(meths)]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    for ax, reg in zip(axes, ["R1", "R2", "R3"]):
        sub = g[g.regime == reg]
        for m in meths:
            mm = sub[sub.method == m]
            mu = [mm[f"cov_b{b}"].mean() for b in range(1, 6)]
            ci = np.array([boot_ci(mm[f"cov_b{b}"]) for b in range(1, 6)])
            x = np.arange(1, 6) + (meths.index(m) - 2) * 0.06
            ax.errorbar(x, mu, yerr=[np.array(mu) - ci[:, 0], ci[:, 1] - np.array(mu)], color=COL[m], marker=MRK[m],
                        ms=4, capsize=1.5, lw=1.4, elinewidth=0.8, label=lab(m))
        ax.axhline(0.9, color=INK2, lw=0.8, ls="--")
        ax.set_xticks(range(1, 6), ["Q1\nclose", "Q2", "Q3", "Q4", "Q5\ndistant"])
        ax.set_title(REG[reg], fontsize=8, color=INK, loc="left")
        ax.set_xlabel("Quintile of relatedness covariate d")
    axes[0].set_ylabel("Empirical coverage (target 0.90)")
    axes[0].set_ylim(0.76, 0.96)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.08), fontsize=7)
    fig.tight_layout()
    save(fig, "Fig3_conditional_coverage")


# ---------------------------------------------------------------- Fig 4: per-unit coverage
def fig4(s):
    meths = ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]
    g = s[(s.tag == "main") & (s.base == "GBLUP") & (s.alpha == 0.10) & s.method.isin(meths)].copy()
    g["unit"] = g.dataset.map(COMMON) + " · " + g.trait.str.replace("_", " ")
    units = sorted(g.unit.unique())
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 0.17 * len(units) + 1.2), sharey=True)
    for ax, reg in zip(axes, ["R1", "R2"]):
        sub = g[g.regime == reg]
        for m in meths:
            mm = sub[sub.method == m].set_index("unit").reindex(units)
            ax.scatter(mm.coverage, np.arange(len(units)) + (meths.index(m) - 2) * 0.12, s=10, color=COL[m],
                       marker=MRK[m], label=lab(m), zorder=3, edgecolors="white", linewidths=0.3)
        ax.axvline(0.9, color=INK2, lw=0.8, ls="--")
        ax.set_title(REG[reg], fontsize=8, loc="left", color=INK)
        ax.set_xlabel("Marginal coverage")
    axes[0].set_yticks(range(len(units)), units, fontsize=6)
    axes[0].invert_yaxis()
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.03), fontsize=7)
    fig.tight_layout()
    save(fig, "Fig4_unit_coverage")


# ---------------------------------------------------------------- Fig 5: ablation
def fig5(s):
    ab = ["KinCP", "KinCP-A", "KinCP-B", "KinCP-C", "KinCP-AB", "KinCP-AC", "KinCP-BC", "KinCP-ABC"]
    names = ["A+B+C (KinCP)", "B+C", "A+C", "A+B", "C only", "B only", "A only", "none"]
    g = s[(s.tag == "main") & (s.base == "GBLUP") & (s.alpha == 0.10) & s.method.isin(ab)]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=True)
    for ax, reg in zip(axes, ["R1", "R2"]):
        sub = g[g.regime == reg]
        mu = [sub[sub.method == m].cond_err.mean() for m in ab]
        ci = np.array([boot_ci(sub[sub.method == m].cond_err) for m in ab])
        y = np.arange(len(ab))
        ax.barh(y, mu, color=[COL["KinCP"] if m == "KinCP" else "#9fbfe6" for m in ab], height=0.62)
        ax.errorbar(mu, y, xerr=[np.array(mu) - ci[:, 0], ci[:, 1] - np.array(mu)], fmt="none", ecolor=INK2, elinewidth=0.8, capsize=1.5)
        ax.set_yticks(y, names)
        ax.set_title(REG[reg], fontsize=8, loc="left", color=INK)
        ax.set_xlabel("Conditional coverage error (mean over units)")
    axes[0].invert_yaxis()
    fig.tight_layout()
    save(fig, "Fig5_ablation")


# ---------------------------------------------------------------- Fig 6: base predictors / robustness
def fig6(s):
    meths = ["SCP", "CV+", "CalPred-style", "KinCP"]
    g = s[(s.tag == "main") & (s.alpha == 0.10) & s.method.isin(meths) & s.regime.isin(["R1", "R2"])]
    bases = [b for b in ["GBLUP", "RKHS", "LightGBM"] if b in g.base.unique()]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))
    for ax, ep, ttl in zip(axes, ["coverage", "cond_err"], ["a  Marginal coverage", "b  Conditional coverage error"]):
        xt = []
        for bi, b in enumerate(bases):
            for ri, reg in enumerate(["R1", "R2"]):
                x0 = bi * 2.6 + ri * 1.2
                xt.append((x0 + 0.3, f"{b}\n{reg}"))
                for mi, m in enumerate(meths):
                    v = g[(g.base == b) & (g.regime == reg) & (g.method == m)][ep]
                    if v.empty:
                        continue
                    lo, hi = boot_ci(v)
                    ax.errorbar(x0 + mi * 0.2, v.mean(), yerr=[[v.mean() - lo], [hi - v.mean()]], color=COL[m],
                                marker=MRK[m], ms=4, capsize=1.5, elinewidth=0.8, label=lab(m) if (bi == 0 and ri == 0) else None)
        if ep == "coverage":
            ax.axhline(0.9, color=INK2, lw=0.8, ls="--")
        ax.set_xticks([x for x, _ in xt], [t for _, t in xt], fontsize=6.5)
        ax.set_title(ttl, fontsize=8, loc="left", color=INK)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.07), fontsize=7)
    fig.tight_layout()
    save(fig, "Fig6_base_predictors")


# ---------------------------------------------------------------- Fig 7: simulation
def fig7(s):
    meths = ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]
    g = s[(s.tag == "sim") & (s.alpha == 0.10) & s.method.isin(meths)]
    if g.empty:
        return
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=False)
    for ax, ep, ttl in zip(axes, ["worst_bin_cov", "cond_err"], ["a  Worst-quintile coverage", "b  Conditional coverage error"]):
        cats = [(reg, h2) for reg in ["R1", "R2"] for h2 in sorted(g.h2.unique())]
        for m in meths:
            mu, lo, hi = [], [], []
            for reg, h2 in cats:
                v = g[(g.method == m) & (g.regime == reg) & (g.h2 == h2)][ep]
                mu.append(v.mean())
                c = boot_ci(v)
                lo.append(v.mean() - c[0])
                hi.append(c[1] - v.mean())
            x = np.arange(len(cats)) + (meths.index(m) - 2) * 0.08
            ax.errorbar(x, mu, yerr=[lo, hi], color=COL[m], marker=MRK[m], ms=4, lw=1.2, capsize=1.5, elinewidth=0.8, label=lab(m))
        ax.set_xticks(range(len(cats)), [f"{r}\nh²={h}" for r, h in cats], fontsize=6.5)
        if ep == "worst_bin_cov":
            ax.axhline(0.9, color=INK2, lw=0.8, ls="--")
        ax.set_title(ttl, fontsize=8, loc="left", color=INK)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.07), fontsize=7)
    fig.tight_layout()
    save(fig, "Fig7_simulation")


# ---------------------------------------------------------------- Fig 8: efficiency
def fig8():
    sc = pd.read_csv(RESULTS_DIR / "scaling.csv")
    a = sc.groupby("n_train").agg(["mean", "std"])
    n = a.index.values
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))
    for col, lab_, c, m in [("t_fit", "Single GBLUP fit (REML)", COL["Gauss-PEV"], "s"),
                            ("t_pool_rand", "Random-fold pool (5 fits)", COL["CalPred-style"], "D"),
                            ("t_pool_clus", "Cluster-fold pool (5 fits)", COL["CV+"], "^"),
                            ("t_intervals", "KinCP intervals (300 candidates)", COL["KinCP"], "o")]:
        axes[0].errorbar(n, a[(col, "mean")], yerr=a[(col, "std")], color=c, marker=m, ms=4, capsize=1.5, label=lab_)
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Training-set size")
    axes[0].set_ylabel("Wall time (s, 1 CPU thread)")
    axes[0].set_title("a  Time (maize genotypes)", fontsize=8, loc="left", color=INK)
    axes[0].legend(fontsize=6)
    axes[1].errorbar(n, a[("peak_mem_mb", "mean")], yerr=a[("peak_mem_mb", "std")], color=COL["KinCP"], marker="o", ms=4, capsize=1.5)
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("Training-set size")
    axes[1].set_ylabel("Peak traced memory (MB)")
    axes[1].set_title("b  Memory (fit + pools + intervals)", fontsize=8, loc="left", color=INK)
    fig.tight_layout()
    save(fig, "Fig8_runtime")


# ---------------------------------------------------------------- Fig 9: sensitivity
def fig9(s):
    g = s[(s.tag == "main") & (s.base == "GBLUP") & s.regime.isin(["R1", "R2"])]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))
    var = ["KinCP[h=0.25]", "KinCP", "KinCP[h=1.0]", "KinCP[h=2.0]", "KinCP[fixed-h]", "KinCP[nmin=25]", "KinCP[nmin=100]"]
    names = ["h=0.25", "h=0.5 (default)", "h=1", "h=2", "no floor", "n_min=25", "n_min=100"]
    gg = g[g.alpha == 0.10]
    for ri, reg in enumerate(["R1", "R2"]):
        mu = [gg[(gg.regime == reg) & (gg.method == v)].cond_err.mean() for v in var]
        axes[0].plot(range(len(var)), mu, marker="os"[ri], color=[COL["KinCP"], COL["Gauss-PEV"]][ri], label=REG[reg])
    axes[0].set_xticks(range(len(var)), names, rotation=35, ha="right", fontsize=6.5)
    axes[0].set_ylabel("Conditional coverage error")
    axes[0].set_title("a  Localisation bandwidth and floor", fontsize=8, loc="left", color=INK)
    axes[0].legend(fontsize=6.5)
    for m in ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]:
        for ri, reg in enumerate(["R1", "R2"]):
            mm = g[(g.method == m) & (g.regime == reg)].groupby("alpha").coverage.mean()
            axes[1].plot(1 - mm.index, mm.values - (1 - mm.index), marker=MRK[m], color=COL[m], ms=3.5,
                         ls="-" if reg == "R1" else ":", label=f"{lab(m)}" if reg == "R2" else None)
    axes[1].axhline(0, color=INK2, lw=0.8, ls="--")
    axes[1].set_xlabel("Nominal coverage 1−α (solid R1, dotted R2)")
    axes[1].set_ylabel("Coverage − nominal")
    axes[1].set_title("b  Nominal level", fontsize=8, loc="left", color=INK)
    axes[1].legend(fontsize=6, ncol=2)
    fig.tight_layout()
    save(fig, "Fig9_sensitivity")


# ---------------------------------------------------------------- Fig 10: error analysis
def fig10():
    p = RESULTS_DIR / "error_analysis_units.csv"
    if not p.exists():
        return
    m = pd.read_csv(p)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))
    for ax, x, xl in zip(axes, ["exkurt", "r_pred"], ["Excess kurtosis of phenotype", "Predictive ability r (GBLUP)"]):
        for meth in ["Gauss-PEV", "KinCP"]:
            g = m[(m.method == meth) & (m.regime == "R2")]
            ax.scatter(g[x], g["coverage"], color=COL[meth], marker=MRK[meth], s=14, label=lab(meth), edgecolors="white", linewidths=0.3)
        ax.axhline(0.9, color=INK2, lw=0.8, ls="--")
        ax.set_xlabel(xl)
        ax.set_ylabel("Marginal coverage, R2")
    axes[0].legend(fontsize=6.5)
    fig.tight_layout()
    save(fig, "Fig10_error_analysis")


# ---------------------------------------------------------------- Fig 11: decision analysis
def fig11():
    p = RESULTS_DIR / "decision_analysis.csv"
    if not p.exists():
        return
    d = pd.read_csv(p)
    u = d.groupby(["regime", "method", "dataset", "trait"]).mean(numeric_only=True).reset_index()
    meths = ["SCP", "CV+", "Gauss-PEV", "CalPred-style", "KinCP"]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))
    for ri, reg in enumerate(["R1", "R2"]):
        for mi, m in enumerate(meths):
            v = u[(u.regime == reg) & (u.method == m)]
            if v.empty:
                continue
            x = ri * 1.4 + mi * 0.2
            lo, hi = boot_ci(v.sel_coverage)
            axes[0].errorbar(x, v.sel_coverage.mean(), yerr=[[v.sel_coverage.mean() - lo], [hi - v.sel_coverage.mean()]],
                             color=COL[m], marker=MRK[m], ms=4, capsize=1.5, label=lab(m) if ri == 0 else None)
            lo, hi = boot_ci(v.sel_below_lower)
            axes[1].errorbar(x, v.sel_below_lower.mean(), yerr=[[v.sel_below_lower.mean() - lo], [hi - v.sel_below_lower.mean()]],
                             color=COL[m], marker=MRK[m], ms=4, capsize=1.5)
    for ax in axes:
        ax.set_xticks([0.4, 1.8], ["R1", "R2"])
    axes[0].axhline(0.9, color=INK2, lw=0.8, ls="--")
    axes[1].axhline(0.05, color=INK2, lw=0.8, ls="--")
    axes[0].set_ylabel("Coverage among top-10% selected")
    axes[1].set_ylabel("Share of selected below lower bound")
    axes[0].set_title("a  Selection-conditional coverage", fontsize=8, loc="left", color=INK)
    axes[1].set_title("b  Lower-bound violations (target 0.05)", fontsize=8, loc="left", color=INK)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.07), fontsize=7)
    fig.tight_layout()
    save(fig, "Fig11_selection")


# ---------------------------------------------------------------- Fig 12: forest plot of statistics
def fig12():
    st = pd.read_csv(RESULTS_DIR / "statistics_table.csv")
    st = st[(st.base == "GBLUP") & (st.endpoint == "cond_err") & (st.family == "baseline")]
    comps = ["Gauss-PEV", "Gauss-homosc", "SCP", "NormCP", "CV+", "CalPred-style", "CalPred-style(rand)"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    for ax, reg in zip(axes, ["R1", "R2", "R3"]):
        g = st[st.regime == reg].set_index("competitor").reindex(comps)
        y = np.arange(len(comps))
        ax.errorbar(g.median_diff, y, xerr=[g.median_diff - g.ci_low, g.ci_high - g.median_diff], fmt="o", color=COL["KinCP"],
                    ms=3.5, capsize=1.5, elinewidth=0.8)
        for yi, (_, r) in zip(y, g.iterrows()):
            if np.isfinite(r.p_holm) and r.p_holm < 0.05:
                ax.annotate("*", xy=(r.ci_high, yi), xytext=(3, -2), textcoords="offset points", fontsize=9, color=INK)
        ax.axvline(0, color=INK2, lw=0.8, ls="--")
        ax.set_title(REG[reg], fontsize=8, loc="left", color=INK)
        ax.margins(x=0.12)
    axes[0].set_yticks(range(len(comps)), [lab(c) for c in comps], fontsize=6.5)
    axes[0].invert_yaxis()
    fig.supxlabel("Median paired difference in conditional coverage error (competitor − KinCP); * Holm P < 0.05", fontsize=7.5)
    fig.tight_layout()
    save(fig, "Fig12_statistics_forest")


def main():
    s = load()
    for f in (fig1, fig2, fig8, fig10, fig11, fig12):
        try:
            f()
        except Exception as e:  # keep going; report
            print("figure failed", f.__name__, e)
    for f in (fig3, fig4, fig5, fig6, fig7, fig9):
        try:
            f(s)
        except Exception as e:
            print("figure failed", f.__name__, e)


if __name__ == "__main__":
    main()
