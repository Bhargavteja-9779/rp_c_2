"""Prediction-interval methods compared in the study.

Notation (one outer fold): T = training individuals, U = test (deployment) individuals.
  yhat[U]    full-training-set prediction of the base model
  d[U]       relatedness covariate (GBLUP PEV in s2g units) of U w.r.t. T
  s2g, s2e   REML variance components of GBLUP fitted on T (outer fold only)
Calibration pools of out-of-fold residuals inside T:
  pool 'rand': random K-fold cross-fitting in T          -> (res, d, fold)
  pool 'clus': genomic-cluster K-fold cross-fitting in T -> (res, d, fold)
For each pooled residual, d is measured w.r.t. the inner training subset that produced it.

KinCP (proposed) = A + B + C:
  A  calibration pool = rand U clus, i.e. it spans close-relative and distant-relative residuals;
  B  normalised nonconformity score  s = |res| / sqrt(s2g*d + s2e);
  C  localisation of the conformal quantile in log(d) with a Gaussian kernel,
     q(d_j) = weighted (1-alpha) quantile of {s_i} with weights w_i = exp(-(log d_i - log d_j)^2 / (2h^2)),
     plus a point mass w=1 at +infinity for the test point (weighted CP, Tibshirani et al. 2019; localized CP, Guan 2023).
Interval: yhat_j +/- q(d_j) * sqrt(s2g*d_j + s2e).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize, stats


@dataclass
class FoldData:
    yhat: np.ndarray                 # base predictions for U (full T fit)
    d: np.ndarray                    # relatedness covariate of U w.r.t. T
    s2g: float
    s2e: float
    pools: dict                      # name -> dict(res, d, fold)
    cvplus_pred: np.ndarray | None = None   # (n_U, K) predictions of the random inner-fold models at U
    scp: dict | None = None          # dict(res, d_cal, yhat, d_test) for split conformal (random 80/20)
    extra: dict = field(default_factory=dict)


def conformal_quantile(scores: np.ndarray, alpha: float) -> float:
    """Split-conformal quantile: ceil((1-alpha)(n+1))-th smallest score (inf if it does not exist)."""
    n = len(scores)
    k = int(np.ceil((1 - alpha) * (n + 1)))
    if k > n:
        return np.inf
    return float(np.partition(scores, k - 1)[k - 1])


def weighted_quantiles(scores: np.ndarray, W: np.ndarray, alpha: float, w_test: float | np.ndarray = 1.0) -> np.ndarray:
    """Row-wise weighted conformal quantile. W has shape (n_test, n_cal); the test point's own
    weight w_test goes to +inf. Returns, per row, the smallest s with
    sum_i W_i 1{s_i <= s} / (sum_i W_i + w_test) >= 1 - alpha."""
    order = np.argsort(scores)
    s_sorted = scores[order]
    Ws = W[:, order]
    cw = np.cumsum(Ws, axis=1)
    tot = cw[:, -1] + w_test
    ok = cw >= (1 - alpha) * tot[:, None]
    idx = np.argmax(ok, axis=1)
    has = ok[np.arange(len(idx)), idx]
    q = np.where(has, s_sorted[idx], np.inf)
    return q


def sigma_of_d(d: np.ndarray, s2g: float, s2e: float) -> np.ndarray:
    return np.sqrt(s2g * d + s2e)


# --------------------------------------------------------------------------- baselines
def gauss_pev(fd: FoldData, alpha: float):
    z = stats.norm.ppf(1 - alpha / 2)
    h = z * sigma_of_d(fd.d, fd.s2g, fd.s2e)
    return fd.yhat - h, fd.yhat + h


def gauss_homosc(fd: FoldData, alpha: float):
    z = stats.norm.ppf(1 - alpha / 2)
    sd = np.std(fd.pools["rand"]["res"], ddof=1)
    return fd.yhat - z * sd, fd.yhat + z * sd


def split_conformal(fd: FoldData, alpha: float):
    q = conformal_quantile(np.abs(fd.scp["res"]), alpha)
    return fd.scp["yhat"] - q, fd.scp["yhat"] + q


def norm_split_conformal(fd: FoldData, alpha: float):
    sc = np.abs(fd.scp["res"]) / sigma_of_d(fd.scp["d_cal"], fd.s2g, fd.s2e)
    q = conformal_quantile(sc, alpha)
    h = q * sigma_of_d(fd.scp["d_test"], fd.s2g, fd.s2e)
    return fd.scp["yhat"] - h, fd.scp["yhat"] + h


def cv_plus(fd: FoldData, alpha: float):
    """CV+ (Barber, Candes, Ramdas & Tibshirani 2021) with random K-fold models."""
    pool = fd.pools["rand"]
    R = np.abs(pool["res"])
    P = fd.cvplus_pred[:, pool["fold"]]            # (n_U, n_T) prediction of the model that excluded i
    n = len(R)
    k_lo = int(np.floor(alpha * (n + 1)))
    k_hi = int(np.ceil((1 - alpha) * (n + 1)))
    lo_vals = P - R[None, :]
    hi_vals = P + R[None, :]
    lo = np.full(P.shape[0], -np.inf) if k_lo < 1 else np.partition(lo_vals, k_lo - 1, axis=1)[:, k_lo - 1]
    hi = np.full(P.shape[0], np.inf) if k_hi > n else np.partition(hi_vals, k_hi - 1, axis=1)[:, k_hi - 1]
    return lo, hi


def _pool(fd: FoldData, which: tuple[str, ...]):
    res = np.concatenate([fd.pools[w]["res"] for w in which])
    d = np.concatenate([fd.pools[w]["d"] for w in which])
    return res, d


def calpred_style(fd: FoldData, alpha: float, which=("rand", "clus")):
    """Heteroscedastic Gaussian calibration in the spirit of CalPred (Hou et al. 2024):
    res ~ N(m0 + m1 c, exp(2(a + b c))) with context c = standardised log d, fitted by ML on the pool."""
    res, d = _pool(fd, which)
    ld = np.log(d)
    mu_c, sd_c = ld.mean(), ld.std() + 1e-12
    c = (ld - mu_c) / sd_c

    def nll(th):
        m0, m1, a, b = th
        s = np.exp(a + b * c)
        return np.sum(np.log(s) + 0.5 * ((res - m0 - m1 * c) / s) ** 2)

    th0 = np.array([res.mean(), 0.0, np.log(res.std() + 1e-9), 0.0])
    th = optimize.minimize(nll, th0, method="L-BFGS-B").x
    ct = (np.log(fd.d) - mu_c) / sd_c
    m = th[0] + th[1] * ct
    s = np.exp(th[2] + th[3] * ct)
    z = stats.norm.ppf(1 - alpha / 2)
    return fd.yhat + m - z * s, fd.yhat + m + z * s


def localization_weights(diff: np.ndarray, h0: float, n_min: float | None, grow: float = 1.25,
                         max_iter: int = 60) -> np.ndarray:
    """Gaussian kernel weights in log(d) (weight 1 at zero distance, i.e. the test point's own weight).
    If n_min is given, the bandwidth of each test row is widened (h <- 1.25 h) until the total calibration
    weight sum_i w_i reaches n_min (the calibration mass measured in units of the test point's weight,
    which is what enters the weighted conformal quantile). The bandwidth therefore depends only on
    relatedness covariates, never on scores or outcomes."""
    h = np.full(diff.shape[0], h0, dtype=float)
    W = np.exp(-0.5 * (diff / h[:, None]) ** 2)
    if n_min is None:
        return W
    for _ in range(max_iter):
        bad = W.sum(1) < n_min
        if not bad.any():
            break
        h[bad] *= grow
        W[bad] = np.exp(-0.5 * (diff[bad] / h[bad, None]) ** 2)
    return W


N_MIN_DEFAULT = 50


def kincp(fd: FoldData, alpha: float, A: bool = True, B: bool = True, C: bool = True, h_mult: float = 0.5,
          return_q: bool = False, n_min: float | None = N_MIN_DEFAULT):
    """KinCP and its ablations (A: relatedness-diverse pool, B: PEV-normalised score, C: localisation)."""
    which = ("rand", "clus") if A else ("rand",)
    res, d = _pool(fd, which)
    if B:
        sc = np.abs(res) / sigma_of_d(d, fd.s2g, fd.s2e)
        scale = sigma_of_d(fd.d, fd.s2g, fd.s2e)
    else:
        sc = np.abs(res)
        scale = np.ones_like(fd.d)
    if C and np.isfinite(h_mult):
        ld = np.log(d)
        h0 = h_mult * (ld.std() + 1e-12)
        diff = np.log(fd.d)[:, None] - ld[None, :]
        W = localization_weights(diff, h0, n_min)
        q = weighted_quantiles(sc, W, alpha, w_test=1.0)
    else:
        q = np.full(len(fd.d), conformal_quantile(sc, alpha))
    lo, hi = fd.yhat - q * scale, fd.yhat + q * scale
    if return_q:
        return lo, hi, q
    return lo, hi


ABLATIONS = {
    "KinCP": dict(A=True, B=True, C=True),
    "KinCP-A": dict(A=False, B=True, C=True),
    "KinCP-B": dict(A=True, B=False, C=True),
    "KinCP-C": dict(A=True, B=True, C=False),
    "KinCP-AB": dict(A=False, B=False, C=True),
    "KinCP-AC": dict(A=False, B=True, C=False),
    "KinCP-BC": dict(A=True, B=False, C=False),
    "KinCP-ABC": dict(A=False, B=False, C=False),   # = random-fold OOF residual quantile (PredInterval-like)
}


def all_intervals(fd: FoldData, alpha: float, base: str, h_mults=(0.25, 1.0, 2.0)) -> dict:
    out = {}
    if base == "GBLUP":
        out["Gauss-PEV"] = gauss_pev(fd, alpha)
    out["Gauss-homosc"] = gauss_homosc(fd, alpha)
    out["SCP"] = split_conformal(fd, alpha)
    out["NormCP"] = norm_split_conformal(fd, alpha)
    out["CV+"] = cv_plus(fd, alpha)
    out["CalPred-style"] = calpred_style(fd, alpha, ("rand", "clus"))
    out["CalPred-style(rand)"] = calpred_style(fd, alpha, ("rand",))
    for name, flags in ABLATIONS.items():
        out[name] = kincp(fd, alpha, **flags)
    for hm in h_mults:
        out[f"KinCP[h={hm}]"] = kincp(fd, alpha, h_mult=hm)
    if h_mults:   # sensitivity: fixed bandwidth (no effective-sample-size floor) and other floors
        out["KinCP[fixed-h]"] = kincp(fd, alpha, n_min=None)
        out["KinCP[nmin=25]"] = kincp(fd, alpha, n_min=25)
        out["KinCP[nmin=100]"] = kincp(fd, alpha, n_min=100)
    return out
