"""Build and execute all experiment jobs (E1-E9 share the same outer/inner cross-fitting engine).

usage: python experiments/run_experiments.py --mode quick|full [--n-jobs 4] [--only GBLUP,RKHS,...]
Outputs (one set per job, resumable):
  results/jobs/<job_id>__summary.csv   per method x alpha metrics (all alphas)
  results/jobs/<job_id>__timing.csv    per-fold timings, REML components, predictive ability
  results/jobs/<job_id>__records.parquet  per-individual intervals at alpha = 0.10
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kincp.data.easygese import DATASETS, eligible_traits, read_phenotypes  # noqa: E402
from kincp.evaluation.metrics import summarize  # noqa: E402
from kincp.utils import RESULTS_DIR, STUDY, environment_info, dump_json, get_logger  # noqa: E402

JOB_DIR = RESULTS_DIR / "jobs"
_SIM = STUDY["simulation"]
SIM_GENOS = tuple(_SIM["genotypes"])
SIM_H2 = tuple(_SIM["h2"])
SIM_NQTL = tuple(_SIM["n_qtl"])
SIM_REPS = tuple(range(1, _SIM["replicates"] + 1))


def job_specs(mode: str) -> list[dict]:
    specs = []
    if mode == "quick":
        for ds in ("oyster", "wheatG"):
            tr = eligible_traits(read_phenotypes(ds))[:1]
            for t in tr:
                specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="GBLUP", repeats=(1,), tag="main"))
                specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2", base="GBLUP", repeats=(1,), tag="main"))
                specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="RKHS", repeats=(1,), tag="main"))
        specs.append(dict(kind="sim", dataset="pine", h2=0.5, n_qtl=1000, rep=1, regime="R1", base="GBLUP"))
        return specs
    for ds in DATASETS:
        for t in eligible_traits(read_phenotypes(ds)):
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="GBLUP", repeats=(1, 2, 3, 4, 5), tag="main"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2", base="GBLUP", repeats=(1, 2, 3, 4, 5), tag="main"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R3", base="GBLUP", repeats=(1, 2, 3, 4, 5), tag="main"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="RKHS", repeats=(1,), tag="main"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2", base="RKHS", repeats=(1, 2), tag="main"))
            if ds != "maize":   # deviation D5: LightGBM on maize (n = 4,421) exceeds the CPU budget
                specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="LightGBM", repeats=(1,), tag="main"))
                specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2", base="LightGBM", repeats=(1,), tag="main"))
            for reg in ("R2k3", "R2k10"):   # Reviewer 5: deployment-cluster granularity
                specs.append(dict(kind="real", dataset=ds, trait=t, regime=reg, base="GBLUP", repeats=(1,), tag="granularity"))
            if ds == "oyster":                # Reviewer 5: real families (four F2 families)
                specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2fam", base="GBLUP", repeats=(1, 2, 3, 4, 5), tag="families"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="GBLUP", repeats=(1,), tag="explore"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2", base="GBLUP", repeats=(1,), tag="explore"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R1", base="GBLUP", repeats=(1,), tag="dedup"))
            specs.append(dict(kind="real", dataset=ds, trait=t, regime="R2", base="GBLUP", repeats=(1,), tag="dedup"))
    for g in SIM_GENOS:
        for h2 in SIM_H2:
            for nq in SIM_NQTL:
                for r in SIM_REPS:
                    for reg in ("R1", "R2"):
                        specs.append(dict(kind="sim", dataset=g, h2=h2, n_qtl=nq, rep=r, regime=reg, base="GBLUP"))
    return specs


def job_id(s: dict) -> str:
    if s["kind"] == "sim":
        return f"sim__{s['dataset']}__h{s['h2']}__q{s['n_qtl']}__r{s['rep']}__{s['regime']}"
    reps = "".join(map(str, s["repeats"]))
    return f"{s['base']}__{s['dataset']}__{s['trait']}__{s['regime']}__{s['tag']}__{reps}"


def _dedup_mask(dataset: str, thr: float = 0.95) -> np.ndarray:
    """Keep one individual per group of near-identical genotypes (standardised relationship > thr)."""
    from kincp.data.prepare import prepare
    from kincp.preprocessing.genomic import standardized_relationship
    G = prepare(dataset)["G"]
    S = standardized_relationship(G)
    n = len(S)
    keep = np.ones(n, bool)
    for i in range(n):
        if keep[i]:
            dup = np.flatnonzero(S[i, i + 1:] > thr) + i + 1
            keep[dup] = False
    return keep


def run_spec(s: dict) -> str:
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    from threadpoolctl import threadpool_limits

    from kincp.data.prepare import load_X
    from kincp.data.simulate import simulate_trait
    from kincp.training.runner import Job, run_job

    jid = job_id(s)
    out = JOB_DIR / f"{jid}__summary.csv"
    if out.exists():
        return f"skip {jid}"
    t0 = time.perf_counter()
    try:
        with threadpool_limits(limits=int(os.environ.get("KINCP_THREADS", "1"))):
            if s["kind"] == "sim":
                X = load_X(s["dataset"])
                seed = int(hashlib.sha256(jid.split("__R")[0].encode()).hexdigest()[:8], 16)
                y, g = simulate_trait(X, s["h2"], s["n_qtl"], seed)
                job = Job(s["dataset"], f"sim_h{s['h2']}_q{s['n_qtl']}", s["regime"], "GBLUP",
                          repeats=(s["rep"],), y_override=y, g_true=g, tag="sim")
            else:
                y_override = None
                if s["tag"] == "dedup":
                    y = read_phenotypes(s["dataset"])[s["trait"]].to_numpy(float).copy()
                    y[~_dedup_mask(s["dataset"])] = np.nan
                    y_override = y
                job = Job(s["dataset"], s["trait"], s["regime"], s["base"], repeats=tuple(s["repeats"]),
                          y_override=y_override, tag=s["tag"])
            rec, tim = run_job(job)
        summ = summarize(rec)
        if s["kind"] == "sim":
            summ["h2"], summ["n_qtl"], summ["sim_rep"] = s["h2"], s["n_qtl"], s["rep"]
            tim["h2"], tim["n_qtl"], tim["sim_rep"] = s["h2"], s["n_qtl"], s["rep"]
        tim["wall_job"] = time.perf_counter() - t0
        tim.to_csv(JOB_DIR / f"{jid}__timing.csv", index=False)
        keep = rec[rec["alpha"] == 0.10]
        float_cols = keep.select_dtypes("float64").columns
        keep = keep.astype({c: "float32" for c in float_cols})
        keep.to_parquet(JOB_DIR / f"{jid}__records.parquet", index=False)
        summ.to_csv(out, index=False)    # written last = completion marker
        return f"done {jid} {time.perf_counter() - t0:.1f}s"
    except Exception:
        (JOB_DIR / f"{jid}__ERROR.txt").write_text(traceback.format_exc())
        return f"ERROR {jid}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--n-jobs", type=int, default=max(1, (os.cpu_count() or 1)))
    ap.add_argument("--only", default="", help="comma list of bases/kinds to run (GBLUP,RKHS,LightGBM,sim)")
    ap.add_argument("--datasets", default="", help="comma list of datasets")
    a = ap.parse_args()
    JOB_DIR.mkdir(parents=True, exist_ok=True)
    log = get_logger("kincp.run", RESULTS_DIR / "experiment_logs" / f"run_{a.mode}.log")
    dump_json(environment_info(), RESULTS_DIR / "experiment_logs" / "environment.json")
    specs = job_specs(a.mode)
    if a.only:
        sel = set(a.only.split(","))
        specs = [s for s in specs if (s["kind"] == "sim" and "sim" in sel) or (s["kind"] == "real" and s["base"] in sel)]
    if a.datasets:
        dsel = set(a.datasets.split(","))
        specs = [s for s in specs if s["dataset"] in dsel]
    # largest jobs first for better load balance
    size = {"maize": 9, "barley": 5, "pig": 4, "pine": 3}
    specs.sort(key=lambda s: -size.get(s["dataset"], 1) * (3 if s.get("base") == "LightGBM" else 1))
    log.info("running %d jobs (%s) with %d workers", len(specs), a.mode, a.n_jobs)
    from joblib import Parallel, delayed
    for msg in Parallel(n_jobs=a.n_jobs, return_as="generator_unordered", verbose=0)(delayed(run_spec)(s) for s in specs):
        log.info(msg)


if __name__ == "__main__":
    main()
