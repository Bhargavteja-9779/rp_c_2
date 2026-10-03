# Novelty map (Phase 4)

| Existing work | Its contribution | What KinCP does differently |
|---|---|---|
| VanRaden 2008; Henderson 1975 (PEV / reliability) | Model-based individual prediction-error variances | KinCP keeps PEV only as a *covariate* (d) and *normaliser*. Its coverage does not rely on Gaussian likelihood, additivity, or correct variance components, and it works around any base predictor, including those without a PEV. Gauss-PEV is evaluated as a baseline. |
| Habier 2007; Clark 2012; Pszczola 2012; Wientjes 2013 | Accuracy and reliability fall as relatedness to the reference set falls | We turn this descriptive knowledge into a calibration mechanism and *measure* coverage as a function of relatedness across 10 species. |
| CalGS (Kumar; split CP for GS) | Marginal split-conformal intervals; simulated data | KinCP adds three components: (A) relatedness-diverse cross-fitted calibration pools, (B) PEV-normalised scores, (C) localisation in the PEV metric. It is evaluated on real data from 10 species, under cluster-out deployment, with ablations. |
| CalPred (Hou et al. 2024) | Parametric heteroscedastic calibration over contexts in human PGS | KinCP is conformal (distribution-free quantiles) and targets related breeding populations. A "CalPred-style" calibration on the same pool is included as a competitor, to separate the effect of the pool from that of conformalisation. |
| PredInterval (Xu et al. 2025) | Quantiles of CV residuals; marginal calibration | Equals our ablation KinCP-ABC (random-fold out-of-fold residual quantile). The paper shows where this fails (distant relatives, cluster-out deployment). |
| Weighted / localized CP (Tibshirani 2019; Guan 2023; Barber 2023) | General theory under covariate shift / localisation | We supply the genetics-specific covariate (PEV d), a calibration-pool design that makes the covariate shift assumption plausible, and an empirical test. We do not claim a new general CP theorem. |
| Ahlinder & Waldmann 2026 | Uses Bayesian posterior uncertainty in selection | We examine whether uncertainty statements are *calibrated*, and how calibration affects selection decisions (E9). |

**Claim boundary.** We do **not** claim to be the first to apply conformal prediction to genomic prediction (CalGS exists). We claim:
* the first multi-species evaluation of relatedness-conditional calibration of genomic-prediction intervals, to our knowledge;
* a kinship-aware conformal procedure.

Patent / technical-disclosure search: a web search for "conformal prediction genomic selection kinship" (2026-10-03) found no patents or disclosures.
