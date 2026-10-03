# Topic discovery and stress test (Phases 1–2)

These constraints narrowed the search space:
* **Target journal:** GENETICS (statistical genetics, genomic prediction, population genetics).
* **Compute:** 4 CPU cores, 15 GB RAM, no GPU.
* **Data:** must be public and downloadable.

## 1. Candidate directions screened (internal)

| # | Direction | Data | Main risk(s) | Verdict |
|---|---|---|---|---|
| 1 | Relatedness-aware (kinship-aware) conformal prediction intervals for genomic prediction | EasyGeSe (10 species, CC-BY) | Could be read as "applying CP"; prior art: CalGS (split CP, simulated data), CalPred/PredInterval (human PGS) | **Selected**, after the novelty defence below |
| 2 | Uncertainty-aware selection (risk-adjusted truncation selection) | EasyGeSe | Overlaps with Ahlinder & Waldmann 2026 (CVaR-OCS, GENETICS) | Merged into #1 as a secondary decision analysis (E9) |
| 3 | Learning-to-rank genomic selection | EasyGeSe | Prior art: Blondel et al. 2015 ranking approach to GS | Rejected: incremental |
| 4 | Domain-adaptive ML selective-sweep detection | msprime simulations | Prior art: Mo & Siepel 2023 domain-adaptive networks; crowded | Rejected |
| 5 | Calibrated neural posterior estimation for demography | simulations | Min et al. 2026 (GENETICS) neural posterior estimation; GPU-heavy | Rejected |
| 6 | G×E prediction with environmental covariates | G2F maize | MegaLMM (Hu et al. 2025), Washburn et al. 2025 competition; crowded | Rejected |
| 7 | Deep-learning genotype imputation | 1000G | Crowded; GPU | Rejected |
| 8 | PGS portability across ancestry | UK Biobank (restricted) | Data access | Rejected |
| 9 | Transfer across breeding cycles (temporal shift) | needs multi-cycle data | Few public multi-cycle datasets with dates | Rejected: data |
| 10 | Sparse / low-density marker panels for GS | EasyGeSe | Many prior studies; incremental | Rejected |
| 11 | Epistasis detection by interpreting ML genomic predictors | EasyGeSe | Weak ground truth; interpretation unreliable | Rejected |
| 12 | Calibration of local-ancestry inference | simulated admixture | Niche; weak genetics audience | Rejected |
| 13 | Variant-effect prediction (sequence models) | ENCODE etc. | GPU-bound | Rejected |
| 14 | Recombination-rate inference robustness (ReLERNN-type) | simulations | Prior work exists; GPU | Rejected |
| 15 | Introgression detection by CNN | simulations | Crowded (genomatnn, IntroUNET) | Rejected |
| 16 | Cross-validation design bias in GS (random vs. family CV) | EasyGeSe | Known since Werner et al. 2020 and earlier | Rejected as a standalone topic; used as the motivation of #1 (regimes R1/R2) |

## 2. Stress test of #1 (skeptical-editor questions)

* **Incremental?** Plain split conformal for GS exists (CalGS). The contribution is *not* conformal prediction itself. It is three things:
  1. the identification, theory and measurement of **relatedness to the training set** as the variable that breaks exchangeability in breeding deployments;
  2. a calibration design (relatedness-diverse cross-fitting pool) plus localisation in the classical PEV metric;
  3. a 10-species benchmark under deployment regimes, with a known-truth simulation and ablations.

  This differs in kind from CalGS, which uses marginal split conformal on simulated data.
* **Already solved?** In animal breeding, reliability and PEV theory (Henderson 1975; VanRaden 2008) gives model-based intervals. Whether these are calibrated across species, traits and deployment regimes, and with non-Gaussian, misspecified or nonlinear predictors, has not been established for 10 species. RKHS and LightGBM have no PEV at all. Gauss-PEV is therefore included as a **strong baseline**, not a straw man.
* **Simpler method enough?** This is tested directly. Gauss-PEV and CalPred-style parametric calibration are competitors, and the ablation removes every component.
* **Leakage risk?** The GRM uses genotypes only. Phenotype standardisation, REML and calibration use training folds only. Near-duplicate genotypes are audited and handled by a dedup sensitivity run.
* **Enough depth for a full article?**
  * 10 species, 24 traits;
  * 3 base predictors;
  * 3 deployment regimes;
  * 7 baselines and 7 ablations;
  * simulation with known truth;
  * cost, sensitivity and error analyses;
  * a selection-decision analysis.
* **Could the improvement disappear under proper testing?** Possibly. Endpoints and tests were fixed in advance (S0), and every result is reported whatever its direction.
