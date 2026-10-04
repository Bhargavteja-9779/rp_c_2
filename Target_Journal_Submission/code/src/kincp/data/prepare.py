"""Build and cache genotype-derived objects for one dataset (genotypes only; no phenotypes used)."""
from __future__ import annotations

import numpy as np

from ..preprocessing.genomic import (gaussian_kernel_from_grm, grm_vanraden, kmeans_clusters,
                                     near_duplicates, standardized_relationship, top_pcs)
from ..utils import CACHE_DIR, STUDY, dump_json, get_logger
from .easygese import read_genotypes, read_phenotypes

log = get_logger("kincp.prepare")
THIN_MAX = STUDY["lightgbm"]["max_markers"]   # evenly spaced marker cap for LightGBM (deviation D2)
_CL = STUDY["genomic"]["clusters"]


def cache_path(name: str):
    p = CACHE_DIR / name
    p.mkdir(parents=True, exist_ok=True)
    return p


def prepare(name: str, k_clusters: int = _CL["k"], n_pcs: int = _CL["n_pcs"], cluster_seed: int = _CL["seed"],
            force: bool = False) -> dict:
    cp = cache_path(name)
    f = cp / "geno.npz"
    if f.exists() and not force:
        z = np.load(f, allow_pickle=True)
        return {k: z[k] for k in z.files}
    log.info("[%s] reading genotypes", name)
    ids, X = read_genotypes(name)
    Y = read_phenotypes(name)
    assert list(Y.index) == [str(i) for i in ids], "genotype/phenotype id order mismatch"
    log.info("[%s] X shape %s; building GRM", name, X.shape)
    G, Gs, m_used = grm_vanraden(X)
    pcs = top_pcs(Gs, n_pcs)
    clusters = kmeans_clusters(pcs, k_clusters, cluster_seed)
    Kg = gaussian_kernel_from_grm(G)
    step = max(1, X.shape[1] // THIN_MAX)
    Xthin = X[:, ::step][:, :THIN_MAX].copy()
    Gstd = standardized_relationship(G)
    dups = near_duplicates(Gstd, 0.95)
    out = dict(ids=ids, G=G, Kg=Kg, pcs=pcs, clusters=clusters, Xthin=Xthin)
    np.savez(f, **out)
    dump_json(dict(name=name, n=int(X.shape[0]), m_total=int(X.shape[1]), m_polymorphic=m_used,
                   m_thin=int(Xthin.shape[1]), cluster_sizes=np.bincount(clusters).tolist(),
                   n_near_duplicate_pairs=len(dups), near_duplicate_pairs=dups[:200],
                   mean_offdiag_G=float((G.sum() - np.trace(G)) / (G.shape[0] * (G.shape[0] - 1))),
                   mean_diag_G=float(np.trace(G) / G.shape[0])),
              cp / "geno_summary.json")
    return out


def load_X(name: str) -> np.ndarray:
    """Full genotype matrix (used only by the simulation study)."""
    cp = cache_path(name) / "X.npy"
    if cp.exists():
        return np.load(cp, mmap_mode="r")
    _, X = read_genotypes(name)
    np.save(cp, X)
    return X
