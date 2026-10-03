"""One-command reproduction of the KinCP study.

  python run_all.py --mode quick   # pipeline check: 2 datasets, 1 trait each, few folds (~1 min);
                                   # writes to ../results_quick, ../figures_quick, ../tables_quick
  python run_all.py --mode full    # complete study (hours on 4 CPU cores; resumable)

Steps: download + verify data -> genotype preprocessing + data audit -> experiments -> aggregation +
statistics -> secondary analyses -> figures -> tables -> key numbers -> manuscript build.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent


def run(cmd, env):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=HERE, env=env)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--n-jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--skip-download", action="store_true")
    ap.add_argument("--skip-experiments", action="store_true", help="only re-aggregate existing job outputs")
    a = ap.parse_args()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(HERE / "src") + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("OMP_NUM_THREADS", "1")
    py = sys.executable
    datasets = ["oyster", "wheatG"] if a.mode == "quick" else None
    if a.mode == "quick":
        env["KINCP_RESULTS"] = str(PKG / "results_quick")
        env["KINCP_FIGURES"] = str(PKG / "figures_quick")
        env["KINCP_TABLES"] = str(PKG / "tables_quick")
        # the quick-mode simulation uses the pine genotypes
        datasets = ["oyster", "wheatG", "pine"]
    prep = [py, "scripts/prepare_data.py"] + (["--skip-download"] if a.skip_download else [])
    if datasets:
        prep += ["--datasets"] + datasets
    run(prep, env)
    if not a.skip_experiments:
        run([py, "experiments/run_experiments.py", "--mode", a.mode, "--n-jobs", str(a.n_jobs)], env)
    run([py, "scripts/aggregate.py", a.mode], env)
    run([py, "scripts/secondary_analyses.py"], env)
    run([py, "scripts/make_figures.py"], env)
    run([py, "scripts/make_tables.py"], env)
    if a.mode == "full":
        run([py, "scripts/key_numbers.py"], env)
        run([py, "scripts/build_manuscript.py"], env)
    print("done:", a.mode)


if __name__ == "__main__":
    main()
