## Results

### Datasets, relatedness and predictive ability

The {{n_units}} traits came from datasets of {{n_individuals_min}} to {{n_individuals_max}} genotyped individuals and {{n_markers_min}} to {{n_markers_max}} polymorphic markers (Table 1). GBLUP predictive ability under random cross-validation ranged from {{r_min}} to {{r_max}} (median {{r_med}}). It fell to a median of {{r2_med}} under cluster-out validation. This is the familiar loss of accuracy for weakly related candidates (Habier *et al.* 2007; Clark *et al.* 2012; Werner *et al.* 2020).

Cluster-out candidates had systematically larger values of the relatedness covariate *d* than random-CV candidates (Figure 2b). Random cross-validation therefore under-represents the weakly related candidates for which uncertainty matters most.

Several panels contain many near-identical genotypes: {{dup_pairs_barley}} pairs above a standardised relationship of 0.95 in barley, {{dup_pairs_soybean}} in soybean and {{dup_pairs_lentil}} in lentil (Table 1).

### RQ1: standard intervals are miscalibrated along the relatedness axis

**Random cross-validation (R1).** Every method reached close to nominal *marginal* coverage. Mean coverage was {{kincp_R1_cov}} for KinCP, {{scp_R1_cov}} for split conformal (SCP), {{cvp_R1_cov}} for CV+ and {{pev_R1_cov}} for Gauss-PEV (Table 2). Marginal coverage hid a systematic pattern, however. Relatedness-blind intervals over-covered the candidates most closely related to the training set and under-covered the least related ones (Figure 3, left):
* SCP: {{scp_R1_q1}} in the closest quintile against {{scp_R1_q5}} in the most distant;
* CV+: {{cvp_R1_q1}} against {{cvp_R1_q5}}.

**Cluster-out validation (R2).** Here the problem became a failure of marginal coverage. Mean coverage was:
* {{scp_R2_cov}} for SCP;
* {{cvp_R2_cov}} for CV+;
* {{homo_R2_cov}} for homoscedastic Gaussian intervals;
* {{oof_R2_cov}} for the out-of-fold residual quantile (the PredInterval-like construction).

Coverage fell below 0.85 for {{scp_R2_nbelow85}} of {{n_units}} units with SCP and for {{cvp_R2_nbelow85}} with CV+ (Figure 4). The worst unit reached only {{cvp_R2_covmin}} with CV+. Because these methods calibrate on residuals of relatives that are closer than the candidates, their intervals were too narrow for new clusters. The shortfall was largest in the least-related quintile (Figure 3, middle).

**Gauss-PEV.** The model-based interval, which uses the same relatedness information through Eq. (1), adapted its width to relatedness and was well calibrated under R1 (conditional coverage error {{pev_R1_cond}}). Under R2 it under-covered on average ({{pev_R2_cov}}; conditional error {{pev_R2_cond}}). It was poorly calibrated for some units, with a minimum of {{pev_R2_covmin}} for {{pev_R2_minunit}}.

### RQ2: KinCP restores coverage, and the calibration pool is the decisive component

**Calibration of KinCP.** With GBLUP as the base predictor, KinCP had the lowest mean relatedness-conditional coverage error of the eight compared methods in every regime (Table 2): {{kincp_R1_cond}} under R1, {{kincp_R2_cond}} under R2 and {{kincp_R3_cond}} under R3. Under R2 its marginal coverage was {{kincp_R2_cov}} (SD over units {{kincp_R2_covsd}}; minimum {{kincp_R2_covmin}}). Its intervals were wider than those of the relatedness-blind conformal methods ({{kincp_R2_width}} *vs.* {{cvp_R2_width}} phenotypic SD for CV+), as required to reach coverage. **Interval score.** On the interval score, which trades width against misses (a proper scoring rule; Gneiting and Raftery 2007), KinCP was *not* better than the main alternatives. The mean scores were {{kincp_R2_is}} for KinCP and {{cvp_R2_is}} for CV+ under R2. The Holm-adjusted *P*-values were {{st_cvp_R2_is_p}} against CV+, {{st_pev_R2_is_p}} against Gauss-PEV and {{st_calp_R2_is_p}} against CalPred-style on pool A. KinCP was significantly better only than SCP (*P* {{st_scp_R2_is_p}}) and NormCP (*P* {{st_normcp_R2_is_p}}). Under R3, Gauss-PEV had a slightly lower interval score than KinCP (Holm *P* {{st_pev_R3_is_p}}). The intervals of relatedness-blind methods were narrower and missed more often, and the interval score weighs these two effects against each other. The benefit of KinCP is therefore *validity*: coverage close to the nominal level, including for weakly related candidates. It is not a better sharpness–coverage trade-off.

