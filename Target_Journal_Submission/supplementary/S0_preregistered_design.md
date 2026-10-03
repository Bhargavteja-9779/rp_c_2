# Pre-specified research design (written before any model was fitted)

Date fixed: 2026-10-03. Git commit time-stamps this document before any experiment is run.
Every later deviation is listed in `supplementary/S9_deviations.md`.

## 1. Problem
Breeders use genomic predictions to choose which candidates to keep. A useful prediction needs an honest statement of uncertainty, and the reliability of a prediction depends strongly on how closely the candidate is related to the training (reference) population. This is classical quantitative genetics: prediction error variance (PEV), reliability, and Habier/Clark/Pszczola-type relatedness effects.

Current uncertainty statements come in four kinds:
* model-based Gaussian intervals from the PEV of the mixed model;
* Bayesian posterior predictive intervals;
* recently, split-conformal intervals (CalGS, a preprint on simulated data);
* in human polygenic scores, context-calibrated intervals (CalPred, Hou et al. 2024) and cross-validation residual quantiles (PredInterval).

Split and CV conformal guarantees assume exchangeability between calibration and deployment individuals. In breeding, deployment candidates often come from new families or sub-populations. Their relatedness to the training set therefore differs systematically from that of a random calibration hold-out, which breaks exchangeability. Model-based intervals do adapt to relatedness through PEV, but they rely on correct model assumptions: Gaussianity, additivity, and correctly estimated variance components.

## 2. Hypothesis
Relatedness to the training set, summarised for each candidate by its GBLUP prediction error variance in σ²_g units (`d`), is the main axis along which genomic-prediction uncertainty statements become miscalibrated.

A conformal procedure that does three things will give near-nominal coverage that is both marginal and relatedness-conditional, across deployment regimes and species, at modest cost:
* (A) builds a calibration pool covering the relevant relatedness range, using residuals from both random-fold and cluster-fold cross-fitting inside the training set;
* (B) normalises nonconformity scores by the PEV-implied predictive standard deviation;
* (C) localises the conformal quantile in `d` (kernel weighting).

The proposed method is called **KinCP** (kinship-aware conformal prediction).

## 3. Research questions → experiments
| RQ | Question | Experiments |
|---|---|---|
| RQ1 | How miscalibrated are standard genomic-prediction intervals across relatedness levels and deployment regimes? | E1, E2 |
| RQ2 | Does KinCP restore marginal and relatedness-conditional coverage, and which components are responsible? | E1, E2, E3 |
| RQ3 | Does this hold across species, traits, base predictors, training-set sizes and simulated genetic architectures with known truth? | E4, E5 |
| RQ4 | What does it cost computationally, and how sensitive is it to its tuning choices? | E6, E7 |
| RQ5 | Where does it fail, and does calibrated uncertainty change selection decisions? | E8, E9 |

## 4. Data
EasyGeSe (Quesada-Traver et al. 2025, BMC Genomics; Zenodo 10.5281/zenodo.15348871; CC-BY 4.0). Ten species: barley, common bean, lentil, loblolly pine, eastern oyster, maize, pig, rice, soybean, wheat. Genotypes and phenotypes are used exactly as distributed.

**Trait selection rule (fixed in advance; does not look at results).** A trait is eligible if it has ≥200 non-missing records and ≥30 distinct values, i.e. it is quasi-continuous. Within each dataset we take up to **3** eligible traits, chosen by largest non-missing n. Ties are broken by column order in the distributed file.

## 5. Deployment regimes
* **R1 Random:** the five EasyGeSe "Split1–5 × CV" 5-fold assignments, i.e. 5 repeats × 5 folds.
* **R2 Cluster-out:** leave-one-genomic-cluster-out. Clusters come from k-means (k = 5, seed 2026, 10 restarts) on the top 10 principal components of the standardised genotype matrix. This uses genotypes only and never looks at phenotypes.
* **R3 Reduced training:** R1 folds with the training set subsampled to 50% (seeded).

## 6. Base predictors
* GBLUP: VanRaden GRM, REML via eigendecomposition. This is the primary predictor.
* RKHS: Gaussian-kernel ridge, median-heuristic bandwidth, λ chosen by internal GCV.
* LightGBM: fixed default-style hyper-parameters, decided in advance (500 trees, learning rate 0.05, 31 leaves, colsample 0.3). No tuning on test folds.

## 7. Uncertainty methods (nominal 1−α = 0.90; α ∈ {0.05, 0.10, 0.20} for sensitivity)
1. **Gauss-PEV:** GBLUP model-based interval ŷ ± z·sqrt(σ²_g·d + σ²_e). GBLUP only.
2. **Gauss-homosc:** ŷ ± z·SD of out-of-fold training residuals.
3. **SCP:** split conformal, with a random 20% calibration hold-out from the training set.
4. **CV+:** cross-conformal / CV+ (Barber et al. 2021), K = 5 random folds.
5. **CalPred-style:** heteroscedastic Gaussian with log σ linear in `d`, fitted by maximum likelihood to out-of-fold residuals.
6. **NormCP:** split conformal with scores normalised by sqrt(σ²_g·d + σ²_e), random calibration. This is component B alone.
7. **KinCP (proposed):** components A + B + C.

**Ablations** (E3): KinCP with one or two of A, B, C removed, giving all 7 non-empty sub-combinations plus none (≈ CV+).

## 8. Endpoints (pre-specified)
* **Primary 1:** relatedness-conditional coverage error. Test individuals in each dataset × trait × regime are pooled over folds, binned into quintiles of `d`, and we report the mean over quintiles of |coverage_q − 0.90|.
* **Primary 2:** marginal coverage deviation |coverage − 0.90|.
* **Primary 3:** mean interval score (Winkler) divided by the trait's phenotypic SD.
* **Secondary:** mean width divided by SD; worst-quintile coverage; runtime.

## 9. Statistics
* **Unit of analysis:** the dataset × trait combination, crossed with regime.
* **Paired comparisons** of KinCP against each competitor: two-sided Wilcoxon signed-rank test with Holm correction within each endpoint family. Effect sizes are the median paired difference with a 95% bootstrap CI (10,000 resamples) and the matched-pairs rank-biserial correlation.
* **Seeds:** stochastic components use seeds {11, 22, 33, 44, 55}, fixed in advance. Results are reported as mean ± SD over seeds, and the best seed is never selected.

## 10. Simulation with known truth (E5b)
* Real genotypes from pine, pig and maize.
* Additive traits simulated with h² ∈ {0.2, 0.5, 0.8} and n_QTL ∈ {10, 1000}, with effects normally distributed.
* Five replicates.
* Phenotype coverage is evaluated together with diagnostics against the true genetic value.

## 11. Leakage controls
* Phenotype standardisation, REML variance components, hyper-parameters and calibration scores all use training individuals only.
* Building the GRM from all genotypes is allowed: candidate genotypes are known at selection time and no phenotypes are involved. This is stated explicitly.
* Duplicate or near-identical genotypes (standardised relationship > 0.95 between distinct individuals) are reported, and a sensitivity analysis removes them.
