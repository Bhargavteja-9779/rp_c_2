"""Kernel BLUP (GBLUP / RKHS) with REML variance components and prediction error variances.

Model for training individuals S:  y = 1*mu + g + e,  g ~ N(0, s2g K_SS),  e ~ N(0, s2e I).
delta = s2e / s2g.  V = K_SS + delta I  (covariance in s2g units).

For a new individual j with kernel column k = K_Sj, the BLUP prediction is
  yhat_j = mu_hat + k' V^{-1} (y - 1 mu_hat),
and the prediction error variance of the *phenotype* (universal-kriging form, which also accounts for
the uncertainty of the GLS mean) is s2g * d_j + s2e, with
  d_j = K_jj - k' V^{-1} k + (1 - 1' V^{-1} k)^2 / (1' V^{-1} 1).
d_j is the GBLUP prediction error variance of the genetic value in units of s2g. It depends only on
genotypes, on the training set and on delta. KinCP uses it as the relatedness covariate.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import linalg, optimize


@dataclass
class VarComp:
    delta: float
    s2g: float
    s2e: float
    mu: float
    loglik: float


def reml(K_SS: np.ndarray, y: np.ndarray, log_delta_bounds=(-9.0, 9.0), grid: int = 60) -> VarComp:
    """REML estimation of delta, s2g (intercept-only fixed effects) via the spectral approach
    of Kang et al. (2008, EMMA): grid search on log(delta) followed by bounded Brent refinement."""
    n = len(y)
    S, U = linalg.eigh(K_SS, check_finite=False)
    S = np.maximum(S, 0.0)
    ys = U.T @ y
    xs = U.T @ np.ones(n)

    def negll(logd):
        h = S + np.exp(logd)
        xhx = np.sum(xs * xs / h)
        beta = np.sum(xs * ys / h) / xhx
        r = ys - xs * beta
        s2g = np.sum(r * r / h) / (n - 1)
        return 0.5 * ((n - 1) * np.log(s2g) + np.sum(np.log(h)) + np.log(xhx))

    lg = np.linspace(*log_delta_bounds, grid)
    vals = np.array([negll(v) for v in lg])
    i = int(np.argmin(vals))
    lo, hi = lg[max(i - 1, 0)], lg[min(i + 1, grid - 1)]
    if lo < hi:
        res = optimize.minimize_scalar(negll, bounds=(lo, hi), method="bounded", options={"xatol": 1e-4})
        logd, f = float(res.x), float(res.fun)
        if vals[i] < f:
            logd, f = float(lg[i]), float(vals[i])
    else:
        logd, f = float(lg[i]), float(vals[i])
    delta = float(np.exp(logd))
    h = S + delta
    xhx = np.sum(xs * xs / h)
    mu = float(np.sum(xs * ys / h) / xhx)
    r = ys - xs * mu
    s2g = float(np.sum(r * r / h) / (n - 1))
    return VarComp(delta=delta, s2g=s2g, s2e=delta * s2g, mu=mu, loglik=-f)


class KernelBLUP:
    """BLUP for a fixed kernel and fixed delta (fit by Cholesky)."""

    def __init__(self, K: np.ndarray, delta: float):
        self.K = K
        self.delta = float(delta)

    def fit(self, S: np.ndarray, y: np.ndarray) -> "KernelBLUP":
        self.S = np.asarray(S)
        V = self.K[np.ix_(self.S, self.S)].copy()
        V[np.diag_indices_from(V)] += self.delta
        self.cf = linalg.cho_factor(V, lower=True, check_finite=False)
        one = np.ones(len(self.S))
        self.vinv1 = linalg.cho_solve(self.cf, one, check_finite=False)
        self.oneVone = float(one @ self.vinv1)
        self.mu = float(self.vinv1 @ y / self.oneVone)
        self.alpha = linalg.cho_solve(self.cf, y - self.mu, check_finite=False)
        return self

    def predict(self, Q: np.ndarray, return_d: bool = False):
        Q = np.asarray(Q)
        KSQ = self.K[np.ix_(self.S, Q)]
        pred = self.mu + KSQ.T @ self.alpha
        if not return_d:
            return pred
        W = linalg.cho_solve(self.cf, KSQ, check_finite=False)
        quad = np.einsum("ij,ij->j", KSQ, W)
        gls = (1.0 - self.vinv1 @ KSQ) ** 2 / self.oneVone
        d = np.diag(self.K)[Q] - quad + gls
        return pred, np.maximum(d, 1e-12)


def pev_d(K: np.ndarray, delta: float, S: np.ndarray, Q: np.ndarray) -> np.ndarray:
    """Relatedness covariate d (GBLUP PEV in s2g units) of individuals Q w.r.t. training set S."""
    m = KernelBLUP(K, delta).fit(S, np.zeros(len(S)))
    return m.predict(Q, return_d=True)[1]
