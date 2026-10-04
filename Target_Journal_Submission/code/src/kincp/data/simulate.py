"""Simulation of additive traits on real genotypes (known true genetic values)."""
from __future__ import annotations

import numpy as np


def simulate_trait(X: np.ndarray, h2: float, n_qtl: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    p = X.mean(axis=0, dtype=np.float64) / 2
    poly = np.flatnonzero((p > 0.01) & (p < 0.99))
    q = np.sort(rng.choice(poly, size=min(n_qtl, len(poly)), replace=False))
    beta = rng.normal(size=len(q))
    g = (np.asarray(X[:, q], dtype=np.float64) - 2 * p[q]) @ beta
    g = (g - g.mean()) / g.std() * np.sqrt(h2)
    e = rng.normal(size=len(g)) * np.sqrt(1 - h2)
    return g + e, g
