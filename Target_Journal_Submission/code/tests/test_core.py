"""Unit tests for the statistical core (run: pytest -q tests)."""
import numpy as np
import pytest
from scipy import linalg

from kincp.conformal.methods import (FoldData, conformal_quantile, cv_plus, kincp, localization_weights,
                                     weighted_quantiles)
from kincp.models.kernel_blup import KernelBLUP, reml
from kincp.preprocessing.genomic import grm_vanraden


def _sim_geno(n=300, m=2000, seed=0):
    rng = np.random.default_rng(seed)
    p = rng.uniform(0.05, 0.5, m)
    return rng.binomial(2, p, size=(n, m)).astype(np.int8)


def test_conformal_quantile_order_statistic():
    s = np.arange(1, 20, dtype=float)       # n = 19
    assert conformal_quantile(s, 0.1) == 18.0   # ceil(0.9*20)=18
    assert np.isinf(conformal_quantile(s[:5], 0.1))


def test_weighted_equals_unweighted_with_unit_weights():
    rng = np.random.default_rng(1)
    s = rng.exponential(size=99)
    W = np.ones((3, 99))
    q = weighted_quantiles(s, W, 0.1, w_test=1.0)
    assert np.allclose(q, conformal_quantile(s, 0.1))


def test_split_conformal_marginal_coverage():
    rng = np.random.default_rng(2)
    cov = []
    for _ in range(400):
        cal = np.abs(rng.standard_t(3, 200))
        q = conformal_quantile(cal, 0.1)
        cov.append(abs(rng.standard_t(3)) <= q)
    assert 0.86 < np.mean(cov) < 0.94


def test_grm_properties():
    X = _sim_geno()
    G, Gs, m = grm_vanraden(X, chunk=500)
    assert np.allclose(G, G.T)
    assert abs(np.mean(np.diag(G)) - 1.0) < 0.1
    assert abs(np.mean(np.diag(Gs)) - 1.0) < 0.05


def test_reml_recovers_heritability():
    X = _sim_geno(n=800, m=3000, seed=3)
    G, _, _ = grm_vanraden(X)
    rng = np.random.default_rng(4)
    w, V = np.linalg.eigh(G)
    L = V * np.sqrt(np.maximum(w, 0))
    h2 = 0.6
    g = L @ rng.normal(size=len(G)) * np.sqrt(h2)
    y = 3.0 + g + rng.normal(size=len(G)) * np.sqrt(1 - h2)
    vc = reml(G, y)
    assert abs(vc.s2g / (vc.s2g + vc.s2e) - h2) < 0.15


def test_kernel_blup_matches_closed_form():
    X = _sim_geno(n=120, m=800, seed=5)
    G, _, _ = grm_vanraden(X)
    rng = np.random.default_rng(6)
    y = rng.normal(size=100)
    S, Q = np.arange(100), np.arange(100, 120)
    delta = 0.7
    m = KernelBLUP(G, delta).fit(S, y)
    pred, d = m.predict(Q, return_d=True)
    V = G[np.ix_(S, S)] + delta * np.eye(100)
    Vi = linalg.inv(V)
    one = np.ones(100)
    mu = one @ Vi @ y / (one @ Vi @ one)
    k = G[np.ix_(S, Q)]
    assert np.allclose(pred, mu + k.T @ Vi @ (y - mu))
    d_ref = np.diag(G)[Q] - np.einsum("ij,ij->j", k, Vi @ k) + (1 - one @ Vi @ k) ** 2 / (one @ Vi @ one)
    assert np.allclose(d, d_ref)
    assert np.all(d > 0)


def test_localization_floor_reaches_mass():
    diff = np.array([[10.0] * 200, [0.0] * 200])
    W = localization_weights(diff, h0=0.1, n_min=50)
    assert W[0].sum() >= 50 and W[1].sum() >= 50


def test_kincp_finite_and_contains_center():
    rng = np.random.default_rng(7)
    pools = {k: dict(res=rng.normal(size=300), d=rng.uniform(0.2, 1.0, 300), fold=rng.integers(0, 5, 300))
             for k in ("rand", "clus")}
    fd = FoldData(yhat=np.zeros(40), d=rng.uniform(0.1, 1.5, 40), s2g=0.5, s2e=0.5, pools=pools,
                  cvplus_pred=rng.normal(size=(40, 5)) * 0.01)
    lo, hi = kincp(fd, 0.1)
    assert np.all(np.isfinite(lo)) and np.all(np.isfinite(hi)) and np.all(lo < 0) and np.all(hi > 0)
    lo2, hi2 = cv_plus(fd, 0.1)
    assert np.all(lo2 < hi2)


def test_kincp_coverage_under_relatedness_heteroscedasticity():
    """Residual SD grows with d; pools span d; KinCP should be near nominal in every d-tercile."""
    rng = np.random.default_rng(8)
    s2g, s2e = 0.5, 0.5
    def draw(n):
        d = np.exp(rng.uniform(np.log(0.05), np.log(1.2), n))
        return d, rng.normal(size=n) * np.sqrt(s2g * d + s2e)
    covs = {0: [], 1: [], 2: []}
    for _ in range(30):
        dr, rr = draw(400)
        dc, rc = draw(400)
        dt, rt = draw(300)
        fd = FoldData(yhat=np.zeros(300), d=dt, s2g=s2g, s2e=s2e,
                      pools=dict(rand=dict(res=rr, d=dr, fold=np.zeros(400, int)),
                                 clus=dict(res=rc, d=dc, fold=np.zeros(400, int))))
        lo, hi = kincp(fd, 0.1)
        c = (rt >= lo) & (rt <= hi)
        terc = np.digitize(dt, np.quantile(dt, [1 / 3, 2 / 3]))
        for t in range(3):
            covs[t].append(c[terc == t].mean())
    for t in range(3):
        assert 0.86 < np.mean(covs[t]) < 0.94


def test_cv_plus_marginal_coverage_exchangeable():
    """CV+ on exchangeable synthetic residuals: coverage at least 1 - 2*alpha and close to nominal."""
    rng = np.random.default_rng(9)
    cov = []
    for _ in range(200):
        n = 150
        res = rng.normal(size=n)
        fold = np.arange(n) % 5
        P = np.zeros((1, 5))
        fd = FoldData(yhat=np.zeros(1), d=np.ones(1), s2g=1.0, s2e=1.0,
                      pools=dict(rand=dict(res=res, d=np.ones(n), fold=fold)), cvplus_pred=P)
        lo, hi = cv_plus(fd, 0.1)
        y = rng.normal()
        cov.append(lo[0] <= y <= hi[0])
    assert np.mean(cov) > 0.84


def test_mondrian_and_calpred_return_finite_ordered_bounds():
    from kincp.conformal.methods import calpred_style, mondrian_bins
    rng = np.random.default_rng(10)
    pools = {k: dict(res=rng.normal(size=400), d=rng.uniform(0.1, 1.0, 400), fold=rng.integers(0, 5, 400))
             for k in ("rand", "clus")}
    fd = FoldData(yhat=np.zeros(30), d=rng.uniform(0.1, 1.0, 30), s2g=0.5, s2e=0.5, pools=pools)
    for f in (mondrian_bins, calpred_style):
        lo, hi = f(fd, 0.1)
        assert np.all(np.isfinite(lo)) and np.all(lo < hi)


def test_config_is_read():
    from kincp.utils import STUDY
    from kincp.training.runner import SEEDS
    assert tuple(STUDY["seeds"]) == SEEDS == (11, 22, 33, 44, 55)
    assert STUDY["kincp"]["mass_floor_n_min"] == 50