**Paired tests on the primary endpoint under R2** (Table 3; Figure 12). KinCP's conditional coverage error was lower than that of:
* CV+: median paired difference {{st_cvp_R2_cond_d}} (95% CI {{st_cvp_R2_cond_ci}}), Holm-adjusted *P* {{st_cvp_R2_cond_p}}, KinCP better in {{st_cvp_R2_cond_wins}} units;
* SCP: *P* {{st_scp_R2_cond_p}};
* Gauss-PEV: difference {{st_pev_R2_cond_d}}, 95% CI {{st_pev_R2_cond_ci}}, *P* {{st_pev_R2_cond_p}}, {{st_pev_R2_cond_wins}} units;
* NormCP: *P* {{st_normcp_R2_cond_p}};
* CalPred-style calibration fitted to a random pool: *P* {{st_calpr_R2_cond_p}}.

**Species-level analysis.** Treating species rather than traits as the unit (10 units; traits averaged within species) gave the same direction. Under R2, KinCP had a lower conditional error than CV+ in {{sp_cvp_R2_cond_wins}} species (unadjusted *P* {{sp_cvp_R2_cond_praw}}, Holm *P* {{sp_cvp_R2_cond_p}}) and than Gauss-PEV in {{sp_pev_R2_cond_wins}} species (unadjusted *P* {{sp_pev_R2_cond_praw}}, Holm *P* {{sp_pev_R2_cond_p}}). With 10 units and Holm adjustment over 21 comparisons, these species-level tests have limited power (Supplementary file statistics_species.csv).

**Pool A versus conformalisation.** KinCP did **not** differ from a CalPred-style heteroscedastic Gaussian calibration fitted to the *same* relatedness-diverse pool (pool A): difference {{st_calp_R2_cond_d}}, 95% CI {{st_calp_R2_cond_ci}}, *P* {{st_calp_R2_cond_p}}. The same parametric calibration fitted to a random pool did significantly worse. The main benefit therefore comes from the calibration pool, not from conformalisation as such. Under R1 the differences between methods were small in absolute terms, although KinCP remained significantly better than CV+ (*P* {{st_cvp_R1_cond_p}}) and SCP (*P* {{st_scp_R1_cond_p}}).

**Ablation** (Table 4; Figure 5). The ablation supports this interpretation:
* *Without component A* (random-fold pool only, B + C), the R2 conditional error rose from {{kincp_R2_cond}} to {{abA_R2_cond}} and coverage fell to {{abA_R2_cov}}. Under R1 the same variant was as good as the full method ({{abA_R1_cond}}): when deployment resembles random cross-validation, a random-fold pool already covers the relevant relatedness range.
* *Without localisation C* (A + B), the R2 error was {{abC_R2_cond}}.
* *Without normalisation B* (A + C), it was {{abB_R2_cond}}. Normalisation therefore contributed little once A and C were present, but it helped when C was absent: A only gave {{abBC_R2_cond}} under R2 and {{abBC_R1_cond}} under R1, where pooling without normalisation over-covered (coverage {{abBC_R1_cov}}).
* *With no component* (the out-of-fold quantile), the R2 error was {{oof_R2_cond}}.

