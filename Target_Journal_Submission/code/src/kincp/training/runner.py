"""Outer/inner cross-fitting loop: produces per-individual prediction intervals for every method.

One *job* = (dataset, trait, regime, base predictor). Outer folds come from the regime.
Inside each outer training set T we run, with fixed outer variance components:
  (i)  random 5-fold cross-fitting      -> pool 'rand' + CV+ fold predictions at U
  (ii) genomic-cluster 5-fold fitting   -> pool 'clus'  (k-means on genotype PCs of T)
  (iii) one random 80/20 split          -> split conformal (SCP, NormCP)
Phenotypes are standardised with training-fold mean/SD only.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold

from ..conformal.methods import FoldData, all_intervals
from ..data.easygese import easygese_folds, read_cv_assignments, read_phenotypes
from ..data.prepare import prepare
from ..models.base import GBLUPPredictor, LightGBMPredictor, RKHSPredictor
from ..models.kernel_blup import KernelBLUP, reml

from ..utils import STUDY

SEEDS = tuple(STUDY["seeds"])


@dataclass
class Job:
    dataset: str
    trait: str
    regime: str          # R1 | R2 | R3
    base: str            # GBLUP | RKHS | LightGBM
    repeats: tuple       # R1/R3: EasyGeSe repeats (1..5); R2: seed indices
    alphas: tuple = tuple(STUDY["alphas"])
    inner_k: int = STUDY["inner_cross_fitting"]["k"]
    scp_frac: float = STUDY["inner_cross_fitting"]["scp_calibration_fraction"]
    y_override: np.ndarray | None = None   # simulation study: phenotypes supplied directly
    g_true: np.ndarray | None = None       # simulation study: true genetic values
    tag: str = ""


def _make_base(base, geno, seed):
    if base == "GBLUP":
        return GBLUPPredictor(geno["G"])
    if base == "RKHS":
        return RKHSPredictor(geno["Kg"])
    if base == "LightGBM":
        return LightGBMPredictor(geno["Xthin"], seed=seed)
    raise ValueError(base)


def _outer_folds(job: Job, geno, has_y: np.ndarray, rep: int):
    """Return a fold label per individual (-1 = not used) and the seed for this repeat."""
    n = len(has_y)
    if job.regime in ("R1", "R3"):
        if job.y_override is not None:     # simulation: seeded random 5-fold
            lab = np.full(n, -1)
            idx = np.flatnonzero(has_y)
            kf = KFold(5, shuffle=True, random_state=SEEDS[rep - 1])
            for f, (_, te) in enumerate(kf.split(idx)):
                lab[idx[te]] = f
        else:
            z = read_cv_assignments(job.dataset)
            lab = easygese_folds(z, job.trait, geno["ids"], rep)
            lab[~has_y] = -1
            missing = has_y & (lab < 0)
            if missing.any():   # individuals with phenotype but no EasyGeSe fold: assign deterministically
                lab[missing] = np.arange(missing.sum()) % 5
        return lab, SEEDS[rep - 1]
    if job.regime == "R2":
        lab = geno["clusters"].astype(int).copy()
        lab[~has_y] = -1
        return lab, SEEDS[rep - 1]
    if job.regime.startswith("R2k"):      # Reviewer 5: cluster granularity sensitivity (k = 3, 10)
        k = int(job.regime[3:])
        lab = KMeans(n_clusters=k, n_init=10, random_state=2026).fit_predict(geno["pcs"]).astype(int)
        lab[~has_y] = -1
        return lab, SEEDS[rep - 1]
    if job.regime == "R2fam":             # Reviewer 5: leave-one-family-out with real families (oyster IDs)
        fam = np.array([str(i).split("_")[0] for i in geno["ids"]])
        lab = np.unique(fam, return_inverse=True)[1].astype(int)
        lab[~has_y] = -1
        return lab, SEEDS[rep - 1]
    raise ValueError(job.regime)


def _cross_fit(base_obj, delta_base, Kg_delta, G, S, y_S, folds, U, need_u_pred):
    """Fit the base model on S minus each fold; return OOF residuals, their d (w.r.t. the inner
    training subset, GBLUP metric) and, optionally, the fold models' predictions at U."""
    res = np.empty(len(S))
    d = np.empty(len(S))
    fold_id = np.empty(len(S), dtype=int)
    preds_u = []
    for f, ho in enumerate(folds):
        tr = np.setdiff1d(np.arange(len(S)), ho)
        base_obj.fit_fixed(S[tr], y_S[tr], delta_base)
        q = np.concatenate([S[ho], U]) if need_u_pred else S[ho]
        p = base_obj.predict(q)
        res[ho] = y_S[ho] - p[: len(ho)]
        if need_u_pred:
            preds_u.append(p[len(ho):])
        # relatedness covariate of held-out individuals relative to S[tr], GBLUP metric
        if getattr(base_obj, "name", "") == "GBLUP":
            d[ho] = base_obj.m.predict(S[ho], return_d=True)[1]
        else:
            m = KernelBLUP(G, Kg_delta).fit(S[tr], np.zeros(len(tr)))
            d[ho] = m.predict(S[ho], return_d=True)[1]
        fold_id[ho] = f
    P = np.column_stack(preds_u) if need_u_pred else None
    return dict(res=res, d=d, fold=fold_id), P


