"""Genotype-only preprocessing: genomic relationship matrices, principal components, clusters.

Everything here uses genotypes only (no phenotypes), so it may use all individuals, including
future selection candidates, whose genotypes are known at selection time.
"""
from __future__ import annotations

import numpy as np
from sklearn.cluster import KMeans


def allele_freq(X: np.ndarray) -> np.ndarray:
    return X.mean(axis=0, dtype=np.float64) / 2.0


def grm_vanraden(X: np.ndarray, chunk: int = 20000) -> tuple[np.ndarray, np.ndarray, int]:
    """VanRaden (2008) method-1 GRM and the standardised-genotype relationship matrix.

    G  = Z Z' / (2 sum p(1-p)),  Z = X - 2p
    Gs = Zs Zs' / m,             Zs = Z / sqrt(2p(1-p))
    Monomorphic markers are dropped. Computed in marker chunks (float32 products, float64 accumulators).
    """
    p = allele_freq(X)
    keep = (p > 0) & (p < 1)
    idx = np.flatnonzero(keep)
    n = X.shape[0]
    G = np.zeros((n, n))
    Gs = np.zeros((n, n))
    denom = 2.0 * np.sum(p[idx] * (1 - p[idx]))
    for s in range(0, len(idx), chunk):
        j = idx[s:s + chunk]
        Z = X[:, j].astype(np.float32) - (2 * p[j]).astype(np.float32)
        G += (Z @ Z.T).astype(np.float64)
        Zs = Z / np.sqrt(2 * p[j] * (1 - p[j])).astype(np.float32)
        Gs += (Zs @ Zs.T).astype(np.float64)
    G /= denom
    Gs /= len(idx)
    return G, Gs, int(len(idx))


def top_pcs(Gs: np.ndarray, k: int = 10) -> np.ndarray:
    w, V = np.linalg.eigh(Gs)
    order = np.argsort(w)[::-1][:k]
    return V[:, order] * np.sqrt(np.maximum(w[order], 0))


def kmeans_clusters(pcs: np.ndarray, k: int = 5, seed: int = 2026) -> np.ndarray:
    return KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(pcs)


def gaussian_kernel_from_grm(G: np.ndarray) -> np.ndarray:
    """Gaussian (RKHS) kernel from squared genomic distances D2_ij = G_ii + G_jj - 2 G_ij,
    bandwidth set by the median heuristic over off-diagonal pairs (genotype-only)."""
    dg = np.diag(G)
    D2 = np.maximum(dg[:, None] + dg[None, :] - 2 * G, 0)
    iu = np.triu_indices_from(D2, 1)
    med = np.median(D2[iu])
    return np.exp(-D2 / med)


def standardized_relationship(G: np.ndarray) -> np.ndarray:
    dg = np.sqrt(np.maximum(np.diag(G), 1e-12))
    return G / dg[:, None] / dg[None, :]


def max_kinship_to(Gstd: np.ndarray, test: np.ndarray, train: np.ndarray) -> np.ndarray:
    return Gstd[np.ix_(test, train)].max(axis=1)


def near_duplicates(Gstd: np.ndarray, thr: float = 0.95) -> list[tuple[int, int]]:
    iu = np.triu_indices_from(Gstd, 1)
    m = Gstd[iu] > thr
    return list(zip(iu[0][m].tolist(), iu[1][m].tolist()))