**Robustness of the endpoint to the relatedness measure.** The primary endpoint bins candidates by *d*, which is also KinCP's localisation variable. We therefore repeated the analysis on quintiles of an independent measure: the maximum standardised genomic relationship of each candidate to the training set.
* *Under R2,* KinCP again had the smallest conditional error ({{mk_kincp_R2_cond}}, against {{mk_cvp_R2_cond}} for CV+ and {{mk_pev_R2_cond}} for Gauss-PEV). It was better than Gauss-PEV in {{mk_st_pev_R2_wins}} units (Holm *P* {{mk_st_pev_R2_p}}) and than CV+ in {{mk_st_cvp_R2_wins}} (Holm *P* {{mk_st_cvp_R2_p}}). It did not differ significantly from CalPred-style calibration on pool A (Holm *P* {{mk_st_calp_R2_p}}).
* *Under R1,* all methods were similar on this measure (KinCP {{mk_kincp_R1_cond}}, CV+ {{mk_cvp_R1_cond}}, Gauss-PEV {{mk_pev_R1_cond}}; all Holm *P* ≥ {{mk_st_cvp_R1_p_num}}). Relatedness-blind intervals still over-covered the candidates with the closest relatives in the training set (CV+ {{mk_cvp_R1_high}}).

KinCP's advantage under random cross-validation is therefore specific to calibration along *d* and is small. Its advantage under cluster-out deployment does not depend on how relatedness is measured.

**Remaining gap.** Even KinCP remained below nominal in the least-related quintile under R2 (worst-quintile coverage {{kincp_R2_worst}}). Its conditional error under R2 exceeded the error expected from binomial sampling alone ({{null_cond}}; see Methods).

### RQ3: robustness and generalisation

**Reduced training set (R3).** Halving the training set (R3) left the picture of R1 unchanged (Table 2). KinCP had a conditional error of {{kincp_R3_cond}}, against {{cvp_R3_cond}} for CV+ (*P* {{st_cvp_R3_cond_p}}) and {{pev_R3_cond}} for Gauss-PEV (*P* {{st_pev_R3_cond_p}}).

**Other base predictors** (Table 5; Figure 6). The pattern was the same for nonlinear predictors that have no prediction error variance of their own. KinCP used the GBLUP-derived *d* as the relatedness covariate:
* *RKHS regression, R2:* coverage {{rk_kincp_R2_cov}} for KinCP against {{rk_cvp_R2_cov}} for CV+ and {{rk_scp_R2_cov}} for SCP. Conditional errors were {{rk_kincp_R2_cond}} *vs.* {{rk_cvp_R2_cond}} (*P* {{st_rk_cvp_R2_cond_p}}).
* *LightGBM, R2:* coverage {{lg_kincp_R2_cov}} against {{lg_cvp_R2_cov}} and {{lg_scp_R2_cov}}. Conditional errors were {{lg_kincp_R2_cond}} *vs.* {{lg_cvp_R2_cond}} (*P* {{st_lg_cvp_R2_cond_p}}).
* As with GBLUP, KinCP and CalPred-style calibration on pool A did not differ for either predictor (RKHS *P* {{st_rk_calp_R2_cond_p}}; LightGBM *P* {{st_lg_calp_R2_cond_p}}).

{{sim_paragraph}}

{{granularity_paragraph}}

**Near-duplicate genotypes.** Removing near-duplicates did not change the conclusions (File S2, Table S_dedup). Under R2 KinCP covered {{dd_kincp_R2_cov}} and CV+ {{dd_cvp_R2_cov}}; under R1 the figures were {{dd_kincp_R1_cov}} and {{dd_cvp_R1_cov}}.

### RQ4: computational cost and sensitivity

**Cost** (Table 7; Figure 8). Building KinCP's two calibration pools requires ten additional model fits per training set. For the kernel models these inner fits reuse the outer-fold variance ratio and need only a Cholesky factorisation, whereas the single outer fit includes REML with an eigendecomposition. The median cost of both pools relative to one outer fit was {{rt_gb_ratio_med}}× for GBLUP, {{rt_rk_ratio_med}}× for RKHS and {{rt_lg_ratio_med}}× for LightGBM. For maize (about 3,500 training individuals), one GBLUP fit took {{rt_maize_fit}} s on one CPU thread and both pools {{rt_maize_pool}} s. Computing all interval methods from the pools took at most {{rt_interval_max}} s per fold. In a controlled benchmark on maize genotypes (Figure 8), with {{sc_n_max}} training individuals on one thread:
* one REML fit took {{sc_fit}} s;
* both pools took {{sc_pools}} s;
* the KinCP intervals for 300 candidates took {{sc_int}} s;
* peak memory was {{sc_mem}} MB.