def run_job(job: Job, h_mults=(0.25, 1.0, 2.0)) -> tuple[pd.DataFrame, pd.DataFrame]:
    geno = prepare(job.dataset)
    G = geno["G"]
    n = G.shape[0]
    if job.y_override is not None:
        y_all = np.asarray(job.y_override, dtype=float)
    else:
        y_all = read_phenotypes(job.dataset)[job.trait].to_numpy(dtype=float)
    has_y = np.isfinite(y_all)
    pcs = geno["pcs"]
    Gstd = G / np.sqrt(np.outer(np.diag(G), np.diag(G)))
    rec_frames, timing_rows = [], []
    for rep in job.repeats:
        lab, seed = _outer_folds(job, geno, has_y, rep)
        rng = np.random.default_rng(seed)
        for f in sorted(set(lab[lab >= 0].tolist())):
            U = np.flatnonzero(lab == f)
            T = np.flatnonzero((lab >= 0) & (lab != f))
            if job.regime == "R3":
                T = np.sort(rng.choice(T, size=len(T) // 2, replace=False))
            if len(U) < 5 or len(T) < 30:
                continue
            mu, sd = y_all[T].mean(), y_all[T].std(ddof=1)
            yT = (y_all[T] - mu) / sd
            yU = (y_all[U] - mu) / sd
            t0 = time.perf_counter()
            vc = reml(G[np.ix_(T, T)], yT)                      # GBLUP variance components (outer)
            gm = KernelBLUP(G, vc.delta).fit(T, yT)
            yhat_g, dU = gm.predict(U, return_d=True)
            base_obj = _make_base(job.base, geno, seed)
            if job.base == "GBLUP":
                delta_base, yhat = vc.delta, yhat_g
            elif job.base == "RKHS":
                vcr = reml(geno["Kg"][np.ix_(T, T)], yT)
                delta_base = vcr.delta
                yhat = base_obj.fit_fixed(T, yT, delta_base).predict(U)
            else:
                delta_base = None
                yhat = base_obj.fit_fixed(T, yT, None).predict(U)
            t_outer = time.perf_counter() - t0
            # (i) random inner folds
            t0 = time.perf_counter()
            kf = KFold(job.inner_k, shuffle=True, random_state=seed)
            rfolds = [te for _, te in kf.split(T)]
            pool_r, P = _cross_fit(base_obj, delta_base, vc.delta, G, T, yT, rfolds, U, True)
            t_rand = time.perf_counter() - t0
            # (ii) genomic-cluster inner folds (k-means on PCs of T only)
            t0 = time.perf_counter()
            k_in = min(job.inner_k, max(2, len(T) // 20))
            cl = KMeans(n_clusters=k_in, n_init=10, random_state=seed).fit_predict(pcs[T])
            cfolds = [np.flatnonzero(cl == c) for c in range(k_in) if (cl == c).sum() > 0]
            pool_c, Pc = _cross_fit(base_obj, delta_base, vc.delta, G, T, yT, cfolds, U, job.tag == "competitor")
            t_clus = time.perf_counter() - t0
            pools = dict(rand=pool_r, clus=pool_c)
            if job.tag == "explore":
                # exploratory (Phase 19): inner folds = the *global* genomic clusters present in T,
                # i.e. calibration shifts of the same granularity as cluster-out deployment
                gl = geno["clusters"][T]
                gfolds = [np.flatnonzero(gl == c) for c in np.unique(gl) if (gl == c).sum() >= 5]
                if len(gfolds) >= 2:
                    pools["glob"], _ = _cross_fit(base_obj, delta_base, vc.delta, G, T, yT, gfolds, U, False)
            # (iii) split conformal
            t0 = time.perf_counter()
            perm = rng.permutation(len(T))
            ncal = max(int(round(job.scp_frac * len(T))), 10)
            cal, fit = np.sort(perm[:ncal]), np.sort(perm[ncal:])
            base_obj.fit_fixed(T[fit], yT[fit], delta_base)
            p = base_obj.predict(np.concatenate([T[cal], U]))
            m80 = KernelBLUP(G, vc.delta).fit(T[fit], np.zeros(len(fit)))
            scp = dict(res=yT[cal] - p[:ncal], d_cal=m80.predict(T[cal], return_d=True)[1],
                       yhat=p[ncal:], d_test=m80.predict(U, return_d=True)[1])
            t_scp = time.perf_counter() - t0
            fd = FoldData(yhat=yhat, d=dU, s2g=vc.s2g, s2e=vc.s2e,
                          pools=pools, cvplus_pred=P, scp=scp)
            if job.tag == "competitor":     # Reviewer 8: group (cluster-fold) CV+ competitors
                fd.extra["cvplus_clus"] = Pc
            maxkin = Gstd[np.ix_(U, T)].max(axis=1)
            for a in job.alphas:
                t0 = time.perf_counter()
                ints = all_intervals(fd, a, job.base, h_mults=h_mults if a == 0.10 else ())
                t_int = time.perf_counter() - t0
                for meth, (lo, hi) in ints.items():
                    fr = pd.DataFrame(dict(idx=U, y=yU, yhat=yhat, lo=lo, hi=hi, d=dU, maxkin=maxkin))
                    fr["method"] = meth
                    fr["alpha"] = a
                    fr["rep"] = rep
                    fr["fold"] = f
                    if job.g_true is not None:
                        fr["g_true"] = (job.g_true[U] - mu) / sd
                        fr["ghat"] = yhat
                    rec_frames.append(fr)
                timing_rows.append(dict(rep=rep, fold=f, alpha=a, t_interval_all_methods=t_int))
            timing_rows.append(dict(rep=rep, fold=f, alpha=np.nan, n_train=len(T), n_test=len(U),
                                    t_outer_fit=t_outer, t_pool_rand=t_rand, t_pool_clus=t_clus, t_scp=t_scp,
                                    delta=vc.delta, s2g=vc.s2g, s2e=vc.s2e, h2_reml=vc.s2g / (vc.s2g + vc.s2e),
                                    r_pred=float(np.corrcoef(yU, yhat)[0, 1])))
    rec = pd.concat(rec_frames, ignore_index=True) if rec_frames else pd.DataFrame()
    tim = pd.DataFrame(timing_rows)
    for df in (rec, tim):
        df["dataset"] = job.dataset
        df["trait"] = job.trait
        df["regime"] = job.regime
        df["base"] = job.base
        df["tag"] = job.tag
    return rec, tim
