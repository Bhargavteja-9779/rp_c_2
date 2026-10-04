# KinCP: kinship-aware conformal prediction intervals for genomic prediction

This repository is the complete code for the manuscript *"Relatedness-aware calibration of genomic prediction intervals: kinship-aware conformal prediction across ten plant and animal species"*, prepared for GENETICS. Every number, table and figure in the manuscript is regenerated from public data by one command.

## 1. Installation
```bash
python3.11 -m venv .venv && source .venv/bin/activate      # or: conda env create -f environment.yml
pip install -r requirements.txt
```
* No GPU is needed. Everything runs on CPU with NumPy/SciPy.
* `kincp.utils.detect_device()` records whether CUDA or Apple MPS is present. The statistical pipeline does not use either.
* Tested on Linux x86-64 (4 cores, 16 GB RAM) with Python 3.11.15.

## 2. Data
* The study uses the ten EasyGeSe datasets (Quesada-Traver et al. 2025, *BMC Genomics* 26:953; Zenodo record [15348871](https://zenodo.org/records/15348871); licence CC-BY 4.0).
* `scripts/prepare_data.py` downloads every file, checks it against the Zenodo MD5 checksums, and writes the data/leakage audit to `results/data_audit.json`.
* Download size is about 2.5 GB, mostly the maize and barley genotype files.
* To place the data elsewhere, set `KINCP_DATA=/path` (the default is `code/data/`).

## 3. Reproduce everything
```bash
python run_all.py --mode quick    # ~2 min: pipeline check on 2 datasets (writes ../results_quick etc.)
python run_all.py --mode full     # complete study; resumable (finished jobs are skipped)
```
The full mode runs these steps in order:
1. data download and audit;
2. all experiment jobs (`experiments/run_experiments.py`): about 600 jobs, roughly 6–8 h on 4 cores, of which LightGBM accounts for most of the time;
3. aggregation and pre-specified statistics (`scripts/aggregate.py`);
4. error and selection analyses (`scripts/secondary_analyses.py`);
5. figures (`scripts/make_figures.py`);
6. tables (`scripts/make_tables.py`);
7. the manuscript numbers file (`scripts/key_numbers.py`);
8. the manuscript itself (`scripts/build_manuscript.py`).

To re-create only the outputs from existing job results:
```bash
python run_all.py --mode full --skip-download --skip-experiments
```

## 4. Where each result comes from
| Output | Produced by | Manuscript |
|---|---|---|
| `results/jobs/<job>__summary.csv` | `kincp.training.runner.run_job` + `kincp.evaluation.metrics.summarize` | all |
| `results/raw_results.csv` | `scripts/aggregate.py` (all jobs × methods × α) | Tables 2, 4–6, 8 |
| `results/statistics.json`, `results/statistics_table.csv` | `scripts/aggregate.py` (Wilcoxon, Holm, bootstrap CI, rank-biserial) | Table 3, Figure 12 |
| `results/metrics.json` | `scripts/aggregate.py` (medians per base/regime/method) | text |
| `results/timings.csv` | runner timings and REML components | Table 7, Figure 8 |
| `results/error_analysis*.{csv,json}`, `results/decision_*` | `scripts/secondary_analyses.py` | Figures 10–11, Table 9 |
| `results/key_numbers.json` | `scripts/key_numbers.py` | every number in the text |
| `figures/Fig*.pdf/png` | `scripts/make_figures.py` | Figures 1–12 |
| `tables/*.csv/md` | `scripts/make_tables.py` | Tables 1–9, S-tables |

## 5. Code map
```
src/kincp/
  data/easygese.py          download (md5-verified), loading, EasyGeSe folds, trait-selection rule
  data/prepare.py           GRM, principal components, k-means clusters, RKHS kernel, marker thinning (cached)
  data/simulate.py          additive traits on real genotypes (known genetic values)
  preprocessing/genomic.py  VanRaden GRM, PCs, clusters, near-duplicate detection
  models/kernel_blup.py     REML (spectral), kernel BLUP, PEV-based relatedness covariate d (Eq. 1)
  models/base.py            GBLUP, RKHS, LightGBM behind one interface
  conformal/methods.py      Gauss-PEV, Gauss-homosc, SCP, NormCP, CV+, CalPred-style, KinCP + ablations
  training/runner.py        outer folds (R1/R2/R3) × inner cross-fitting pools × all methods
  evaluation/metrics.py     coverage, quintile-conditional coverage, width, interval score
  statistics/tests.py       Wilcoxon signed-rank, Holm, bootstrap CI, rank-biserial
experiments/run_experiments.py   job list (quick/full), parallel, resumable
scripts/                         data prep, aggregation, analyses, figures, tables, numbers, manuscript
tests/test_core.py               unit tests (pytest -q)
config/study.yaml                seeds, α levels, inner-fold settings, KinCP bandwidth/floor
```

## 6. Using KinCP on your own data
```python
from kincp.models.kernel_blup import reml, KernelBLUP
from kincp.conformal.methods import FoldData, kincp
# see kincp.training.runner.run_job for the complete recipe:
# 1) REML on the training set -> s2g, s2e, delta;
# 2) random and genomic-cluster 5-fold cross-fitting inside the training set -> pools of (residual, d);
# 3) d for candidates with KernelBLUP(G, delta).fit(T, y).predict(U, return_d=True);
# 4) lo, hi = kincp(FoldData(yhat, d, s2g, s2e, pools), alpha=0.10)
```

## 7. Tests
```bash
pytest -q        # 9 tests: GRM, REML recovery, BLUP/PEV closed form, conformal quantiles, KinCP coverage
```

## 8. Determinism
* Seeds {11, 22, 33, 44, 55} are fixed in `config/study.yaml` and tied to repeats.
* k-means uses seed 2026.
* BLAS threads are limited to 1 per job.
* Results are deterministic for a given platform and library versions. Floating-point differences across BLAS builds can change the last digits.

## 9. Licence
Code: MIT. Data: CC-BY 4.0 (EasyGeSe); cite the original data sources listed in the manuscript.