Pool time grew with training-set size to the power {{sc_slope}}, and memory to the power {{sc_mslope}}. These exponents follow the dense *O*(*n*³) factorisations and *O*(*n*²) relationship matrices of GBLUP itself. The overhead is therefore that of a standard five-fold cross-validation run twice, and is small relative to phenotyping or genotyping costs.

**Sensitivity** (Table 8; Figure 9). KinCP was insensitive to its tuning choices:
* *Bandwidth multiplier* from 0.25 to 2: R2 conditional error {{sens_h025_R2_cond}} to {{sens_h2_R2_cond}}, against {{kincp_R2_cond}} at the default.
* *Mass floor:* without the floor, {{sens_fixed_R2_inf}} of R2 intervals were infinite. With n_min = 25 or 100 the conditional error was {{sens_n25_R2_cond}} and {{sens_n100_R2_cond}}.
* *Nominal level:* at 1 − α = 0.95 and 0.80, KinCP's R2 coverage was {{kincp_R2_cov_a05}} and {{kincp_R2_cov_a20}}, against {{cvp_R2_cov_a05}} and {{cvp_R2_cov_a20}} for CV+.

{{explore_paragraph}}

### RQ5: failure modes and selection decisions

**Error analysis** (Figure 10). Neither the excess kurtosis of the phenotype (Spearman ρ between kurtosis and KinCP R2 coverage = {{err_kincp_R2_kurt_rho}}, *P* {{err_kincp_R2_kurt_p}}) nor predictive ability (ρ with conditional error = {{err_kincp_R2_r_rho}}, *P* {{err_kincp_R2_r_p}}) explained KinCP's remaining errors. Its worst unit under R2 was {{err_kincp_R2_worst_unit}} (coverage {{err_kincp_R2_worst_cov}}).

Gauss-PEV's conditional error under R2 increased with the REML heritability of the trait (ρ = {{err_pev_R2_h2_rho}}, *P* {{err_pev_R2_h2_p}}; unadjusted, exploratory). Its worst unit was {{err_pev_R2_worst_unit}} (coverage {{err_pev_R2_worst_cov}}).

One explanation consistent with this pattern, which we did not test directly, is that variance components estimated within the training clusters overstate how much genetic signal transfers to a new cluster. Under that misspecification a model-based interval is too narrow, whereas an empirically calibrated interval adjusts. In the simulation, where the additive Gaussian model is correct by construction, Gauss-PEV was calibrated (see above).

**Selection** (Table 9; Figure 11). Among the top 10% of candidates by predicted value, KinCP's coverage under R2 was {{sel_kincp_R2_cov}}. The corresponding values were {{sel_cvp_R2_cov}} for CV+, {{sel_scp_R2_cov}} for SCP, {{sel_pev_R2_cov}} for Gauss-PEV and {{sel_calp_R2_cov}} for CalPred-style. The share of selected candidates falling below KinCP's lower bound was {{sel_kincp_R2_below}}, against a target of 0.05.

Ranking candidates by their lower bound instead of their predicted value did not increase the mean phenotype of the selected set, and under R1 it slightly reduced it. Under R1 the median difference was {{sel_kincp_R1_gaindiff}} phenotypic SD (*P* {{sel_kincp_R1_gainp}}); under R2 it was {{sel_kincp_R2_gaindiff}} (*P* {{sel_kincp_R2_gainp}}). The two rankings overlapped by a median of {{sel_kincp_R2_overlap}} under R2. Calibrated intervals therefore improve the validity of risk statements about selected candidates, but they do not by themselves change expected genetic gain.
