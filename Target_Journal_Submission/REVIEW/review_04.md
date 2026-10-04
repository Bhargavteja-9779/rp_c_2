# Review round 4 — Reviewer #4 (ML methodology, implementation correctness, code–manuscript consistency)

The reviewer read `src/kincp/**`, `experiments/run_experiments.py`, `scripts/*` and the Methods side by side. These points are new relative to Reviewers #1–3.

## MAJOR
**C1. Each training individual contributes two residuals to pool A.**
* *Problem:* Every training individual has one out-of-fold residual from the random scheme and one from the cluster scheme. The pool therefore contains dependent pairs. This weakens any exchangeability-based reading of the weighted quantile, beyond the subset-fit issue the authors already acknowledge.
* *Fix:* state it in the guarantee paragraph.

**C2. Interval centre versus calibration residuals.**
* *Problem:* KinCP centres the interval on the full-training-set prediction, while its residuals come from fold models. This is the "CV residual quantile" construction (as in PredInterval), not CV+. It has no CV+-type ≥1−2α guarantee.
* *Fix:* state it.

**C3. Methods ambiguity about which principal components define the inner clusters.**
* *Problem:* The code applies *k*-means to the *global* genotype principal components (computed from all genotyped individuals) restricted to the training individuals. The text ("principal components of the training individuals") could be read as re-computed PCs.
* *Fix:* clarify.

**C4. Configuration partly decorative.**
* *Problem:* `config/study.yaml` listed LightGBM, simulation, cluster and trait-rule settings that the code did not read; they were hard-coded instead. A user changing the config would silently not change the run.
* *Fix:* make the code read them, or mark them as documentation.

## MODERATE
1. *MD5 verification.* `download()` verified MD5 only for files it downloaded itself. Files obtained otherwise were checked only by size. Add an explicit verification of all files.
2. *Unit tests.* The tests do not cover CV+ coverage, the Mondrian variant or the CalPred-style calibration. Add them.
3. *Edge cases.* The SCP calibration set has a minimum of 10 individuals, and the bandwidth widening has an iteration cap (60 steps, i.e. up to 1.25⁶⁰ × h). Document both.
4. *Unused imports.* The manuscript builder had unused imports. This is cosmetic.

## MINOR
1. The LightGBM input thinning keeps evenly spaced columns of the raw dosage matrix, which can include monomorphic markers. These are harmless for trees, but say so.
2. Equation 1 matches `KernelBLUP.predict(return_d=True)`. This is verified by the unit test `test_kernel_blup_matches_closed_form`, which compares the code against an explicit matrix inverse.
3. Equation 2 matches `weighted_quantiles` (the test point's mass at +∞ enters the denominator). This is verified by `test_weighted_equals_unweighted_with_unit_weights`.

## Verified consistent (no change needed)
* Training-only standardisation.
* REML grid and Brent search.
* RKHS bandwidth by the median heuristic.
* The SCP 80/20 split.
* The CV+ order statistics.
* The CalPred-style likelihood.
* The normalisation σ(*d*).
* Inner fits reusing the outer δ (D3).
* The simulation design (QTL with MAF > 0.01, *N*(0, 1) effects, scaling to *h*²).
* The endpoint definitions, including quintiles pooled over repeats and folds.
* The interval-score formula.

---
# Author response and changes (Round 4)

| Issue | Action | Status |
|---|---|---|
| C1, C2 | The "Rationale and guarantees" paragraph now states both points explicitly. | Fixed |
| C3 | Methods clarified: global PCs restricted to the training individuals. | Fixed |
| C4 | The code now reads `lightgbm`, `simulation`, `genomic.clusters` and `data.trait_rule` from `config/study.yaml` (`kincp.models.base`, `kincp.data.prepare`, `kincp.data.easygese`, `experiments/run_experiments.py`). New test `test_config_is_read`. | Fixed |
| Moderate 1 | Added `kincp.data.easygese.verify_all()`. All 30 files match the Zenodo MD5 checksums (`results/data_md5_verification.json`). | Fixed (run) |
| Moderate 2 | Three tests added (CV+ coverage; Mondrian and CalPred-style bounds; config). The suite passes 12/12. | Fixed |
| Moderate 3 | Documented in Methods. | Fixed |
| Moderate 4 | Removed. | Fixed |
| Minor 1 | Documented. | Fixed |
