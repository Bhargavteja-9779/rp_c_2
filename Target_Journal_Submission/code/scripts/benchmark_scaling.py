"""Reviewer 6: controlled scaling benchmark of KinCP's cost (time and peak memory) vs training-set size.

Uses random subsets of the maize genotypes (n_train in {500, 1000, 2000, 3500}, 300 candidates),
a simulated additive trait (h2 = 0.5), one CPU thread, and measures separately:
REML outer fit, random-fold pool, cluster-fold pool, KinCP interval computation.
Peak memory is measured with tracemalloc (NumPy allocations are traced). Writes results/scaling.csv.
"""
from __future__ import annotations

import os
import sys
import time
import tracemalloc
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.model_selection import KFold  # noqa: E402
from threadpoolctl import threadpool_limits  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.conformal.methods import FoldData, kincp  # noqa: E402
from kincp.data.prepare import prepare  # noqa: E402
from kincp.models.kernel_blup import KernelBLUP, reml  # noqa: E402
from kincp.utils import RESULTS_DIR  # noqa: E402


def pool(G, delta, T, y, folds):
    res, d = np.empty(len(T)), np.empty(len(T))
    for ho in folds:
        tr = np.setdiff1d(np.arange(len(T)), ho)
        m = KernelBLUP(G, delta).fit(T[tr], y[tr])
        p, dd = m.predict(T[ho], return_d=True)
        res[ho], d[ho] = y[ho] - p, dd
    return dict(res=res, d=d, fold=np.zeros(len(T), int))


def main():
    geno = prepare("maize")
    G, pcs = geno["G"], geno["pcs"]
    rng = np.random.default_rng(2026)
    n = G.shape[0]
    L = np.linalg.cholesky(G + 1e-3 * np.eye(n))
    g = L @ rng.normal(size=n)
    g = (g - g.mean()) / g.std() * np.sqrt(0.5)
    y = g + rng.normal(size=n) * np.sqrt(0.5)
    rows = []
    with threadpool_limits(1):
        for n_train in (500, 1000, 2000, 3500):
            for rep in range(3):
                idx = rng.permutation(n)
                T, U = np.sort(idx[:n_train]), np.sort(idx[n_train:n_train + 300])
                yT = y[T]
                tracemalloc.start()
                t0 = time.perf_counter()
                vc = reml(G[np.ix_(T, T)], yT)
                m = KernelBLUP(G, vc.delta).fit(T, yT)
                yhat, dU = m.predict(U, return_d=True)
                t_fit = time.perf_counter() - t0
                t0 = time.perf_counter()
                pr = pool(G, vc.delta, T, yT, [te for _, te in KFold(5, shuffle=True, random_state=rep).split(T)])
                t_rand = time.perf_counter() - t0
                t0 = time.perf_counter()
                cl = KMeans(5, n_init=10, random_state=rep).fit_predict(pcs[T])
                pc = pool(G, vc.delta, T, yT, [np.flatnonzero(cl == c) for c in range(5)])
                t_clus = time.perf_counter() - t0
                t0 = time.perf_counter()
                lo, hi = kincp(FoldData(yhat=yhat, d=dU, s2g=vc.s2g, s2e=vc.s2e, pools=dict(rand=pr, clus=pc)), 0.10)
                t_int = time.perf_counter() - t0
                peak = tracemalloc.get_traced_memory()[1] / 2**20
                tracemalloc.stop()
                rows.append(dict(n_train=n_train, rep=rep, t_fit=t_fit, t_pool_rand=t_rand, t_pool_clus=t_clus,
                                 t_intervals=t_int, peak_mem_mb=peak, coverage=float(np.mean((y[U] >= lo) & (y[U] <= hi)))))
                print(rows[-1], flush=True)
    pd.DataFrame(rows).to_csv(RESULTS_DIR / "scaling.csv", index=False)


if __name__ == "__main__":
    main()
