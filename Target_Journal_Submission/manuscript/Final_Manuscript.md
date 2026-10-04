# Kinship-aware conformal prediction intervals for genomic prediction across ten plant and animal species

**Running title:** Kinship-aware genomic prediction intervals

[Author names to be inserted]¹

¹[Affiliation to be inserted]

**Corresponding author:** [Name, address, e-mail to be inserted]

**Keywords:** genomic prediction; genomic selection; prediction interval; conformal prediction; prediction error variance; genomic relationship; uncertainty quantification; GBLUP; Genomic Prediction

## Abstract

Genomic prediction guides selection in plant and animal breeding, but breeders acting on an individual prediction also need honest uncertainty. Distribution-free conformal prediction intervals assume that calibration individuals are exchangeable with selection candidates; we show that relatedness to the training population breaks this assumption. We measure each candidate's relatedness by the prediction error variance of genomic best linear unbiased prediction and propose kinship-aware conformal prediction, which calibrates on residuals from random and genomic-cluster cross-fitting, normalises them by this variance and localises the conformal quantile in relatedness. We compared it with seven alternatives on 24 traits from barley, common bean, lentil, loblolly pine, eastern oyster, maize, pig, rice, soybean and wheat, under random and cluster-out validation, with three prediction models, and in simulations on real genotypes. Intervals ignoring relatedness over-covered close relatives and under-covered distant candidates; for held-out clusters, split-conformal and cross-validation-plus intervals covered 0.828 and 0.838 of phenotypes at nominal 0.90, and the classical Gaussian interval 0.881. Kinship-aware intervals covered 0.894, with relatedness-conditional coverage error 0.036 against 0.079 for cross-validation-plus and 0.052 for the Gaussian interval, and the smallest or joint-smallest error for all three predictors. The gains were in calibration, not in interval score. Ablation showed that the calibration pool spanning distant relatives was decisive: a parametric calibration fitted to the same pool performed equally well. Prediction intervals for selection candidates should be calibrated along the relatedness axis, at the cost of about ten additional model fits.

## Article summary

Breeders need honest uncertainty for genomic predictions of individual selection candidates. We show that standard distribution-free prediction intervals become unreliable for candidates that are weakly related to the training population, because they are calibrated on close relatives. Using the classical prediction error variance as a measure of relatedness, we propose a kinship-aware calibration that draws calibration residuals from both close and distant relatives. Across ten plant and animal species, three prediction models and a simulation, it restored near-nominal coverage across relatedness levels, whereas standard intervals covered as little as 0.838 of phenotypes on average for new genomic clusters.

## Introduction

Genomic prediction uses genome-wide markers to predict the genetic merit or future phenotype of individuals that have been genotyped but not yet phenotyped (Meuwissen *et al.* 2001). It is now routine in animal and plant breeding (Crossa *et al.* 2017). Its methodological literature is dominated by point accuracy: the correlation between predicted and observed values, usually estimated by cross-validation. Selection decisions are made on individual candidates, however, and the reliability of an individual prediction varies widely. Two candidates with the same predicted value can carry very different risks. Uncertainty statements that are correct for the candidates actually being selected are therefore a prerequisite for risk-aware selection. Such approaches are beginning to appear; for example, Ahlinder and Waldmann (2026) propagate Bayesian posterior uncertainty into optimum contribution selection.

Quantitative genetics has long recognised that relatedness to the training population is the main determinant of individual prediction reliability. Accuracy decreases as the relationship between a candidate and the reference population decreases (Habier *et al.* 2007; Clark *et al.* 2012; Pszczola *et al.* 2012), and family relationships matter more than linkage disequilibrium *per se* (Wientjes *et al.* 2013). Random cross-validation in structured populations therefore overstates the accuracy expected for new families or sub-populations (Werner *et al.* 2020). In mixed-model theory these effects are summarised by the prediction error variance (PEV) of best linear unbiased prediction (Henderson 1975; VanRaden 2008). The PEV yields model-based Gaussian intervals whose width grows as relatedness falls. These intervals are correct only if the linear mixed model, its Gaussian assumptions and its variance components are correct. They are also unavailable for nonlinear or machine-learning predictors.

Conformal prediction offers intervals with finite-sample coverage guarantees for any predictor (Vovk *et al.* 2022; Lei *et al.* 2018; Angelopoulos and Bates 2023). The guarantee rests on exchangeability between calibration residuals and the residual of the new observation. Conformal and related calibrated intervals have recently been proposed for polygenic scores in human populations (Sun *et al.* 2021; Hou *et al.* 2024; Xu *et al.* 2025; Kodji *et al.* 2026). Some of these use group-conditional (Mondrian) calibration across ancestry groups (Sun *et al.* 2021; Kodji *et al.* 2026). Split-conformal intervals have been suggested for genomic selection on simulated data (Kumar 2026). In human polygenic scores, accuracy decays continuously with the genetic distance of an individual from the training data (Ding *et al.* 2023). This motivated context-specific calibration (Hou *et al.* 2024). Breeding populations are more extreme. They consist of families and closely related lines, and in the scenarios that matter most the selection candidates belong to new crosses, new families or new sub-populations. A calibration hold-out drawn at random from the training population is then systematically more closely related to the remaining training individuals than the candidates are. Exchangeability fails along a known and measurable axis: relatedness to the training set. The statistical literature provides general tools for this situation:
* normalised or locally weighted scores (Papadopoulos *et al.* 2002; Lei *et al.* 2018);
* weighted conformal prediction under covariate shift (Tibshirani *et al.* 2019; Barber *et al.* 2023);
* localized conformal prediction (Guan 2023);
* group-conditional and hierarchical guarantees (Vovk 2013; Dunn *et al.* 2023; Bhattacharyya and Barber 2026);
* conditional guarantees over function classes (Gibbs *et al.* 2025).

These tools must be given the right covariate and a calibration design in which their assumptions are plausible.

Here we connect these two lines of work. We use the GBLUP prediction error variance, scaled by the genetic variance, as a genotype-only measure of each candidate's genomic relatedness to the training set (we call the approach "kinship-aware", where kinship refers to genomic relationships). We propose kinship-aware conformal prediction (KinCP), which has three components:
* (A) a calibration pool of out-of-fold residuals from random and genomic-cluster cross-fitting, spanning close and distant relatives;
* (B) nonconformity scores normalised by the PEV-implied predictive standard deviation;
* (C) localisation of the conformal quantile in the relatedness metric.

Throughout, intervals are for the phenotype a candidate will express, which is the quantity breeders observe when validating predictions. The relatedness covariate is also shown, by simulation, to calibrate the error of the genetic-value prediction. We regard the calibration design as the main contribution: a relatedness-diverse calibration pool together with the PEV covariate. KinCP is its distribution-free implementation. The conformal components themselves are established tools; what is new is:
* the identification and measurement of relatedness as the variable along which genomic-prediction intervals lose calibration;
* a calibration-pool design that makes the relevant shift assumption plausible without phenotypes of the candidates;
* a pre-specified, multi-species evaluation.

We do not claim a new conformal theorem, nor superiority over a parametric calibration fitted to the same pool.

We evaluate KinCP against seven alternatives across ten plant and animal species from the EasyGeSe resource (Quesada-Traver *et al.* 2025). The design covers three deployment regimes, three base predictors, an ablation of every component, and a simulation on real genotypes with known genetic values. It addresses five questions:
* RQ1: how miscalibrated are standard intervals across relatedness levels and deployment regimes?
* RQ2: does KinCP restore marginal and relatedness-conditional coverage, and which components are responsible?
* RQ3: does this hold across species, traits, predictors and genetic architectures?
* RQ4: what does it cost, and how sensitive is it to its tuning choices?
* RQ5: where does it fail, and how does calibration affect selection?

The design, endpoints and statistical tests were fixed before any model was fitted (File S1).

## Materials and methods

### Data

We used the ten datasets of EasyGeSe (Quesada-Traver *et al.* 2025; Zenodo record 15348871; licence CC-BY 4.0) exactly as distributed. EasyGeSe documents their original sources and quality control. They comprise:
* barley (*Hordeum vulgare*);
* common bean (*Phaseolus vulgaris*);
* lentil (*Lens culinaris*; Haile *et al.* 2020);
* loblolly pine (*Pinus taeda*; Resende *et al.* 2012);
* eastern oyster (*Crassostrea virginica*);
* maize (*Zea mays*; Washburn *et al.* 2025);
* pig (*Sus scrofa*);
* rice (*Oryza sativa*; Zhao *et al.* 2011);
* soybean (*Glycine max*; Kaler *et al.* 2017);
* wheat (*Triticum aestivum*; Gogna *et al.* 2022).

Genotypes were recoded as allele dosages 0/1/2. The wheat file, coded −2/0/2, was shifted to this scale; inbred panels coded 0/2 were kept as is. Monomorphic markers were dropped. No further marker filtering or imputation was applied. All 30 files were verified against the Zenodo MD5 checksums.

Traits were selected by a rule fixed in advance that does not look at results. A trait was eligible if it had at least 200 phenotyped individuals and at least 30 distinct values. Within each dataset we took up to three eligible traits with the largest number of records, breaking ties by column order. This gave 24 dataset × trait units (Table 1).

Near-duplicate genotypes, defined as distinct individuals with a standardised genomic relationship above 0.95, were counted. A sensitivity analysis retained only one individual from each near-duplicate group.

### Genomic relationships

Let *X* be the *n* × *m* dosage matrix, *p* the vector of allele frequencies computed from all genotyped individuals, and *Z* = *X* − 2*p*. The genomic relationship matrix (GRM) is *G* = *ZZ*ᵀ / (2 Σₖ *p*ₖ(1 − *p*ₖ)) (VanRaden 2008). Allele frequencies and *G* use genotypes only. Selection candidates are genotyped before selection, so computing *G* over all individuals involves no phenotype information and is legitimate in deployment.

Principal components were taken from the standardised-genotype relationship matrix. *k*-means clustering (*k* = 5, 10 restarts, fixed seed) of the first ten components defined genomic clusters.

### Base predictors

Phenotypes were standardised in every outer fold using the training mean and standard deviation only.

**GBLUP.** The model is *y* = 1μ + *g* + *e*, with *g* ~ N(0, σ²_g *G*) and *e* ~ N(0, σ²_e *I*). Variance components were estimated by restricted maximum likelihood (REML) on the training individuals, using the spectral decomposition of Kang *et al.* (2008): a grid over log δ (δ = σ²_e/σ²_g) followed by bounded Brent refinement.

**RKHS regression.** This is the same mixed-model machinery with a Gaussian kernel *K*ᵢⱼ = exp(−*D*²ᵢⱼ / median *D*²), where *D*²ᵢⱼ = *G*ᵢᵢ + *G*ⱼⱼ − 2*G*ᵢⱼ (Gianola and van Kaam 2008; de los Campos *et al.* 2010).

**LightGBM.** Gradient-boosted trees (Ke *et al.* 2017) were fitted with hyper-parameters fixed in advance: 500 trees, learning rate 0.05, 31 leaves, column subsampling 0.3, row subsampling 0.8 and at least 10 samples per leaf. Inputs were at most 10,000 evenly spaced markers of the dosage matrix. These may include a few monomorphic markers, which trees ignore.

### Relatedness covariate

For a training set *S* and a candidate *j* with relationship vector *k* = *G*_{S,j}, let *V* = *G*_{S,S} + δ*I*. The prediction error variance of the GBLUP phenotype prediction (universal kriging form, including the uncertainty of the estimated mean) is σ²_g *d*ⱼ + σ²_e, with

*d*ⱼ = *G*ⱼⱼ − *k*ᵀ*V*⁻¹*k* + (1 − 1ᵀ*V*⁻¹*k*)² / (1ᵀ*V*⁻¹1).     (1)

*d*ⱼ is the PEV of the genetic value in units of σ²_g. It is small for candidates with many close relatives in *S* and approaches *G*ⱼⱼ for unrelated candidates; 1 − *d*ⱼ/*G*ⱼⱼ is the classical reliability. *d*ⱼ depends only on genotypes, on the training set and on δ. It can therefore be computed for any candidate and used with any base predictor. All variance components came from the outer training set.

### Prediction-interval methods

Let *ŷ*ⱼ be the base prediction for candidate *j* from the model fitted on the training set *T*, and let σ(*d*) = (σ̂²_g *d* + σ̂²_e)^{1/2}. The nominal coverage was 1 − α = 0.90; α = 0.05 and 0.20 were used for sensitivity analyses. Eight methods were compared: KinCP and seven alternatives. CalPred-style calibration was fitted in two variants, which are counted as one alternative.

1. **Gauss-PEV** (GBLUP only): *ŷ*ⱼ ± *z*_{1−α/2} σ(*d*ⱼ). This is the classical model-based interval.
2. **Gauss-homosc**: *ŷ*ⱼ ± *z*_{1−α/2} times the standard deviation of random five-fold out-of-fold residuals in *T*.
3. **SCP** (split conformal): the model is refitted on a random 80% of *T* (at least 10 individuals are kept for calibration). With absolute residuals *R*ᵢ on the remaining 20% (*n*_c individuals), the interval is *ŷ*ⱼ ± the ⌈(1 − α)(*n*_c + 1)⌉-th smallest *R*ᵢ (Lei *et al.* 2018).
4. **NormCP**: as SCP, with scores *R*ᵢ/σ(*d*ᵢ) and half-width scaled by σ(*d*ⱼ). This is component B alone, with *d* measured relative to the 80% fitting subset.
5. **CV+** (Barber *et al.* 2021): random five-fold cross-fitting in *T*. The bounds are the ⌊α(*n* + 1)⌋-th smallest of {*ŷ*ⱼ^{(−k(i))} − *R*ᵢ} and the ⌈(1 − α)(*n* + 1)⌉-th smallest of {*ŷ*ⱼ^{(−k(i))} + *R*ᵢ}.
6. **CalPred-style** calibration, inspired by Hou *et al.* (2024): a heteroscedastic Gaussian model for residuals, *r* ~ N(*m*₀ + *m*₁*c*, exp{2(*a* + *bc*)}), with context *c* the standardised log *d*. It was fitted by maximum likelihood either to the random-fold pool ("random pool") or to the same pool A used by KinCP ("pool A").
7. **OOF-quantile**: the conformal quantile of absolute random-fold out-of-fold residuals, placed around *ŷ*ⱼ. This mirrors the cross-validated residual quantiles of PredInterval (Xu *et al.* 2025) and is also the ablation of KinCP with none of its components.
8. **KinCP** (proposed), described next.

**KinCP.** KinCP has three components.

(A) *Calibration pool.* Two cross-fitting schemes are run inside *T*: random five-fold, and genomic-cluster folds. For the latter, *k*-means (10 restarts) with *k* = min{5, max(2, ⌊|*T*|/20⌋)} is applied to the training individuals' scores on the global genotype principal components, which are computed once from all genotyped individuals. Each scheme yields an out-of-fold residual *r*ᵢ for every training individual. For each residual, *d*ᵢ is computed with Eq. (1) relative to the inner training subset that produced it. The pool {(*r*ᵢ, *d*ᵢ)} has 2|*T*| members and spans both close relatives (random folds) and distant relatives (cluster folds).

(B) *Normalised scores.* *s*ᵢ = |*r*ᵢ| / σ(*d*ᵢ).

(C) *Localisation.* For candidate *j*, each pool member receives weight *w*ᵢ(*j*) = exp{−(log *d*ᵢ − log *d*ⱼ)² / (2*h*ⱼ²)}. The candidate's own weight is 1, placed at +∞ (Tibshirani *et al.* 2019; Guan 2023). The quantile is

*q̂*ⱼ = inf{*s* : Σᵢ *w*ᵢ(*j*) 1[*s*ᵢ ≤ *s*] / (Σᵢ *w*ᵢ(*j*) + 1) ≥ 1 − α},     (2)

and the interval is *ŷ*ⱼ ± *q̂*ⱼ σ(*d*ⱼ). The default bandwidth is *h* = 0.5 × SD(log *d*ᵢ). It is widened multiplicatively (×1.25, at most 60 times) for each candidate until Σᵢ *w*ᵢ(*j*) ≥ 50. This floor prevents uninformative infinite intervals for candidates outside the pool's range of *d* (File S1, deviation D1). The floor depends only on genotype-derived covariates, never on outcomes.

Ablations removed every non-empty subset of A, B and C:
* without A, the random-fold pool only;
* without B, raw |*r*| with unit scale;
* without C, the unweighted conformal quantile of the pool.

**Rationale and guarantees.** Suppose that the conditional distribution of the score given *d* is the same for pool members and candidates (relatedness-conditional invariance), and that only the distribution of *d* differs between them. Weighting pool members by the density ratio of *d* then gives a finite-sample marginal coverage guarantee (Tibshirani *et al.* 2019). Kernel localisation in *d* approximates conditional coverage given *d* (Guan 2023).

KinCP departs from these conditions in four ways:
* it uses a deterministic kernel;
* the pool residuals come from models trained on subsets of *T* (as in CV+; Barber *et al.* 2021), while the interval is centred on the full-training-set prediction (the cross-validated residual-quantile construction of PredInterval, which has no CV+-type guarantee);
* each training individual contributes two dependent residuals, one per cross-fitting scheme;
* the invariance assumption is only approximately met.

KinCP therefore inherits no exact finite-sample guarantee. Its two design choices make the invariance assumption more plausible:
* cross-fitting with genomic clusters places calibration residuals at the levels of *d* that candidates actually reach;
* normalisation by σ(*d*) removes the first-order dependence of the residual scale on relatedness.

We therefore evaluate calibration empirically, with endpoints that are conditional on *d*.

### Deployment regimes and leakage control

Three regimes were used:
* **R1, random:** the five 5-fold EasyGeSe cross-validation assignments, i.e. 25 outer folds.
* **R2, cluster-out:** each of the five genomic clusters was held out in turn, and the analysis was repeated with five seeds for all stochastic components.
* **R3, reduced training:** the R1 folds with the training set randomly subsampled to 50%.

RKHS was run on R1 (first repeat) and R2 (two seeds). LightGBM was run on R1 (first repeat) and R2 (one seed), and not on maize (compute; deviation D5).

Phenotype scaling, REML, hyper-parameters, cross-fitting, calibration scores and the variance components in σ(*d*) used outer-training individuals only. Inner cross-fitting reused the outer-fold δ (deviation D3). Seeds {11, 22, 33, 44, 55} were fixed in advance and tied to repeats. No seed was selected after viewing results. The R1 repeats re-use the same individuals, and the R2 seeds share identical outer folds and differ only in inner randomness, so neither is an independent replicate. Test folds with fewer than five individuals were skipped. This affected only one loblolly-pine cluster of three trees, leaving 20 of 25 R2 folds per pine trait.

Split conformal fits its model on 80% of the training set by construction. LightGBM hyper-parameters were not tuned, which may limit its point accuracy but affects all interval methods equally, because they share the same base predictor.

### Simulation with known genetic values

Additive traits were simulated on the real genotypes of loblolly pine, pig and maize. The design used:
* heritability *h*² ∈ {0.2, 0.5, 0.8};
* 10 or 1,000 quantitative trait loci, drawn among markers with minor-allele frequency above 0.01, with standard-normal effects;
* five replicates per setting.

Genetic values were scaled to variance *h*², and environmental noise had variance 1 − *h*². Each replicate was analysed with GBLUP under R1 (seeded random five-fold) and R2.

### Endpoints

For each unit, regime and base predictor, test records were pooled over folds and repeats. The endpoints were:
* marginal coverage, and its absolute deviation from 0.90;
* **relatedness-conditional coverage error**, the primary endpoint: test records were grouped into quintiles of *d* and we took the mean over quintiles of |coverage − 0.90|;
* worst-quintile coverage;
* mean width, in phenotypic SD units;
* the interval score (Gneiting and Raftery 2007), (*u* − *l*) + (2/α)(*l* − *y*)₊ + (2/α)(*y* − *u*)₊.

A perfectly calibrated method still shows a conditional error from binomial sampling within quintiles. As a reference, we report the expected value of this noise floor for one pass over the data, with quintiles of *n*/5 individuals. Under R1 each individual is tested in five repeats with different training sets. Pooled R1 errors can therefore fall below this single-pass floor, so the floor is only an approximate yardstick.

### Statistical analysis

The unit of analysis was the dataset × trait combination. KinCP was compared with each alternative using two-sided Wilcoxon signed-rank tests (Wilcoxon 1945), paired by unit. *P*-values were Holm-adjusted (Holm 1979) within each family, defined by base predictor × endpoint × comparison set (baselines or ablations). Each baseline family spans three regimes and seven competitors (21 tests), which is conservative. Effect sizes were the median paired difference (competitor minus KinCP; positive values favour KinCP), with 95% percentile-bootstrap confidence intervals (10,000 resamples; Efron 1979), and the matched-pairs rank-biserial correlation (Kerby 2014). With 24 heterogeneous units these intervals can be asymmetric and mainly reflect heterogeneity between units.

As a robustness check on the primary endpoint, conditional coverage error was also computed on quintiles of the maximum standardised genomic relationship to the training set, a relatedness measure that KinCP does not use.

Traits from the same dataset share genotypes, so units are not fully independent. The tests are interpreted together with the per-species results (Figure 4).

### Selection analysis

Within each outer fold, the top 10% of candidates were selected by *ŷ*. We recorded:
* coverage among the selected candidates (selection-conditional coverage; cf. Jin and Candès 2023);
* the share of selected candidates whose phenotype fell below the interval's lower bound (target ≤ 0.05 for a two-sided 90% interval);
* the mean standardised phenotype of the selected candidates when ranking by *ŷ* versus by the lower bound.

### Exploratory analyses (not pre-specified)

Two variants were added after the main results had been seen, and are reported separately as exploratory (File S1, deviation D6). Both were run with GBLUP for R1 (first repeat) and R2 (first seed) on all units.

1. **KinCP-G.** The cluster folds of pool A are the *global* genomic clusters present in the training set rather than a re-clustering of it. This matches the granularity of the calibration shifts to cluster-out deployment.
2. **Mondrian-d.** This is a group-conditional alternative to localisation C (Vovk 2013). It uses pool A and normalised scores, with separate conformal quantiles within quintile bins of log *d*.

### Software, reproducibility and pre-specification

The analysis uses Python 3.11, NumPy, SciPy, scikit-learn and LightGBM. All computations ran on a 4-core CPU without a GPU. A single command (`python run_all.py --mode full`) regenerates every result, table and figure from the public data, and every number in this article is inserted automatically from the generated result files. The study design was committed to version control before any model was fitted. Five deviations, all made for compute reasons or found in a pipeline smoke test, are listed in File S1.


## Results

### Datasets, relatedness and predictive ability

The 24 traits came from datasets of 324 to 4,421 genotyped individuals and 4,782 to 201,896 polymorphic markers (Table 1). GBLUP predictive ability under random cross-validation ranged from 0.29 to 0.90 (median 0.62). It fell to a median of 0.38 under cluster-out validation. This is the familiar loss of accuracy for weakly related candidates (Habier *et al.* 2007; Clark *et al.* 2012; Werner *et al.* 2020).

Cluster-out candidates had systematically larger values of the relatedness covariate *d* than random-CV candidates (Figure 2b). Random cross-validation therefore under-represents the weakly related candidates for which uncertainty matters most.

Several panels contain many near-identical genotypes: 2,600 pairs above a standardised relationship of 0.95 in barley, 192 in soybean and 37 in lentil (Table 1).

### RQ1: standard intervals are miscalibrated along the relatedness axis

**Random cross-validation (R1).** Every method reached close to nominal *marginal* coverage. Mean coverage was 0.906 for KinCP, 0.903 for split conformal (SCP), 0.910 for CV+ and 0.905 for Gauss-PEV (Table 2). Marginal coverage hid a systematic pattern, however. Relatedness-blind intervals over-covered the candidates most closely related to the training set and under-covered the least related ones (Figure 3, left):
* SCP: 0.921 in the closest quintile against 0.880 in the most distant;
* CV+: 0.931 against 0.881.

**Cluster-out validation (R2).** Here the problem became a failure of marginal coverage. Mean coverage was:
* 0.828 for SCP;
* 0.838 for CV+;
* 0.830 for homoscedastic Gaussian intervals;
* 0.829 for the out-of-fold residual quantile (the PredInterval-like construction).

Coverage fell below 0.85 for 11 of 24 units with SCP and for 11 with CV+ (Figure 4). The worst unit reached only 0.703 with CV+. Because these methods calibrate on residuals of relatives that are closer than the candidates, their intervals were too narrow for new clusters. The shortfall was largest in the least-related quintile (Figure 3, middle).

**Gauss-PEV.** The model-based interval, which uses the same relatedness information through Eq. (1), adapted its width to relatedness and was well calibrated under R1 (conditional coverage error 0.020). Under R2 it under-covered on average (0.881; conditional error 0.052). It was poorly calibrated for some units, with a minimum of 0.778 for pine c5c6.

### RQ2: KinCP restores coverage, and the calibration pool is the decisive component

**Calibration of KinCP.** With GBLUP as the base predictor, KinCP had the lowest mean relatedness-conditional coverage error of the eight compared methods in every regime (Table 2): 0.017 under R1, 0.036 under R2 and 0.014 under R3. Under R2 its marginal coverage was 0.894 (SD over units 0.024; minimum 0.845). Its intervals were wider than those of the relatedness-blind conformal methods (2.83 *vs.* 2.46 phenotypic SD for CV+), as required to reach coverage. **Interval score.** On the interval score, which trades width against misses (a proper scoring rule; Gneiting and Raftery 2007), KinCP was *not* better than the main alternatives. The mean scores were 3.91 for KinCP and 4.06 for CV+ under R2. The Holm-adjusted *P*-values were = 0.983 against CV+, = 1.000 against Gauss-PEV and = 1.000 against CalPred-style on pool A. KinCP was significantly better only than SCP (*P* < 0.001) and NormCP (*P* = 0.034). Under R3, Gauss-PEV had a slightly lower interval score than KinCP (Holm *P* = 0.032). The intervals of relatedness-blind methods were narrower and missed more often, and the interval score weighs these two effects against each other. The benefit of KinCP is therefore *validity*: coverage close to the nominal level, including for weakly related candidates. It is not a better sharpness–coverage trade-off.

**Paired tests on the primary endpoint under R2** (Table 3; Figure 12). KinCP's conditional coverage error was lower than that of:
* CV+: median paired difference 0.012 (95% CI 0.007 to 0.064), Holm-adjusted *P* = 0.003, KinCP better in 20/24 units;
* SCP: *P* = 0.002;
* Gauss-PEV: difference 0.008, 95% CI 0.003 to 0.021, *P* = 0.004, 19/24 units;
* NormCP: *P* = 0.033;
* CalPred-style calibration fitted to a random pool: *P* = 0.003.

**Species-level analysis.** Treating species rather than traits as the unit (10 units; traits averaged within species) gave the same direction. Under R2, KinCP had a lower conditional error than CV+ in 9/10 species (unadjusted *P* = 0.004, Holm *P* = 0.070) and than Gauss-PEV in 9/10 species (unadjusted *P* = 0.004, Holm *P* = 0.070). With 10 units and Holm adjustment over 21 comparisons, these species-level tests have limited power (Supplementary file statistics_species.csv).

**Pool A versus conformalisation.** KinCP did **not** differ from a CalPred-style heteroscedastic Gaussian calibration fitted to the *same* relatedness-diverse pool (pool A): difference -0.001, 95% CI -0.006 to 0.006, *P* = 0.900. The same parametric calibration fitted to a random pool did significantly worse. The main benefit therefore comes from the calibration pool, not from conformalisation as such. Under R1 the differences between methods were small in absolute terms, although KinCP remained significantly better than CV+ (*P* = 0.003) and SCP (*P* = 0.033).

**Ablation** (Table 4; Figure 5). The ablation supports this interpretation:
* *Without component A* (random-fold pool only, B + C), the R2 conditional error rose from 0.036 to 0.053 and coverage fell to 0.881. Under R1 the same variant was as good as the full method (0.015): when deployment resembles random cross-validation, a random-fold pool already covers the relevant relatedness range.
* *Without localisation C* (A + B), the R2 error was 0.042.
* *Without normalisation B* (A + C), it was 0.035. Normalisation therefore contributed little once A and C were present, but it helped when C was absent: A only gave 0.045 under R2 and 0.035 under R1, where pooling without normalisation over-covered (coverage 0.928).
* *With no component* (the out-of-fold quantile), the R2 error was 0.086.

**Robustness of the endpoint to the relatedness measure.** The primary endpoint bins candidates by *d*, which is also KinCP's localisation variable. We therefore repeated the analysis on quintiles of an independent measure: the maximum standardised genomic relationship of each candidate to the training set.
* *Under R2,* KinCP again had the smallest conditional error (0.032, against 0.076 for CV+ and 0.050 for Gauss-PEV). It was better than Gauss-PEV in 23/24 units (Holm *P* < 0.001) and than CV+ in 21/24 (Holm *P* < 0.001). It did not differ significantly from CalPred-style calibration on pool A (Holm *P* = 0.094).
* *Under R1,* all methods were similar on this measure (KinCP 0.022, CV+ 0.026, Gauss-PEV 0.023; all Holm *P* ≥ 0.15). Relatedness-blind intervals still over-covered the candidates with the closest relatives in the training set (CV+ 0.928).

KinCP's advantage under random cross-validation is therefore specific to calibration along *d* and is small. Its advantage under cluster-out deployment does not depend on how relatedness is measured.

**Remaining gap.** Even KinCP remained below nominal in the least-related quintile under R2 (worst-quintile coverage 0.839). Its conditional error under R2 exceeded the error expected from binomial sampling alone (0.022; see Methods).

### RQ3: robustness and generalisation

**Reduced training set (R3).** Halving the training set (R3) left the picture of R1 unchanged (Table 2). KinCP had a conditional error of 0.014, against 0.024 for CV+ (*P* = 0.002) and 0.017 for Gauss-PEV (*P* = 0.212).

**Other base predictors** (Table 5; Figure 6). The pattern was the same for nonlinear predictors that have no prediction error variance of their own. KinCP used the GBLUP-derived *d* as the relatedness covariate:
* *RKHS regression, R2:* coverage 0.891 for KinCP against 0.828 for CV+ and 0.826 for SCP. Conditional errors were 0.038 *vs.* 0.090 (*P* = 0.004).
* *LightGBM, R2:* coverage 0.895 against 0.845 and 0.826. Conditional errors were 0.037 *vs.* 0.082 (*P* = 0.007).
* As with GBLUP, KinCP and CalPred-style calibration on pool A did not differ for either predictor (RKHS *P* = 0.927; LightGBM *P* = 1.000).

**Simulation with known genetic values** (Table 6; Figure 7). In simulations with known additive genetic values on real loblolly pine, pig and maize genotypes (128 analyses), KinCP covered 0.899 under R1 and 0.901 under R2. CV+ covered 0.906 and 0.881, SCP 0.878 under R2, and Gauss-PEV 0.899 under R2. Mean worst-quintile coverage under R2 was 0.874 for KinCP and 0.872 for Gauss-PEV. Because the simulated traits satisfy the Gaussian additive model exactly, Gauss-PEV is the correctly specified reference here. KinCP approached it without using the model's distributional assumptions, whereas relatedness-blind conformal intervals under-covered under R2. The relatedness covariate itself was calibrated for the genetic values. By quintile of *d*, the realised mean squared error of the genetic-value prediction divided by σ̂²_g·*d* ranged from 1.00 to 1.07 under R1 and from 0.98 to 1.06 under R2 (median over analyses; 1 = perfect calibration).

**Near-duplicate genotypes.** Removing near-duplicates did not change the conclusions (File S2, Table S_dedup). Under R2 KinCP covered 0.892 and CV+ 0.845; under R1 the figures were 0.902 and 0.904.

### RQ4: computational cost and sensitivity

**Cost** (Table 7; Figure 8). Building KinCP's two calibration pools requires ten additional model fits per training set. For the kernel models these inner fits reuse the outer-fold variance ratio and need only a Cholesky factorisation, whereas the single outer fit includes REML with an eigendecomposition. The median cost of both pools relative to one outer fit was 1.9× for GBLUP, 1.3× for RKHS and 8.3× for LightGBM. For maize (about 3,500 training individuals), one GBLUP fit took 10.6 s on one CPU thread and both pools 7.7 s. Computing all interval methods from the pools took at most 6.27 s per fold. The overhead is therefore that of a standard five-fold cross-validation run twice, and is negligible relative to phenotyping or genotyping.

**Sensitivity** (Table 8; Figure 9). KinCP was insensitive to its tuning choices:
* *Bandwidth multiplier* from 0.25 to 2: R2 conditional error 0.037 to 0.040, against 0.036 at the default.
* *Mass floor:* without the floor, 0.002 of R2 intervals were infinite. With n_min = 25 or 100 the conditional error was 0.036 and 0.036.
* *Nominal level:* at 1 − α = 0.95 and 0.80, KinCP's R2 coverage was 0.945 and 0.789, against 0.909 and 0.710 for CV+.

[PENDING]

### RQ5: failure modes and selection decisions

**Error analysis** (Figure 10). Neither the excess kurtosis of the phenotype (Spearman ρ between kurtosis and KinCP R2 coverage = -0.14, *P* = 0.504) nor predictive ability (ρ with conditional error = 0.13, *P* = 0.560) explained KinCP's remaining errors. Its worst unit under R2 was pine c5c6 (coverage 0.870).

Gauss-PEV's conditional error under R2 increased with the REML heritability of the trait (ρ = 0.56, *P* = 0.005; unadjusted, exploratory). Its worst unit was pine c5c6 (coverage 0.778).

One explanation consistent with this pattern, which we did not test directly, is that variance components estimated within the training clusters overstate how much genetic signal transfers to a new cluster. Under that misspecification a model-based interval is too narrow, whereas an empirically calibrated interval adjusts. In the simulation, where the additive Gaussian model is correct by construction, Gauss-PEV was calibrated (see above).

**Selection** (Table 9; Figure 11). Among the top 10% of candidates by predicted value, KinCP's coverage under R2 was 0.891. The corresponding values were 0.857 for CV+, 0.834 for SCP, 0.889 for Gauss-PEV and 0.899 for CalPred-style. The share of selected candidates falling below KinCP's lower bound was 0.043, against a target of 0.05.

Ranking candidates by their lower bound instead of their predicted value did not increase the mean phenotype of the selected set, and under R1 it slightly reduced it. Under R1 the median difference was -0.011 phenotypic SD (*P* = 0.005); under R2 it was -0.007 (*P* = 0.422). The two rankings overlapped by a median of 0.87 under R2. Calibrated intervals therefore improve the validity of risk statements about selected candidates, but they do not by themselves change expected genetic gain.


## Discussion

Uncertainty statements for genomic predictions are only useful if they are calibrated for the candidates being selected. Across ten species, three predictors and three deployment regimes, relatedness to the training population was the axis along which standard intervals failed:
* conformal intervals calibrated on random hold-outs were too narrow for weakly related candidates and too wide for close relatives;
* when the candidates formed a new genomic cluster, their marginal coverage collapsed;
* the classical Gaussian interval based on prediction error variance adapted to relatedness but inherited the misspecification of the mixed model under cluster-out deployment.

Kinship-aware calibration largely corrected these failures at the cost of a few additional cross-validation fits.

### Relatedness as the exchangeability-breaking variable

A conformal guarantee is only as good as the exchangeability between calibration residuals and the residual of a new individual. In breeding data the main source of non-exchangeability is not an unknown covariate shift but a known and computable quantity. Quantitative-genetic theory has long shown that the reliability of a genomic prediction is governed by the relationship of the candidate to the reference population (Habier *et al.* 2007; Clark *et al.* 2012; Pszczola *et al.* 2012; Wientjes *et al.* 2013).

The GBLUP prediction error variance summarises this relationship as a single number per candidate, available before phenotyping (Eq. 1). It plays here the role that genetic distance or "context" plays for human polygenic scores (Ding *et al.* 2023; Hou *et al.* 2024). In breeding populations, however, the dominant structure is family relatedness rather than continental ancestry. The training set typically contains full- and half-sibs of some candidates and no relatives of others, so relatedness to the training set varies far more within a single deployment than in largely unrelated human cohorts.

The point here goes beyond the known optimism of random cross-validation for *accuracy* (Werner *et al.* 2020). Uncertainty statements calibrated on random hold-outs are miscalibrated in a relatedness-dependent way even when their marginal coverage is nominal. This can be corrected using genotypes alone. Our results show that adopting this covariate is not enough. Normalising scores by it (NormCP) or fitting a heteroscedastic model to random-fold residuals (CalPred-style with a random pool) still left large errors under cluster-out deployment. Calibration residuals must also *cover* the relatedness range of the candidates. Genomic-cluster cross-fitting inside the training set achieves this cheaply and without any phenotypes of the candidates.

### Conformal or parametric calibration?

Given the relatedness-diverse pool, KinCP and a parametric heteroscedastic Gaussian calibration in the spirit of CalPred performed indistinguishably. This is a useful negative result. It shows that, in these data, the benefit comes from the calibration *design* rather than from conformalisation as such. KinCP retains two practical advantages:
* its quantiles are distribution-free, so they need no Gaussian or log-linear variance model;
* under the relatedness-conditional invariance assumption it inherits the weighted-conformal coverage argument (Tibshirani *et al.* 2019).

Practitioners who prefer a parametric calibration can obtain most of the gain by fitting it to the same pool. Neither approach improved the interval score relative to relatedness-blind conformal intervals or the Gaussian PEV interval. Narrower, under-covering intervals can score similarly, because the interval score trades width against misses. When the purpose of an interval is a statement of risk that holds for the candidates at hand, coverage validity is the relevant criterion, and that is what calibration along relatedness delivers. We therefore regard pool A as the main methodological recommendation and KinCP as a convenient, assumption-light way to use it.

### Relation to classical reliability and accuracy validation

The classical PEV interval was competitive under random cross-validation, which is the regime in which it is usually checked. It lost calibration under cluster-out deployment, mostly for traits with high within-cluster heritability. This complements the LR method of Legarra and Reverter (2018), which validates *population-level* accuracy and dispersion of predictions. Our endpoints assess *individual-level* interval calibration conditional on relatedness. Both kinds of validation are needed. Neither replaces a deployment-matched validation design (Werner *et al.* 2020).

### Practical recommendations

1. **Report calibration conditional on relatedness**, not only marginal coverage. Random cross-validation can show nominal marginal coverage while systematically misstating uncertainty for distant candidates.
2. **Build the calibration pool by cross-fitting with both random and genomic-cluster folds** whenever candidates may come from new families or sub-populations.
3. **Use the GBLUP PEV as the relatedness covariate**, even when the point predictor is a kernel or tree model.
4. **Use intervals to qualify, not replace, rankings.** Ranking by lower bounds did not increase mean selected phenotypes. Its value lies in identifying candidates whose predictions are unreliable, consistent with the uncertainty-aware selection framework of Ahlinder and Waldmann (2026).

### Limitations

* **Coverage target.** Coverage is assessed for observed phenotypes (the quantity breeders observe). It is not assessed for true breeding values, which are unknown in real data. The simulation reports calibration with known genetic values only as a diagnostic.
* **Guarantee.** KinCP's guarantee is approximate. The pool residuals come from models fitted to subsets of the training set, and the invariance of scores given relatedness is an assumption that we tested empirically rather than proved. A residual under-coverage remained for the least-related candidates under cluster-out deployment.
* **Deployment regimes are proxies.**
  * *Clusters.* Genomic clusters stand in for new families or populations. Five clusters per dataset give few independent deployment groups, so coverage under R2 is itself estimated with sizeable error.
  * *No temporal data.* Temporal deployment across breeding cycles, which also involves genotype-by-environment and selection effects, could not be studied because the public datasets lack cycle information.
* **Phenotype preprocessing.** Some EasyGeSe phenotypes are BLUEs adjusted across all lines and environments (e.g. maize, barley). Test and training phenotypes may therefore share adjusted environmental effects. This mild preprocessing leakage applies equally to all methods.
* **R1 advantage.** Under random cross-validation, KinCP's advantage was small and specific to calibration along *d*. It was not significant when relatedness was measured by maximum genomic relationship.
* **Statistical units.** Traits from the same species share genotypes, so the 24 units are not fully independent. The pattern was, however, consistent across species (Figure 4).
* **Trait choice.** Traits were chosen by a rule fixed in advance. In loblolly pine this selected two closely related root traits.
* **Compute.** LightGBM was not run on maize, and the RKHS and LightGBM analyses used fewer repeats than GBLUP, both for compute reasons.
* **Scope of the evaluation.** Only one-step prediction intervals for single traits in a single environment were evaluated. Multi-trait, multi-environment and selection-conditional (Jin and Candès 2023) guarantees are natural extensions.

### Conclusions

Relatedness to the training population is the variable along which genomic-prediction intervals lose calibration. Kinship-aware conformal prediction uses the GBLUP prediction error variance as a relatedness covariate and calibrates on residuals from random and genomic-cluster cross-fitting. Across ten species and three predictors it restored near-nominal coverage that holds across relatedness levels, at modest computational cost. The calibration design, rather than the choice between conformal and parametric calibration, is what matters most.

## Data availability

All genotype and phenotype data are publicly available from EasyGeSe (Quesada-Traver *et al.* 2025; Zenodo record 15348871, https://zenodo.org/records/15348871, CC-BY 4.0). The complete code, configuration, per-job results and the scripts that regenerate every table, figure and number in this article are provided as File S3. They will be deposited on Zenodo with a DOI upon acceptance [DOI to be inserted]. File S1 contains the pre-specified study design and the log of deviations. File S2 contains supplementary tables, including the per-unit results for every method, base predictor and regime.

## Acknowledgments

We thank the data generators and the EasyGeSe curators for making the benchmark data openly available. In accordance with GENETICS policy, we disclose that a generative AI assistant was used to help write analysis code and draft text. All analyses, results and text were checked by the authors, who take full responsibility for the content. [Further acknowledgments to be added by the authors.]

## Funding

[To be completed by the authors. If none: This research received no specific grant from any funding agency.]

## Conflicts of interest

The authors declare no conflicts of interest.


## Literature cited

Ahlinder J, Waldmann P. 2026. Uncertainty-aware breeding decisions: MCMC-based optimum contribution selection increases breeding decision robustness. GENETICS. iyag205. doi:10.1093/genetics/iyag205

Angelopoulos AN, Bates S. 2023. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 16(4):494–591. doi:10.1561/2200000101

Barber RF, Candès EJ, Ramdas A, Tibshirani RJ. 2021. Predictive inference with the jackknife+. The Annals of Statistics. 49(1). doi:10.1214/20-aos1965

Barber RF, Candès EJ, Ramdas A, Tibshirani RJ. 2023. Conformal prediction beyond exchangeability. The Annals of Statistics. 51(2). doi:10.1214/23-aos2276

Bhattacharyya A, Barber RF. 2026. Group-weighted conformal prediction. Electronic Journal of Statistics. 20(1). doi:10.1214/26-ejs2506

Clark SA, Hickey JM, Daetwyler HD, van der Werf JH. 2012. The importance of information on relatives for the prediction of genomic breeding values and the implications for the makeup of reference data sets in livestock breeding schemes. Genetics Selection Evolution. 44(1):4. doi:10.1186/1297-9686-44-4

Crossa J, Pérez-Rodríguez P, Cuevas J, Montesinos-López O, Jarquín D, de los Campos G, Burgueño J, González-Camacho JM, Pérez-Elizalde S, Beyene Y, et al. 2017. Genomic Selection in Plant Breeding: Methods, Models, and Perspectives. Trends in Plant Science. 22(11):961–975. doi:10.1016/j.tplants.2017.08.011

de los Campos G, Gianola D, Rosa GJM, Weigel KA, Crossa J. 2010. Semi-parametric genomic-enabled prediction of genetic values using reproducing kernel Hilbert spaces methods. Genetics Research. 92(4):295–308. doi:10.1017/s0016672310000285

Ding Y, Hou K, Xu Z, Pimplaskar A, Petter E, Boulier K, Privé F, Vilhjálmsson BJ, Olde Loohuis LM, Pasaniuc B. 2023. Polygenic scoring accuracy varies across the genetic ancestry continuum. Nature. 618(7966):774–781. doi:10.1038/s41586-023-06079-4

Dunn R, Wasserman L, Ramdas A. 2023. Distribution-Free Prediction Sets for Two-Layer Hierarchical Models. Journal of the American Statistical Association. 118(544):2491–2502. doi:10.1080/01621459.2022.2060112

Efron B. 1979. Bootstrap Methods: Another Look at the Jackknife. The Annals of Statistics. 7(1). doi:10.1214/aos/1176344552

Gianola D, van Kaam JBCHM. 2008. Reproducing Kernel Hilbert Spaces Regression Methods for Genomic Assisted Prediction of Quantitative Traits. Genetics. 178(4):2289–2303. doi:10.1534/genetics.107.084285

Gibbs I, Cherian JJ, Candès EJ. 2025. Conformal prediction with conditional guarantees. Journal of the Royal Statistical Society Series B: Statistical Methodology. 87(4):1100–1126. doi:10.1093/jrsssb/qkaf008

Gneiting T, Raftery AE. 2007. Strictly Proper Scoring Rules, Prediction, and Estimation. Journal of the American Statistical Association. 102(477):359–378. doi:10.1198/016214506000001437

Gogna A, Schulthess AW, Röder MS, Ganal MW, Reif JC. 2022. Gabi wheat a panel of European elite lines as central stock for wheat genetic research. Scientific Data. 9(1):538. doi:10.1038/s41597-022-01651-5

Guan L. 2023. Localized conformal prediction: a generalized inference framework for conformal prediction. Biometrika. 110(1):33–50. doi:10.1093/biomet/asac040

Habier D, Fernando RL, Dekkers JCM. 2007. The Impact of Genetic Relationship Information on Genome-Assisted Breeding Values. Genetics. 177(4):2389–2397. doi:10.1534/genetics.107.081190

Haile TA, Heidecker T, Wright D, Neupane S, Ramsay L, Vandenberg A, Bett KE. 2020. Genomic selection for lentil breeding: Empirical evidence. The Plant Genome. 13(1):e20002. doi:10.1002/tpg2.20002

Henderson CR. 1975. Best Linear Unbiased Estimation and Prediction under a Selection Model. Biometrics. 31(2):423. doi:10.2307/2529430

Holm S. 1979. A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics. 6(2):65–70. https://www.jstor.org/stable/4615733

Hou K, Xu Z, Ding Y, Mandla R, Shi Z, Boulier K, Harpak A, Pasaniuc B. 2024. Calibrated prediction intervals for polygenic scores across diverse contexts. Nature Genetics. 56(7):1386–1396. doi:10.1038/s41588-024-01792-w

Jin Y, Candès EJ. 2023. Selection by prediction with conformal p-values. Journal of Machine Learning Research. 24. https://arxiv.org/abs/2210.01408

Kaler AS, Dhanapal AP, Ray JD, King CA, Fritschi FB, Purcell LC. 2017. Genome‐Wide Association Mapping of Carbon Isotope and Oxygen Isotope Ratios in Diverse Soybean Genotypes. Crop Science. 57(6):3085–3100. doi:10.2135/cropsci2017.03.0160

Kang HM, Zaitlen NA, Wade CM, Kirby A, Heckerman D, Daly MJ, Eskin E. 2008. Efficient Control of Population Structure in Model Organism Association Mapping. Genetics. 178(3):1709–1723. doi:10.1534/genetics.107.080101

Ke G, Meng Q, Finley T, Wang T, Chen W, Ma W, Ye Q, Liu TY. 2017. LightGBM: a highly efficient gradient boosting decision tree. Advances in Neural Information Processing Systems. 30. https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html

Kerby DS. 2014. The Simple Difference Formula: An Approach to Teaching Nonparametric Correlation. Comprehensive Psychology. 3:11.IT.3.1. doi:10.2466/11.it.3.1

Kodji E, Attaoua R, Haloui M, Hishmih C, Seitz M, Woodward M, Hussin JG, Hamet P, Tremblay J. 2026. Improving the reliability of polygenic risk score-based prediction for cardiovascular and renal complications across ancestries in type 2 diabetes using Mondrian Cross-Conformal Prediction. PLOS Computational Biology. 22(8):e1014670. doi:10.1371/journal.pcbi.1014670

Kumar P. 2026. Calibrated genomic selection [data paper and code]. Zenodo. doi:10.5281/zenodo.22962591

Legarra A, Reverter A. 2018. Semi-parametric estimates of population accuracy and bias of predictions of breeding values and future phenotypes using the LR method. Genetics Selection Evolution. 50(1):53. doi:10.1186/s12711-018-0426-6

Lei J, G’Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. 2018. Distribution-Free Predictive Inference for Regression. Journal of the American Statistical Association. 113(523):1094–1111. doi:10.1080/01621459.2017.1307116

Meuwissen THE, Hayes BJ, Goddard ME. 2001. Prediction of Total Genetic Value Using Genome-Wide Dense Marker Maps. Genetics. 157(4):1819–1829. doi:10.1093/genetics/157.4.1819

Papadopoulos H, Proedrou K, Vovk V, Gammerman A. 2002. Inductive Confidence Machines for Regression. Lecture Notes in Computer Science. 345-356. doi:10.1007/3-540-36755-1_29

Pszczola M, Strabel T, Mulder H, Calus M. 2012. Reliability of direct genomic values for animals with different relationships within and to the reference population. Journal of Dairy Science. 95(1):389–400. doi:10.3168/jds.2011-4338

Quesada-Traver C, Ariza-Suarez D, Studer B, Yates S. 2025. EasyGeSe – a resource for benchmarking genomic prediction methods. BMC Genomics. 26(1):953. doi:10.1186/s12864-025-12129-0

Resende MFR, Muñoz P, Resende MDV, Garrick DJ, Fernando RL, Davis JM, Jokela EJ, Martin TA, Peter GF, Kirst M. 2012. Accuracy of Genomic Selection Methods in a Standard Data Set of Loblolly Pine (Pinus taedaL.). Genetics. 190(4):1503–1510. doi:10.1534/genetics.111.137026

Sun J, Wang Y, Folkersen L, Borné Y, Amlien I, Buil A, Orho-Melander M, Børglum AD, Hougaard DM, , et al. 2021. Translating polygenic risk scores for clinical use by estimating the confidence bounds of risk prediction. Nature Communications. 12(1):5276. doi:10.1038/s41467-021-25014-7

Tibshirani RJ, Barber RF, Candès EJ, Ramdas A. 2019. Conformal prediction under covariate shift. Advances in Neural Information Processing Systems. 32. https://papers.nips.cc/paper_files/paper/2019/hash/8fb21ee7a2207526da55a679f0332de2-Abstract.html

VanRaden P. 2008. Efficient Methods to Compute Genomic Predictions. Journal of Dairy Science. 91(11):4414–4423. doi:10.3168/jds.2007-0980

Vovk V. 2013. Conditional validity of inductive conformal predictors. Machine Learning. 92(2-3):349–376. doi:10.1007/s10994-013-5355-6

Vovk V, Gammerman A, Shafer G. 2022. Algorithmic Learning in a Random World. Springer, Cham (2nd edition). doi:10.1007/978-3-031-06649-8

Washburn JD, Varela JI, Xavier A, Chen Q, Ertl D, Gage JL, Holland JB, Lima DC, Romay MC, Lopez-Cruz M, et al. 2025. Global genotype by environment prediction competition reveals that diverse modeling strategies can deliver satisfactory maize yield estimates. GENETICS. 229(2):iyae195. doi:10.1093/genetics/iyae195

Werner CR, Gaynor RC, Gorjanc G, Hickey JM, Kox T, Abbadi A, Leckband G, Snowdon RJ, Stahl A. 2020. How Population Structure Impacts Genomic Selection Accuracy in Cross-Validation: Implications for Practical Breeding. Frontiers in Plant Science. 11:592977. doi:10.3389/fpls.2020.592977

Wientjes YCJ, Veerkamp RF, Calus MPL. 2013. The Effect of Linkage Disequilibrium and Family Relationships on the Reliability of Genomic Prediction. Genetics. 193(2):621–631. doi:10.1534/genetics.112.146290

Wilcoxon F. 1945. Individual Comparisons by Ranking Methods. Biometrics Bulletin. 1(6):80. doi:10.2307/3001968

Xu C, Ganesh SK, Zhou X. 2025. Statistical construction of calibrated prediction intervals for polygenic score-based phenotype prediction. Nature Genetics. 57(11):2891–2900. doi:10.1038/s41588-025-02360-6

Zhao K, Tung CW, Eizenga GC, Wright MH, Ali ML, Price AH, Norton GJ, Islam MR, Reynolds A, Mezey J, et al. 2011. Genome-wide association mapping reveals a rich genetic architecture of complex traits in Oryza sativa. Nature Communications. 2(1):467. doi:10.1038/ncomms1467


[Date]

The Editor-in-Chief
GENETICS
Genetics Society of America

Dear Editor,

We submit our manuscript **"Kinship-aware conformal prediction intervals for genomic prediction across ten plant and animal species"** for consideration as an Investigation in GENETICS, in the area of Systems & Computational Genetics (statistical methods / genomic prediction).

**What the manuscript does.** Breeders act on individual genomic predictions, so they need uncertainty statements that are valid for the candidates actually being selected. Distribution-free conformal intervals are increasingly proposed for this purpose. We show that their guarantee is undermined in breeding data along a known quantitative-genetic axis: the relatedness of each candidate to the training population. We measure this relatedness with the GBLUP prediction error variance and propose kinship-aware conformal prediction (KinCP), which has three components: a calibration pool spanning close and distant relatives, PEV-normalised scores, and localisation in the relatedness metric.

The study covers 24 traits from ten species in the EasyGeSe resource, three prediction models, three deployment regimes, and simulations on real genotypes with known genetic values:
* Relatedness-blind conformal intervals (split conformal, CV+) over-cover close relatives and under-cover distant candidates. For candidates from held-out genomic clusters their mean coverage of nominal 90% intervals fell to 0.828–0.838.
* KinCP achieved the lowest, or joint-lowest, relatedness-conditional coverage error in all deployment regimes and for all three predictors (GBLUP, RKHS, LightGBM). The classical PEV-based Gaussian interval lost calibration under cluster-out deployment (mean coverage 0.881; KinCP 0.894).
* Ablations show that the relatedness-diverse calibration pool, rather than conformalisation itself, is the decisive ingredient. We report this openly and give practical recommendations.

**Why GENETICS.** The work joins classical quantitative-genetic theory (prediction error variance, reliability and the effect of relatedness, a tradition with deep roots in GENETICS, e.g. Habier *et al.* 2007; Wientjes *et al.* 2013) with modern distribution-free inference. It continues the journal's recent genomic-prediction methods literature, for example Gibbs *et al.* 2025 and Ahlinder and Waldmann 2026.

**Reproducibility and data policy.** All data are public (EasyGeSe, CC-BY 4.0). The complete code reproduces every number, table and figure with one command, and will be deposited with a DOI (Zenodo) on acceptance, in line with the GSA data policy. The study design and endpoints were version-controlled before any model was fitted, and all deviations are reported.

**Declarations.**
* This manuscript is original, has not been published, and is not under consideration elsewhere.
* [No preprint has been posted / A preprint is available at …].
* All authors approved the submission.
* The work uses only public, de-identified plant and animal genotype and phenotype data, so no ethics approval was required.
* The authors declare no competing interests.
* Generative-AI assistance used in preparing the analysis code and text is disclosed in the Acknowledgments, as GENETICS policy requires. The authors take full responsibility for the content.

**Suggested reviewers.** [Optional: names and e-mail addresses to be added by the authors]

Thank you for considering our submission.

Sincerely,

[Corresponding author name]
[Affiliation, address]
[E-mail, ORCID]
on behalf of all authors


## Tables

**Table 1** Datasets and traits. The traits were chosen by a rule fixed in advance (at least 200 records and 30 distinct values; up to three per dataset). Near-duplicate pairs are distinct individuals whose standardised genomic relationship exceeds 0.95. REML h² and GBLUP predictive ability r are means over the random cross-validation folds.

| Species                                | Trait            |   n phenotyped |   Markers |   Near-duplicate pairs (>0.95) | Cluster sizes (k-means, k=5)   |   REML h² (R1) |   GBLUP r (R1) |
|:---------------------------------------|:-----------------|---------------:|----------:|-------------------------------:|:-------------------------------|---------------:|---------------:|
| Barley (Hordeum vulgare)               | BaMMV            |           1438 |    176064 |                           2600 | 355/780/103/75/125             |          0.718 |          0.685 |
| Barley (Hordeum vulgare)               | BaYMV            |           1438 |    176064 |                           2600 | 355/780/103/75/125             |          0.430 |          0.529 |
| Common bean (Phaseolus vulgaris)       | DF               |            444 |     16707 |                              0 | 244/24/50/40/86                |          0.569 |          0.769 |
| Common bean (Phaseolus vulgaris)       | DPM              |            444 |     16707 |                              0 | 244/24/50/40/86                |          0.530 |          0.675 |
| Common bean (Phaseolus vulgaris)       | PHI              |            444 |     16707 |                              0 | 244/24/50/40/86                |          0.290 |          0.436 |
| Eastern oyster (Crassostrea virginica) | mm               |            372 |     20745 |                              2 | 91/45/95/76/65                 |          0.463 |          0.460 |
| Lentil (Lens culinaris)                | DTF              |            324 |     23590 |                             37 | 44/96/52/100/32                |          0.818 |          0.813 |
| Lentil (Lens culinaris)                | VEG              |            324 |     23590 |                             37 | 44/96/52/100/32                |          0.798 |          0.835 |
| Lentil (Lens culinaris)                | DTM              |            324 |     23590 |                             37 | 44/96/52/100/32                |          0.654 |          0.841 |
| Loblolly pine (Pinus taeda)            | rootnum          |            925 |      4782 |                              0 | 175/510/222/3/15               |          0.824 |          0.864 |
| Loblolly pine (Pinus taeda)            | rootnumbin       |            925 |      4782 |                              0 | 175/510/222/3/15               |          0.793 |          0.844 |
| Loblolly pine (Pinus taeda)            | c5c6             |            910 |      4782 |                              0 | 172/500/220/3/15               |          0.847 |          0.896 |
| Maize (Zea mays)                       | Yield_Mg_ha      |           4421 |    201896 |                            116 | 1547/689/577/384/1224          |          0.680 |          0.609 |
| Maize (Zea mays)                       | Grain_Moisture   |           4421 |    201896 |                            116 | 1547/689/577/384/1224          |          0.771 |          0.883 |
| Maize (Zea mays)                       | Plant_Height_cm  |           4420 |    201896 |                            116 | 1547/688/577/384/1224          |          0.848 |          0.857 |
| Pig (Sus scrofa)                       | PFAI             |           1709 |     39308 |                              4 | 712/239/134/494/130            |          0.235 |          0.294 |
| Rice (Oryza sativa)                    | Plant_height     |            352 |     27232 |                              2 | 52/55/81/86/78                 |          0.639 |          0.626 |
| Rice (Oryza sativa)                    | Culm_habit       |            351 |     27232 |                              2 | 52/55/80/86/78                 |          0.402 |          0.614 |
| Rice (Oryza sativa)                    | Flag_leaf_length |            346 |     27232 |                              2 | 50/54/80/84/78                 |          0.323 |          0.345 |
| Soybean (Glycine max)                  | C13              |            346 |     20526 |                            192 | 155/10/58/59/64                |          0.308 |          0.414 |
| Soybean (Glycine max)                  | Wilt             |            346 |     20526 |                            192 | 155/10/58/59/64                |          0.765 |          0.457 |
| Wheat (Triticum aestivum)              | EW               |            371 |     12546 |                              6 | 123/30/98/29/91                |          0.557 |          0.386 |
| Wheat (Triticum aestivum)              | GH               |            371 |     12546 |                              6 | 123/30/98/29/91                |          0.848 |          0.595 |
| Wheat (Triticum aestivum)              | GPE              |            371 |     12546 |                              6 | 123/30/98/29/91                |          0.549 |          0.384 |

**Table 2** Calibration of 90% prediction intervals with the GBLUP base predictor. Values are mean ± SD over dataset × trait units. Cond. error is the mean over quintiles of relatedness of |coverage − 0.90| (primary endpoint). Width is in phenotypic SD units. Lower interval scores are better.

| Regime   | Method              |   Units | Coverage      | Abs. cov. deviation   | Cond. error   | Worst-quintile cov.   | Width (SD units)   | Interval score   |
|:---------|:--------------------|--------:|:--------------|:----------------------|:--------------|:----------------------|:-------------------|:-----------------|
| R1       | Gauss-PEV           |      24 | 0.905 ± 0.010 | 0.009 ± 0.007         | 0.020 ± 0.008 | 0.876 ± 0.016         | 2.397 ± 0.565      | 3.183 ± 0.746    |
| R1       | Gauss-homosc        |      24 | 0.907 ± 0.011 | 0.010 ± 0.008         | 0.027 ± 0.012 | 0.867 ± 0.024         | 2.449 ± 0.576      | 3.210 ± 0.751    |
| R1       | SCP                 |      24 | 0.903 ± 0.009 | 0.006 ± 0.007         | 0.025 ± 0.011 | 0.863 ± 0.025         | 2.481 ± 0.593      | 3.278 ± 0.774    |
| R1       | NormCP              |      24 | 0.903 ± 0.009 | 0.007 ± 0.006         | 0.019 ± 0.007 | 0.873 ± 0.016         | 2.455 ± 0.587      | 3.253 ± 0.771    |
| R1       | CV+                 |      24 | 0.910 ± 0.006 | 0.010 ± 0.006         | 0.025 ± 0.011 | 0.870 ± 0.018         | 2.446 ± 0.553      | 3.197 ± 0.764    |
| R1       | CalPred-style(rand) |      24 | 0.902 ± 0.012 | 0.009 ± 0.007         | 0.020 ± 0.008 | 0.874 ± 0.015         | 2.376 ± 0.557      | 3.190 ± 0.743    |
| R1       | CalPred-style       |      24 | 0.904 ± 0.017 | 0.014 ± 0.010         | 0.022 ± 0.009 | 0.873 ± 0.019         | 2.418 ± 0.546      | 3.205 ± 0.733    |
| R1       | KinCP               |      24 | 0.906 ± 0.009 | 0.009 ± 0.006         | 0.017 ± 0.007 | 0.880 ± 0.016         | 2.410 ± 0.539      | 3.197 ± 0.739    |
| R2       | Gauss-PEV           |      24 | 0.881 ± 0.048 | 0.038 ± 0.035         | 0.052 ± 0.029 | 0.819 ± 0.076         | 2.776 ± 0.581      | 3.953 ± 0.676    |
| R2       | Gauss-homosc        |      24 | 0.830 ± 0.081 | 0.076 ± 0.075         | 0.088 ± 0.065 | 0.751 ± 0.113         | 2.454 ± 0.572      | 4.110 ± 0.739    |
| R2       | SCP                 |      24 | 0.828 ± 0.073 | 0.074 ± 0.072         | 0.086 ± 0.062 | 0.742 ± 0.112         | 2.498 ± 0.566      | 4.167 ± 0.665    |
| R2       | NormCP              |      24 | 0.883 ± 0.045 | 0.036 ± 0.031         | 0.049 ± 0.027 | 0.818 ± 0.077         | 2.867 ± 0.601      | 4.003 ± 0.620    |
| R2       | CV+                 |      24 | 0.838 ± 0.071 | 0.066 ± 0.068         | 0.079 ± 0.058 | 0.756 ± 0.109         | 2.464 ± 0.538      | 4.062 ± 0.720    |
| R2       | CalPred-style(rand) |      24 | 0.867 ± 0.058 | 0.049 ± 0.044         | 0.060 ± 0.038 | 0.799 ± 0.087         | 2.715 ± 0.620      | 4.072 ± 0.877    |
| R2       | CalPred-style       |      24 | 0.891 ± 0.027 | 0.022 ± 0.018         | 0.037 ± 0.014 | 0.838 ± 0.042         | 2.825 ± 0.449      | 3.886 ± 0.659    |
| R2       | KinCP               |      24 | 0.894 ± 0.024 | 0.018 ± 0.017         | 0.036 ± 0.015 | 0.839 ± 0.044         | 2.830 ± 0.453      | 3.907 ± 0.688    |
| R3       | Gauss-PEV           |      24 | 0.901 ± 0.012 | 0.009 ± 0.008         | 0.017 ± 0.007 | 0.876 ± 0.020         | 2.504 ± 0.555      | 3.345 ± 0.754    |
| R3       | Gauss-homosc        |      24 | 0.905 ± 0.012 | 0.010 ± 0.008         | 0.024 ± 0.009 | 0.870 ± 0.025         | 2.558 ± 0.570      | 3.377 ± 0.756    |
| R3       | SCP                 |      24 | 0.912 ± 0.014 | 0.013 ± 0.013         | 0.023 ± 0.009 | 0.881 ± 0.023         | 2.762 ± 0.631      | 3.525 ± 0.797    |
| R3       | NormCP              |      24 | 0.913 ± 0.013 | 0.014 ± 0.011         | 0.020 ± 0.008 | 0.890 ± 0.022         | 2.747 ± 0.628      | 3.499 ± 0.801    |
| R3       | CV+                 |      24 | 0.910 ± 0.009 | 0.011 ± 0.007         | 0.024 ± 0.009 | 0.873 ± 0.024         | 2.588 ± 0.577      | 3.371 ± 0.772    |
| R3       | CalPred-style(rand) |      24 | 0.897 ± 0.013 | 0.011 ± 0.008         | 0.018 ± 0.007 | 0.872 ± 0.018         | 2.515 ± 0.618      | 3.395 ± 0.805    |
| R3       | CalPred-style       |      24 | 0.897 ± 0.016 | 0.013 ± 0.009         | 0.021 ± 0.011 | 0.866 ± 0.032         | 2.510 ± 0.538      | 3.394 ± 0.777    |
| R3       | KinCP               |      24 | 0.902 ± 0.009 | 0.007 ± 0.005         | 0.014 ± 0.005 | 0.883 ± 0.013         | 2.530 ± 0.565      | 3.364 ± 0.753    |

**Table 3** Paired comparisons of KinCP with each alternative (GBLUP) on the relatedness-conditional coverage error (Cond. error) and the marginal coverage deviation (Abs. cov. deviation). Median diff. is the median paired difference (competitor − KinCP; positive favours KinCP), with its 95% bootstrap confidence interval (CI low, CI high). P is from a two-sided Wilcoxon signed-rank test; P (Holm) is adjusted within each endpoint family (all regimes × baseline competitors). Interval-score comparisons and all ablation comparisons are in File S2.

| Regime   | Endpoint            | Competitor          |   Units |   KinCP median |   Competitor median |   Median diff. |   CI low |   CI high |   Rank-biserial r |     P |   P (Holm) |
|:---------|:--------------------|:--------------------|--------:|---------------:|--------------------:|---------------:|---------:|----------:|------------------:|------:|-----------:|
| R1       | Cond. error         | Gauss-PEV           |      24 |          0.016 |               0.019 |          0.001 |   -0.001 |     0.005 |             0.453 | 0.053 |      0.212 |
| R1       | Cond. error         | Gauss-homosc        |      24 |          0.016 |               0.026 |          0.006 |    0.003 |     0.013 |             0.787 | 0.000 |      0.004 |
| R1       | Cond. error         | SCP                 |      24 |          0.016 |               0.022 |          0.004 |    0.000 |     0.009 |             0.667 | 0.003 |      0.033 |
| R1       | Cond. error         | NormCP              |      24 |          0.016 |               0.018 |          0.000 |   -0.000 |     0.004 |             0.260 | 0.277 |      0.554 |
| R1       | Cond. error         | CV+                 |      24 |          0.016 |               0.026 |          0.005 |    0.003 |     0.010 |             0.813 | 0.000 |      0.003 |
| R1       | Cond. error         | CalPred-style       |      24 |          0.016 |               0.021 |          0.004 |    0.001 |     0.010 |             0.627 | 0.006 |      0.047 |
| R1       | Cond. error         | CalPred-style(rand) |      24 |          0.016 |               0.017 |          0.003 |   -0.000 |     0.006 |             0.500 | 0.031 |      0.189 |
| R1       | Abs. cov. deviation | Gauss-PEV           |      24 |          0.008 |               0.007 |         -0.001 |   -0.005 |     0.003 |            -0.181 | 0.447 |      1.000 |
| R1       | Abs. cov. deviation | Gauss-homosc        |      24 |          0.008 |               0.008 |          0.000 |   -0.002 |     0.002 |             0.060 | 0.812 |      1.000 |
| R1       | Abs. cov. deviation | SCP                 |      24 |          0.008 |               0.005 |         -0.001 |   -0.007 |     0.002 |            -0.293 | 0.218 |      1.000 |
| R1       | Abs. cov. deviation | NormCP              |      24 |          0.008 |               0.005 |         -0.001 |   -0.003 |     0.002 |            -0.207 | 0.390 |      1.000 |
| R1       | Abs. cov. deviation | CV+                 |      24 |          0.008 |               0.009 |          0.001 |   -0.003 |     0.004 |             0.153 | 0.527 |      1.000 |
| R1       | Abs. cov. deviation | CalPred-style       |      24 |          0.008 |               0.011 |          0.004 |   -0.001 |     0.010 |             0.464 | 0.052 |      0.619 |
| R1       | Abs. cov. deviation | CalPred-style(rand) |      24 |          0.008 |               0.008 |         -0.001 |   -0.004 |     0.004 |            -0.060 | 0.812 |      1.000 |
| R2       | Cond. error         | Gauss-PEV           |      24 |          0.034 |               0.040 |          0.008 |    0.003 |     0.021 |             0.793 | 0.000 |      0.004 |
| R2       | Cond. error         | Gauss-homosc        |      24 |          0.034 |               0.058 |          0.023 |    0.008 |     0.069 |             0.887 | 0.000 |      0.001 |
| R2       | Cond. error         | SCP                 |      24 |          0.034 |               0.048 |          0.028 |    0.005 |     0.080 |             0.840 | 0.000 |      0.002 |
| R2       | Cond. error         | NormCP              |      24 |          0.034 |               0.044 |          0.007 |    0.001 |     0.012 |             0.667 | 0.003 |      0.033 |
| R2       | Cond. error         | CV+                 |      24 |          0.034 |               0.049 |          0.012 |    0.007 |     0.064 |             0.807 | 0.000 |      0.003 |
| R2       | Cond. error         | CalPred-style       |      24 |          0.034 |               0.032 |         -0.001 |   -0.006 |     0.006 |            -0.033 | 0.900 |      0.900 |
| R2       | Cond. error         | CalPred-style(rand) |      24 |          0.034 |               0.052 |          0.014 |    0.006 |     0.026 |             0.820 | 0.000 |      0.003 |
| R2       | Abs. cov. deviation | Gauss-PEV           |      24 |          0.015 |               0.032 |          0.010 |    0.005 |     0.021 |             0.727 | 0.001 |      0.020 |
| R2       | Abs. cov. deviation | Gauss-homosc        |      24 |          0.015 |               0.043 |          0.029 |    0.010 |     0.079 |             0.813 | 0.000 |      0.004 |
| R2       | Abs. cov. deviation | SCP                 |      24 |          0.015 |               0.044 |          0.032 |    0.002 |     0.083 |             0.740 | 0.001 |      0.016 |
| R2       | Abs. cov. deviation | NormCP              |      24 |          0.015 |               0.026 |          0.008 |    0.002 |     0.022 |             0.696 | 0.004 |      0.056 |
| R2       | Abs. cov. deviation | CV+                 |      24 |          0.015 |               0.040 |          0.012 |    0.001 |     0.073 |             0.680 | 0.003 |      0.043 |
| R2       | Abs. cov. deviation | CalPred-style       |      24 |          0.015 |               0.018 |          0.003 |   -0.002 |     0.009 |             0.320 | 0.178 |      1.000 |
| R2       | Abs. cov. deviation | CalPred-style(rand) |      24 |          0.015 |               0.033 |          0.021 |    0.004 |     0.045 |             0.820 | 0.000 |      0.003 |
| R3       | Cond. error         | Gauss-PEV           |      24 |          0.013 |               0.015 |          0.002 |   -0.001 |     0.005 |             0.460 | 0.049 |      0.212 |
| R3       | Cond. error         | Gauss-homosc        |      24 |          0.013 |               0.023 |          0.007 |    0.004 |     0.013 |             0.827 | 0.000 |      0.002 |
| R3       | Cond. error         | SCP                 |      24 |          0.013 |               0.023 |          0.007 |    0.001 |     0.013 |             0.780 | 0.000 |      0.004 |
| R3       | Cond. error         | NormCP              |      24 |          0.013 |               0.019 |          0.003 |    0.000 |     0.008 |             0.600 | 0.009 |      0.061 |
| R3       | Cond. error         | CV+                 |      24 |          0.013 |               0.023 |          0.008 |    0.003 |     0.014 |             0.935 | 0.000 |      0.002 |
| R3       | Cond. error         | CalPred-style       |      24 |          0.013 |               0.020 |          0.007 |    0.002 |     0.010 |             0.693 | 0.003 |      0.033 |
| R3       | Cond. error         | CalPred-style(rand) |      24 |          0.013 |               0.017 |          0.002 |    0.001 |     0.007 |             0.473 | 0.042 |      0.212 |
| R3       | Abs. cov. deviation | Gauss-PEV           |      24 |          0.007 |               0.007 |          0.002 |   -0.002 |     0.004 |             0.200 | 0.406 |      1.000 |
| R3       | Abs. cov. deviation | Gauss-homosc        |      24 |          0.007 |               0.009 |          0.001 |   -0.002 |     0.005 |             0.254 | 0.287 |      1.000 |
| R3       | Abs. cov. deviation | SCP                 |      24 |          0.007 |               0.007 |          0.004 |   -0.003 |     0.015 |             0.393 | 0.095 |      1.000 |
| R3       | Abs. cov. deviation | NormCP              |      24 |          0.007 |               0.010 |          0.007 |   -0.001 |     0.011 |             0.478 | 0.045 |      0.581 |
| R3       | Abs. cov. deviation | CV+                 |      24 |          0.007 |               0.009 |          0.002 |    0.001 |     0.006 |             0.480 | 0.040 |      0.555 |
| R3       | Abs. cov. deviation | CalPred-style       |      24 |          0.007 |               0.013 |          0.006 |    0.000 |     0.010 |             0.652 | 0.006 |      0.093 |
| R3       | Abs. cov. deviation | CalPred-style(rand) |      24 |          0.007 |               0.008 |          0.003 |   -0.003 |     0.005 |             0.287 | 0.229 |      1.000 |

**Table 4** Ablation of KinCP (GBLUP). A: relatedness-diverse calibration pool. B: PEV-normalised scores. C: localisation in log d. The row label lists the components that are kept. Mean ± SD over units.

| Regime   | Method        |   Units | Coverage      | Abs. cov. deviation   | Cond. error   | Worst-quintile cov.   | Width (SD units)   | Interval score   |
|:---------|:--------------|--------:|:--------------|:----------------------|:--------------|:----------------------|:-------------------|:-----------------|
| R1       | A+B+C (KinCP) |      24 | 0.906 ± 0.009 | 0.009 ± 0.006         | 0.017 ± 0.007 | 0.880 ± 0.016         | 2.410 ± 0.539      | 3.197 ± 0.739    |
| R1       | B+C           |      24 | 0.903 ± 0.005 | 0.005 ± 0.004         | 0.015 ± 0.007 | 0.880 ± 0.013         | 2.392 ± 0.566      | 3.195 ± 0.746    |
| R1       | A+C           |      24 | 0.912 ± 0.010 | 0.013 ± 0.009         | 0.020 ± 0.007 | 0.887 ± 0.018         | 2.475 ± 0.542      | 3.206 ± 0.743    |
| R1       | A+B           |      24 | 0.907 ± 0.018 | 0.014 ± 0.013         | 0.023 ± 0.009 | 0.879 ± 0.024         | 2.400 ± 0.486      | 3.194 ± 0.733    |
| R1       | C             |      24 | 0.906 ± 0.006 | 0.007 ± 0.005         | 0.017 ± 0.007 | 0.881 ± 0.013         | 2.422 ± 0.573      | 3.201 ± 0.749    |
| R1       | B             |      24 | 0.899 ± 0.005 | 0.004 ± 0.003         | 0.019 ± 0.006 | 0.869 ± 0.013         | 2.349 ± 0.562      | 3.181 ± 0.743    |
| R1       | A             |      24 | 0.928 ± 0.023 | 0.028 ± 0.023         | 0.035 ± 0.019 | 0.897 ± 0.032         | 2.646 ± 0.443      | 3.275 ± 0.685    |
| R1       | none          |      24 | 0.904 ± 0.004 | 0.005 ± 0.003         | 0.025 ± 0.011 | 0.864 ± 0.018         | 2.409 ± 0.555      | 3.207 ± 0.747    |
| R2       | A+B+C (KinCP) |      24 | 0.894 ± 0.024 | 0.018 ± 0.017         | 0.036 ± 0.015 | 0.839 ± 0.044         | 2.830 ± 0.453      | 3.907 ± 0.688    |
| R2       | B+C           |      24 | 0.881 ± 0.049 | 0.039 ± 0.035         | 0.053 ± 0.030 | 0.814 ± 0.080         | 2.779 ± 0.609      | 3.962 ± 0.682    |
| R2       | A+C           |      24 | 0.893 ± 0.023 | 0.017 ± 0.017         | 0.035 ± 0.013 | 0.843 ± 0.039         | 2.802 ± 0.419      | 3.884 ± 0.671    |
| R2       | A+B           |      24 | 0.891 ± 0.028 | 0.021 ± 0.020         | 0.042 ± 0.021 | 0.829 ± 0.052         | 2.822 ± 0.463      | 3.917 ± 0.679    |
| R2       | C             |      24 | 0.861 ± 0.061 | 0.048 ± 0.053         | 0.060 ± 0.047 | 0.794 ± 0.101         | 2.606 ± 0.569      | 3.992 ± 0.687    |
| R2       | B             |      24 | 0.875 ± 0.050 | 0.042 ± 0.036         | 0.056 ± 0.030 | 0.811 ± 0.077         | 2.723 ± 0.596      | 3.966 ± 0.675    |
| R2       | A             |      24 | 0.883 ± 0.028 | 0.025 ± 0.022         | 0.045 ± 0.017 | 0.813 ± 0.053         | 2.723 ± 0.372      | 3.916 ± 0.651    |
| R2       | none          |      24 | 0.829 ± 0.073 | 0.073 ± 0.071         | 0.086 ± 0.060 | 0.750 ± 0.109         | 2.422 ± 0.540      | 4.104 ± 0.730    |
| R3       | A+B+C (KinCP) |      24 | 0.902 ± 0.009 | 0.007 ± 0.005         | 0.014 ± 0.005 | 0.883 ± 0.013         | 2.530 ± 0.565      | 3.364 ± 0.753    |
| R3       | B+C           |      24 | 0.904 ± 0.007 | 0.006 ± 0.006         | 0.013 ± 0.007 | 0.886 ± 0.010         | 2.545 ± 0.600      | 3.364 ± 0.760    |
| R3       | A+C           |      24 | 0.911 ± 0.011 | 0.014 ± 0.008         | 0.018 ± 0.008 | 0.892 ± 0.015         | 2.624 ± 0.558      | 3.383 ± 0.757    |
| R3       | A+B           |      24 | 0.902 ± 0.017 | 0.012 ± 0.012         | 0.020 ± 0.008 | 0.879 ± 0.022         | 2.506 ± 0.505      | 3.360 ± 0.744    |
| R3       | C             |      24 | 0.908 ± 0.009 | 0.009 ± 0.007         | 0.015 ± 0.008 | 0.888 ± 0.011         | 2.595 ± 0.605      | 3.378 ± 0.764    |
| R3       | B             |      24 | 0.898 ± 0.008 | 0.006 ± 0.006         | 0.016 ± 0.006 | 0.873 ± 0.014         | 2.493 ± 0.588      | 3.350 ± 0.753    |
| R3       | A             |      24 | 0.927 ± 0.024 | 0.027 ± 0.024         | 0.032 ± 0.020 | 0.899 ± 0.028         | 2.769 ± 0.435      | 3.445 ± 0.683    |
| R3       | none          |      24 | 0.905 ± 0.008 | 0.007 ± 0.005         | 0.021 ± 0.009 | 0.869 ± 0.021         | 2.555 ± 0.587      | 3.381 ± 0.757    |

**Table 5** Calibration with three base predictors under random (R1) and cluster-out (R2) validation. Mean ± SD over units. LightGBM was not run on maize (deviation D5).

| Base     | Regime   | Method        |   Units | Coverage      | Cond. error   | Worst-quintile cov.   | Width         |
|:---------|:---------|:--------------|--------:|:--------------|:--------------|:----------------------|:--------------|
| GBLUP    | R1       | SCP           |      24 | 0.903 ± 0.009 | 0.025 ± 0.011 | 0.863 ± 0.025         | 2.481 ± 0.593 |
| GBLUP    | R1       | CV+           |      24 | 0.910 ± 0.006 | 0.025 ± 0.011 | 0.870 ± 0.018         | 2.446 ± 0.553 |
| GBLUP    | R1       | CalPred-style |      24 | 0.904 ± 0.017 | 0.022 ± 0.009 | 0.873 ± 0.019         | 2.418 ± 0.546 |
| GBLUP    | R1       | KinCP         |      24 | 0.906 ± 0.009 | 0.017 ± 0.007 | 0.880 ± 0.016         | 2.410 ± 0.539 |
| GBLUP    | R1       | Gauss-PEV     |      24 | 0.905 ± 0.010 | 0.020 ± 0.008 | 0.876 ± 0.016         | 2.397 ± 0.565 |
| GBLUP    | R2       | SCP           |      24 | 0.828 ± 0.073 | 0.086 ± 0.062 | 0.742 ± 0.112         | 2.498 ± 0.566 |
| GBLUP    | R2       | CV+           |      24 | 0.838 ± 0.071 | 0.079 ± 0.058 | 0.756 ± 0.109         | 2.464 ± 0.538 |
| GBLUP    | R2       | CalPred-style |      24 | 0.891 ± 0.027 | 0.037 ± 0.014 | 0.838 ± 0.042         | 2.825 ± 0.449 |
| GBLUP    | R2       | KinCP         |      24 | 0.894 ± 0.024 | 0.036 ± 0.015 | 0.839 ± 0.044         | 2.830 ± 0.453 |
| GBLUP    | R2       | Gauss-PEV     |      24 | 0.881 ± 0.048 | 0.052 ± 0.029 | 0.819 ± 0.076         | 2.776 ± 0.581 |
| RKHS     | R1       | SCP           |      24 | 0.897 ± 0.018 | 0.033 ± 0.016 | 0.847 ± 0.044         | 2.431 ± 0.633 |
| RKHS     | R1       | CV+           |      24 | 0.910 ± 0.005 | 0.028 ± 0.010 | 0.864 ± 0.018         | 2.429 ± 0.561 |
| RKHS     | R1       | CalPred-style |      24 | 0.905 ± 0.015 | 0.027 ± 0.009 | 0.864 ± 0.024         | 2.401 ± 0.546 |
| RKHS     | R1       | KinCP         |      24 | 0.905 ± 0.009 | 0.022 ± 0.009 | 0.873 ± 0.022         | 2.390 ± 0.547 |
| RKHS     | R2       | SCP           |      24 | 0.826 ± 0.083 | 0.091 ± 0.069 | 0.729 ± 0.128         | 2.501 ± 0.601 |
| RKHS     | R2       | CV+           |      24 | 0.828 ± 0.084 | 0.090 ± 0.070 | 0.738 ± 0.120         | 2.434 ± 0.555 |
| RKHS     | R2       | CalPred-style |      24 | 0.893 ± 0.028 | 0.038 ± 0.013 | 0.841 ± 0.036         | 2.828 ± 0.419 |
| RKHS     | R2       | KinCP         |      24 | 0.891 ± 0.025 | 0.038 ± 0.014 | 0.836 ± 0.040         | 2.813 ± 0.424 |
| LightGBM | R1       | SCP           |      21 | 0.899 ± 0.020 | 0.034 ± 0.019 | 0.847 ± 0.044         | 2.573 ± 0.618 |
| LightGBM | R1       | CV+           |      21 | 0.922 ± 0.009 | 0.034 ± 0.011 | 0.880 ± 0.031         | 2.613 ± 0.573 |
| LightGBM | R1       | CalPred-style |      21 | 0.905 ± 0.014 | 0.028 ± 0.010 | 0.858 ± 0.028         | 2.515 ± 0.539 |
| LightGBM | R1       | KinCP         |      21 | 0.905 ± 0.011 | 0.024 ± 0.010 | 0.865 ± 0.027         | 2.501 ± 0.535 |
| LightGBM | R2       | SCP           |      21 | 0.826 ± 0.095 | 0.097 ± 0.077 | 0.726 ± 0.135         | 2.653 ± 0.628 |
| LightGBM | R2       | CV+           |      21 | 0.845 ± 0.089 | 0.082 ± 0.069 | 0.763 ± 0.130         | 2.620 ± 0.588 |
| LightGBM | R2       | CalPred-style |      21 | 0.891 ± 0.029 | 0.038 ± 0.018 | 0.834 ± 0.048         | 2.935 ± 0.388 |
| LightGBM | R2       | KinCP         |      21 | 0.895 ± 0.025 | 0.037 ± 0.015 | 0.844 ± 0.041         | 2.930 ± 0.375 |

**Table 6** Simulation on real genotypes (loblolly pine, pig, maize) with additive genetic values. Mean ± SD over genotype sets × replicates.

| Regime   |    h² |   QTL | Method        |   Replicates×genotype sets | Coverage      | Cond. error   | Worst-quintile cov.   | Width         |
|:---------|------:|------:|:--------------|---------------------------:|:--------------|:--------------|:----------------------|:--------------|
| R1       | 0.200 |    10 | SCP           |                         14 | 0.902 ± 0.007 | 0.016 ± 0.007 | 0.878 ± 0.014         | 3.190 ± 0.114 |
| R1       | 0.200 |    10 | CV+           |                         14 | 0.902 ± 0.003 | 0.014 ± 0.007 | 0.881 ± 0.013         | 3.162 ± 0.079 |
| R1       | 0.200 |    10 | Gauss-PEV     |                         14 | 0.899 ± 0.004 | 0.014 ± 0.007 | 0.877 ± 0.011         | 3.144 ± 0.074 |
| R1       | 0.200 |    10 | CalPred-style |                         14 | 0.897 ± 0.007 | 0.014 ± 0.009 | 0.877 ± 0.015         | 3.125 ± 0.071 |
| R1       | 0.200 |    10 | KinCP         |                         14 | 0.900 ± 0.004 | 0.014 ± 0.008 | 0.879 ± 0.012         | 3.143 ± 0.074 |
| R1       | 0.200 |  1000 | SCP           |                         10 | 0.901 ± 0.007 | 0.016 ± 0.008 | 0.875 ± 0.017         | 3.209 ± 0.116 |
| R1       | 0.200 |  1000 | CV+           |                         10 | 0.902 ± 0.002 | 0.015 ± 0.007 | 0.878 ± 0.009         | 3.196 ± 0.075 |
| R1       | 0.200 |  1000 | Gauss-PEV     |                         10 | 0.900 ± 0.005 | 0.015 ± 0.007 | 0.875 ± 0.015         | 3.178 ± 0.064 |
| R1       | 0.200 |  1000 | CalPred-style |                         10 | 0.898 ± 0.007 | 0.016 ± 0.006 | 0.875 ± 0.014         | 3.161 ± 0.071 |
| R1       | 0.200 |  1000 | KinCP         |                         10 | 0.898 ± 0.003 | 0.016 ± 0.006 | 0.875 ± 0.009         | 3.175 ± 0.080 |
| R1       | 0.500 |    10 | SCP           |                         10 | 0.904 ± 0.011 | 0.015 ± 0.004 | 0.884 ± 0.018         | 2.976 ± 0.117 |
| R1       | 0.500 |    10 | CV+           |                         10 | 0.905 ± 0.007 | 0.014 ± 0.004 | 0.885 ± 0.007         | 2.953 ± 0.093 |
| R1       | 0.500 |    10 | Gauss-PEV     |                         10 | 0.898 ± 0.005 | 0.013 ± 0.004 | 0.878 ± 0.012         | 2.869 ± 0.090 |
| R1       | 0.500 |    10 | CalPred-style |                         10 | 0.896 ± 0.005 | 0.013 ± 0.005 | 0.874 ± 0.011         | 2.857 ± 0.092 |
| R1       | 0.500 |    10 | KinCP         |                         10 | 0.900 ± 0.006 | 0.013 ± 0.003 | 0.880 ± 0.009         | 2.898 ± 0.101 |
| R1       | 0.500 |  1000 | SCP           |                         10 | 0.902 ± 0.011 | 0.018 ± 0.006 | 0.875 ± 0.014         | 2.990 ± 0.133 |
| R1       | 0.500 |  1000 | CV+           |                         10 | 0.904 ± 0.004 | 0.017 ± 0.006 | 0.881 ± 0.009         | 2.961 ± 0.108 |
| R1       | 0.500 |  1000 | Gauss-PEV     |                         10 | 0.898 ± 0.004 | 0.015 ± 0.006 | 0.873 ± 0.008         | 2.896 ± 0.086 |
| R1       | 0.500 |  1000 | CalPred-style |                         10 | 0.896 ± 0.007 | 0.016 ± 0.006 | 0.871 ± 0.011         | 2.875 ± 0.090 |
| R1       | 0.500 |  1000 | KinCP         |                         10 | 0.898 ± 0.005 | 0.014 ± 0.006 | 0.878 ± 0.012         | 2.909 ± 0.107 |
| R1       | 0.800 |    10 | SCP           |                         10 | 0.906 ± 0.011 | 0.023 ± 0.007 | 0.871 ± 0.017         | 2.518 ± 0.191 |
| R1       | 0.800 |    10 | CV+           |                         10 | 0.915 ± 0.008 | 0.023 ± 0.005 | 0.886 ± 0.014         | 2.516 ± 0.155 |
| R1       | 0.800 |    10 | Gauss-PEV     |                         10 | 0.900 ± 0.007 | 0.017 ± 0.005 | 0.873 ± 0.018         | 2.391 ± 0.137 |
| R1       | 0.800 |    10 | CalPred-style |                         10 | 0.901 ± 0.010 | 0.016 ± 0.003 | 0.876 ± 0.017         | 2.399 ± 0.163 |
| R1       | 0.800 |    10 | KinCP         |                         10 | 0.902 ± 0.012 | 0.016 ± 0.005 | 0.878 ± 0.022         | 2.408 ± 0.171 |
| R1       | 0.800 |  1000 | SCP           |                         10 | 0.906 ± 0.009 | 0.019 ± 0.005 | 0.876 ± 0.015         | 2.523 ± 0.201 |
| R1       | 0.800 |  1000 | CV+           |                         10 | 0.910 ± 0.005 | 0.020 ± 0.004 | 0.879 ± 0.014         | 2.506 ± 0.181 |
| R1       | 0.800 |  1000 | Gauss-PEV     |                         10 | 0.899 ± 0.006 | 0.013 ± 0.004 | 0.876 ± 0.015         | 2.402 ± 0.163 |
| R1       | 0.800 |  1000 | CalPred-style |                         10 | 0.897 ± 0.009 | 0.014 ± 0.005 | 0.873 ± 0.021         | 2.392 ± 0.185 |
| R1       | 0.800 |  1000 | KinCP         |                         10 | 0.899 ± 0.006 | 0.014 ± 0.003 | 0.881 ± 0.012         | 2.401 ± 0.175 |
| R2       | 0.200 |    10 | SCP           |                         14 | 0.894 ± 0.014 | 0.019 ± 0.008 | 0.870 ± 0.018         | 3.195 ± 0.128 |
| R2       | 0.200 |    10 | CV+           |                         14 | 0.893 ± 0.009 | 0.017 ± 0.008 | 0.871 ± 0.014         | 3.159 ± 0.086 |
| R2       | 0.200 |    10 | Gauss-PEV     |                         14 | 0.900 ± 0.007 | 0.014 ± 0.006 | 0.878 ± 0.011         | 3.215 ± 0.052 |
| R2       | 0.200 |    10 | CalPred-style |                         14 | 0.900 ± 0.006 | 0.013 ± 0.005 | 0.880 ± 0.009         | 3.226 ± 0.070 |
| R2       | 0.200 |    10 | KinCP         |                         14 | 0.902 ± 0.005 | 0.013 ± 0.006 | 0.879 ± 0.014         | 3.239 ± 0.080 |
| R2       | 0.200 |  1000 | SCP           |                         10 | 0.896 ± 0.014 | 0.020 ± 0.010 | 0.870 ± 0.021         | 3.208 ± 0.128 |
| R2       | 0.200 |  1000 | CV+           |                         10 | 0.897 ± 0.004 | 0.015 ± 0.006 | 0.868 ± 0.013         | 3.196 ± 0.075 |
| R2       | 0.200 |  1000 | Gauss-PEV     |                         10 | 0.902 ± 0.008 | 0.015 ± 0.004 | 0.877 ± 0.014         | 3.243 ± 0.034 |
| R2       | 0.200 |  1000 | CalPred-style |                         10 | 0.899 ± 0.008 | 0.016 ± 0.006 | 0.874 ± 0.015         | 3.235 ± 0.043 |
| R2       | 0.200 |  1000 | KinCP         |                         10 | 0.901 ± 0.004 | 0.015 ± 0.005 | 0.877 ± 0.013         | 3.235 ± 0.084 |
| R2       | 0.500 |    10 | SCP           |                         10 | 0.877 ± 0.016 | 0.027 ± 0.014 | 0.846 ± 0.031         | 2.925 ± 0.096 |
| R2       | 0.500 |    10 | CV+           |                         10 | 0.881 ± 0.012 | 0.023 ± 0.010 | 0.852 ± 0.016         | 2.960 ± 0.098 |
| R2       | 0.500 |    10 | Gauss-PEV     |                         10 | 0.895 ± 0.009 | 0.019 ± 0.007 | 0.865 ± 0.018         | 3.082 ± 0.049 |
| R2       | 0.500 |    10 | CalPred-style |                         10 | 0.897 ± 0.012 | 0.021 ± 0.008 | 0.863 ± 0.019         | 3.106 ± 0.072 |
| R2       | 0.500 |    10 | KinCP         |                         10 | 0.903 ± 0.009 | 0.020 ± 0.009 | 0.870 ± 0.012         | 3.163 ± 0.097 |
| R2       | 0.500 |  1000 | SCP           |                         10 | 0.890 ± 0.018 | 0.023 ± 0.014 | 0.868 ± 0.020         | 3.049 ± 0.110 |
| R2       | 0.500 |  1000 | CV+           |                         10 | 0.884 ± 0.020 | 0.022 ± 0.017 | 0.862 ± 0.025         | 2.977 ± 0.106 |
| R2       | 0.500 |  1000 | Gauss-PEV     |                         10 | 0.902 ± 0.011 | 0.014 ± 0.008 | 0.883 ± 0.017         | 3.118 ± 0.071 |
| R2       | 0.500 |  1000 | CalPred-style |                         10 | 0.898 ± 0.014 | 0.017 ± 0.012 | 0.878 ± 0.023         | 3.110 ± 0.079 |
| R2       | 0.500 |  1000 | KinCP         |                         10 | 0.900 ± 0.011 | 0.015 ± 0.009 | 0.881 ± 0.019         | 3.100 ± 0.070 |
| R2       | 0.800 |    10 | SCP           |                         10 | 0.861 ± 0.021 | 0.045 ± 0.019 | 0.823 ± 0.034         | 2.523 ± 0.153 |
| R2       | 0.800 |    10 | CV+           |                         10 | 0.869 ± 0.019 | 0.038 ± 0.019 | 0.829 ± 0.044         | 2.520 ± 0.142 |
| R2       | 0.800 |    10 | Gauss-PEV     |                         10 | 0.901 ± 0.017 | 0.024 ± 0.014 | 0.867 ± 0.029         | 2.737 ± 0.166 |
| R2       | 0.800 |    10 | CalPred-style |                         10 | 0.899 ± 0.013 | 0.022 ± 0.014 | 0.865 ± 0.030         | 2.737 ± 0.155 |
| R2       | 0.800 |    10 | KinCP         |                         10 | 0.901 ± 0.012 | 0.022 ± 0.010 | 0.867 ± 0.023         | 2.753 ± 0.197 |
| R2       | 0.800 |  1000 | SCP           |                         10 | 0.843 ± 0.026 | 0.057 ± 0.027 | 0.794 ± 0.059         | 2.503 ± 0.208 |
| R2       | 0.800 |  1000 | CV+           |                         10 | 0.857 ± 0.034 | 0.045 ± 0.033 | 0.811 ± 0.055         | 2.522 ± 0.210 |
| R2       | 0.800 |  1000 | Gauss-PEV     |                         10 | 0.891 ± 0.021 | 0.020 ± 0.015 | 0.862 ± 0.035         | 2.771 ± 0.096 |
| R2       | 0.800 |  1000 | CalPred-style |                         10 | 0.894 ± 0.018 | 0.019 ± 0.014 | 0.867 ± 0.026         | 2.780 ± 0.085 |
| R2       | 0.800 |  1000 | KinCP         |                         10 | 0.897 ± 0.013 | 0.017 ± 0.009 | 0.870 ± 0.027         | 2.813 ± 0.101 |

**Table 7** Wall time per outer fold on one CPU thread (random cross-validation). Overhead is the time to build both calibration pools divided by the time of one model fit.

| Base     | Dataset        |   n train |   Single fit (s) |   Random-fold pool (s) |   Cluster-fold pool (s) |   Split-conformal refit (s) |   All interval computations, α=0.10 (s) |   KinCP overhead vs single fit (×) |
|:---------|:---------------|----------:|-----------------:|-----------------------:|------------------------:|----------------------------:|----------------------------------------:|-----------------------------------:|
| GBLUP    | Barley         |      1150 |            0.576 |                  0.288 |                   0.298 |                       0.108 |                                   0.182 |                              1.017 |
| GBLUP    | Common bean    |       355 |            0.026 |                  0.018 |                   0.031 |                       0.007 |                                   0.019 |                              1.934 |
| GBLUP    | Lentil         |       259 |            0.015 |                  0.010 |                   0.021 |                       0.004 |                                   0.016 |                              2.118 |
| GBLUP    | Maize          |      3537 |           10.577 |                  3.737 |                   3.978 |                       1.549 |                                   3.090 |                              0.729 |
| GBLUP    | Eastern oyster |       298 |            0.019 |                  0.014 |                   0.023 |                       0.004 |                                   0.015 |                              1.939 |
| GBLUP    | Pig            |      1367 |            0.711 |                  0.336 |                   0.336 |                       0.137 |                                   0.222 |                              0.945 |
| GBLUP    | Loblolly pine  |       736 |            0.129 |                  0.078 |                   0.085 |                       0.030 |                                   0.054 |                              1.256 |
| GBLUP    | Rice           |       280 |            0.017 |                  0.012 |                   0.022 |                       0.004 |                                   0.014 |                              1.977 |
| GBLUP    | Soybean        |       277 |            0.016 |                  0.011 |                   0.021 |                       0.004 |                                   0.018 |                              1.971 |
| GBLUP    | Wheat          |       297 |            0.019 |                  0.013 |                   0.026 |                       0.005 |                                   0.017 |                              2.093 |
| LightGBM | Barley         |      1150 |           26.704 |                115.238 |                 109.420 |                      21.910 |                                   0.151 |                              8.413 |
| LightGBM | Common bean    |       355 |           12.358 |                 51.405 |                  50.951 |                      10.285 |                                   0.021 |                              8.283 |
| LightGBM | Lentil         |       259 |           10.029 |                 41.534 |                  40.151 |                       8.298 |                                   0.016 |                              8.145 |
| LightGBM | Eastern oyster |       298 |           11.138 |                 45.660 |                  43.201 |                       9.277 |                                   0.016 |                              7.978 |
| LightGBM | Pig            |      1367 |           45.999 |                192.848 |                 191.519 |                      38.430 |                                   0.231 |                              8.356 |
| LightGBM | Loblolly pine  |       736 |            9.698 |                 41.068 |                  40.161 |                       8.277 |                                   0.054 |                              8.376 |
| LightGBM | Rice           |       280 |            9.891 |                 41.353 |                  38.947 |                       8.283 |                                   0.014 |                              8.119 |
| LightGBM | Soybean        |       277 |            9.512 |                 39.658 |                  38.630 |                       7.833 |                                   0.017 |                              8.231 |
| LightGBM | Wheat          |       297 |           10.723 |                 44.626 |                  44.112 |                       8.971 |                                   0.017 |                              8.275 |
| RKHS     | Barley         |      1150 |            1.061 |                  0.448 |                   0.482 |                       0.123 |                                   0.195 |                              0.876 |
| RKHS     | Common bean    |       355 |            0.051 |                  0.028 |                   0.042 |                       0.007 |                                   0.020 |                              1.367 |
| RKHS     | Lentil         |       259 |            0.028 |                  0.015 |                   0.024 |                       0.004 |                                   0.016 |                              1.394 |
| RKHS     | Maize          |      3537 |           20.843 |                  5.390 |                   6.372 |                       1.461 |                                   3.108 |                              0.564 |
| RKHS     | Eastern oyster |       298 |            0.036 |                  0.019 |                   0.031 |                       0.005 |                                   0.015 |                              1.391 |
| RKHS     | Pig            |      1367 |            1.535 |                  0.504 |                   0.527 |                       0.145 |                                   0.227 |                              0.672 |
| RKHS     | Loblolly pine  |       736 |            0.243 |                  0.107 |                   0.124 |                       0.031 |                                   0.053 |                              0.954 |
| RKHS     | Rice           |       280 |            0.032 |                  0.018 |                   0.028 |                       0.004 |                                   0.016 |                              1.464 |
| RKHS     | Soybean        |       277 |            0.033 |                  0.019 |                   0.029 |                       0.004 |                                   0.018 |                              1.454 |
| RKHS     | Wheat          |       297 |            0.038 |                  0.022 |                   0.034 |                       0.005 |                                   0.017 |                              1.474 |

**Table 8** Sensitivity of KinCP to the bandwidth multiplier h, the mass floor n_min and the nominal level, compared with alternatives (GBLUP). Mean ± SD over units.

| Regime   | Variant                  | Coverage      | Cond. error   | Width         |   Share infinite |
|:---------|:-------------------------|:--------------|:--------------|:--------------|-----------------:|
| R1       | KinCP[h=0.25]            | 0.907 ± 0.009 | 0.017 ± 0.007 | 2.431 ± 0.552 |            0.000 |
| R1       | KinCP                    | 0.906 ± 0.009 | 0.017 ± 0.007 | 2.410 ± 0.539 |            0.000 |
| R1       | KinCP[h=1.0]             | 0.906 ± 0.010 | 0.019 ± 0.007 | 2.398 ± 0.524 |            0.000 |
| R1       | KinCP[h=2.0]             | 0.907 ± 0.014 | 0.021 ± 0.007 | 2.400 ± 0.501 |            0.000 |
| R1       | KinCP[fixed-h]           | 0.907 ± 0.009 | 0.018 ± 0.007 | 2.429 ± 0.554 |            0.009 |
| R1       | KinCP[nmin=25]           | 0.906 ± 0.009 | 0.017 ± 0.007 | 2.420 ± 0.544 |            0.000 |
| R1       | KinCP[nmin=100]          | 0.905 ± 0.009 | 0.017 ± 0.006 | 2.401 ± 0.538 |            0.000 |
| R2       | KinCP[h=0.25]            | 0.893 ± 0.023 | 0.037 ± 0.014 | 2.843 ± 0.449 |            0.000 |
| R2       | KinCP                    | 0.894 ± 0.024 | 0.036 ± 0.015 | 2.830 ± 0.453 |            0.000 |
| R2       | KinCP[h=1.0]             | 0.895 ± 0.026 | 0.038 ± 0.017 | 2.843 ± 0.458 |            0.000 |
| R2       | KinCP[h=2.0]             | 0.893 ± 0.027 | 0.040 ± 0.019 | 2.833 ± 0.460 |            0.000 |
| R2       | KinCP[fixed-h]           | 0.894 ± 0.025 | 0.036 ± 0.015 | 2.835 ± 0.457 |            0.002 |
| R2       | KinCP[nmin=25]           | 0.894 ± 0.025 | 0.036 ± 0.015 | 2.835 ± 0.457 |            0.000 |
| R2       | KinCP[nmin=100]          | 0.895 ± 0.024 | 0.036 ± 0.016 | 2.843 ± 0.450 |            0.000 |
| R1       | SCP @ 1−α=0.95           | 0.955 ± 0.006 | 0.016 ± 0.006 | 3.192 ± 0.794 |            0.000 |
| R1       | CV+ @ 1−α=0.95           | 0.956 ± 0.003 | 0.016 ± 0.007 | 3.060 ± 0.718 |            0.000 |
| R1       | Gauss-PEV @ 1−α=0.95     | 0.945 ± 0.008 | 0.015 ± 0.006 | 2.857 ± 0.673 |            0.000 |
| R1       | CalPred-style @ 1−α=0.95 | 0.945 ± 0.011 | 0.017 ± 0.007 | 2.882 ± 0.650 |            0.000 |
| R1       | KinCP @ 1−α=0.95         | 0.953 ± 0.007 | 0.012 ± 0.006 | 3.030 ± 0.686 |            0.000 |
| R1       | SCP @ 1−α=0.90           | 0.903 ± 0.009 | 0.025 ± 0.011 | 2.481 ± 0.593 |            0.000 |
| R1       | CV+ @ 1−α=0.90           | 0.910 ± 0.006 | 0.025 ± 0.011 | 2.446 ± 0.553 |            0.000 |
| R1       | Gauss-PEV @ 1−α=0.90     | 0.905 ± 0.010 | 0.020 ± 0.008 | 2.397 ± 0.565 |            0.000 |
| R1       | CalPred-style @ 1−α=0.90 | 0.904 ± 0.017 | 0.022 ± 0.009 | 2.418 ± 0.546 |            0.000 |
| R1       | KinCP @ 1−α=0.90         | 0.906 ± 0.009 | 0.017 ± 0.007 | 2.410 ± 0.539 |            0.000 |
| R1       | SCP @ 1−α=0.80           | 0.803 ± 0.009 | 0.037 ± 0.021 | 1.842 ± 0.440 |            0.000 |
| R1       | CV+ @ 1−α=0.80           | 0.814 ± 0.007 | 0.041 ± 0.021 | 1.841 ± 0.425 |            0.000 |
| R1       | Gauss-PEV @ 1−α=0.80     | 0.820 ± 0.018 | 0.033 ± 0.015 | 1.868 ± 0.440 |            0.000 |
| R1       | CalPred-style @ 1−α=0.80 | 0.821 ± 0.026 | 0.036 ± 0.015 | 1.884 ± 0.425 |            0.000 |
| R1       | KinCP @ 1−α=0.80         | 0.809 ± 0.014 | 0.026 ± 0.009 | 1.816 ± 0.414 |            0.000 |
| R2       | SCP @ 1−α=0.95           | 0.910 ± 0.054 | 0.050 ± 0.048 | 3.231 ± 0.792 |            0.000 |
| R2       | CV+ @ 1−α=0.95           | 0.909 ± 0.054 | 0.053 ± 0.046 | 3.077 ± 0.686 |            0.000 |
| R2       | Gauss-PEV @ 1−α=0.95     | 0.928 ± 0.039 | 0.040 ± 0.027 | 3.308 ± 0.692 |            0.000 |
| R2       | CalPred-style @ 1−α=0.95 | 0.939 ± 0.021 | 0.028 ± 0.013 | 3.367 ± 0.535 |            0.000 |
| R2       | KinCP @ 1−α=0.95         | 0.945 ± 0.018 | 0.025 ± 0.011 | 3.510 ± 0.547 |            0.000 |
| R2       | SCP @ 1−α=0.90           | 0.828 ± 0.073 | 0.086 ± 0.062 | 2.498 ± 0.566 |            0.000 |
| R2       | CV+ @ 1−α=0.90           | 0.838 ± 0.071 | 0.079 ± 0.058 | 2.464 ± 0.538 |            0.000 |
| R2       | Gauss-PEV @ 1−α=0.90     | 0.881 ± 0.048 | 0.052 ± 0.029 | 2.776 ± 0.581 |            0.000 |
| R2       | CalPred-style @ 1−α=0.90 | 0.891 ± 0.027 | 0.037 ± 0.014 | 2.825 ± 0.449 |            0.000 |
| R2       | KinCP @ 1−α=0.90         | 0.894 ± 0.024 | 0.036 ± 0.015 | 2.830 ± 0.453 |            0.000 |
| R2       | SCP @ 1−α=0.80           | 0.697 ± 0.103 | 0.119 ± 0.089 | 1.848 ± 0.427 |            0.000 |
| R2       | CV+ @ 1−α=0.80           | 0.710 ± 0.100 | 0.113 ± 0.082 | 1.849 ± 0.423 |            0.000 |
| R2       | Gauss-PEV @ 1−α=0.80     | 0.784 ± 0.066 | 0.074 ± 0.035 | 2.163 ± 0.452 |            0.000 |
| R2       | CalPred-style @ 1−α=0.80 | 0.795 ± 0.039 | 0.056 ± 0.021 | 2.201 ± 0.350 |            0.000 |
| R2       | KinCP @ 1−α=0.80         | 0.789 ± 0.035 | 0.052 ± 0.019 | 2.153 ± 0.364 |            0.000 |

**Table 9** Interval validity among the top 10% of candidates selected by predicted value (GBLUP). The columns give medians over units of: coverage among the selected; the share of selected candidates below the lower bound; the mean standardised phenotype of candidates selected by point prediction versus by lower bound, and the median difference between the two with its Wilcoxon P-value; and the overlap between the two selected sets.

| Regime   | Method        |   n_units |   median_sel_coverage |   median_sel_below_lower |   median_gain_point |   median_gain_lower |   median_gain_diff |   wilcoxon_p |   median_overlap |
|:---------|:--------------|----------:|----------------------:|-------------------------:|--------------------:|--------------------:|-------------------:|-------------:|-----------------:|
| R1       | CV+           |        24 |                 0.891 |                    0.045 |               1.020 |               1.031 |              0.001 |        0.833 |            0.921 |
| R1       | CalPred-style |        24 |                 0.903 |                    0.053 |               1.020 |               1.019 |             -0.005 |        0.037 |            0.903 |
| R1       | Gauss-PEV     |        24 |                 0.891 |                    0.050 |               1.020 |               1.010 |             -0.006 |        0.121 |            0.931 |
| R1       | KinCP         |        24 |                 0.894 |                    0.050 |               1.020 |               1.009 |             -0.011 |        0.005 |            0.874 |
| R1       | KinCP-ABC     |        24 |                 0.894 |                    0.047 |               1.020 |               1.020 |              0.000 |      nan     |            1.000 |
| R1       | SCP           |        24 |                 0.891 |                    0.048 |               1.020 |               1.017 |             -0.004 |        0.136 |            0.845 |
| R2       | CV+           |        24 |                 0.857 |                    0.047 |               0.525 |               0.458 |              0.006 |        0.663 |            0.909 |
| R2       | CalPred-style |        24 |                 0.899 |                    0.042 |               0.525 |               0.580 |             -0.013 |        0.330 |            0.903 |
| R2       | Gauss-PEV     |        24 |                 0.889 |                    0.042 |               0.525 |               0.630 |             -0.002 |        0.989 |            0.925 |
| R2       | KinCP         |        24 |                 0.891 |                    0.043 |               0.525 |               0.552 |             -0.007 |        0.422 |            0.867 |
| R2       | KinCP-ABC     |        24 |                 0.828 |                    0.069 |               0.525 |               0.525 |              0.000 |      nan     |            1.000 |
| R2       | SCP           |        24 |                 0.834 |                    0.055 |               0.525 |               0.460 |             -0.006 |        0.317 |            0.778 |

## Figure legends

**Figure 1** Kinship-aware conformal prediction (KinCP). (A) Random and genomic-cluster cross-fitting inside the training set produce a pool of out-of-fold residuals together with each residual's relatedness covariate d, the GBLUP prediction error variance in σ²_g units (Equation 1), computed relative to the inner training subset. (B) Scores are normalised by the predictive standard deviation implied by d. (C) For each candidate, the conformal quantile is computed with kernel weights in log d (Equation 2); the candidate's own unit weight is placed at +∞.

Alt text: Flow diagram. Genotypes and training phenotypes feed an outer model fit. Two cross-fitting schemes (random and genomic-cluster folds) produce residuals and relatedness values, which are normalised and kernel-weighted to give an interval for each candidate.

**Figure 2** Datasets and relatedness of test candidates. (a) Number of genotyped individuals (n) and polymorphic markers (m) in each EasyGeSe dataset. (b) Distribution of the relatedness covariate d (log10 scale) for test candidates under random cross-validation (R1) and cluster-out validation (R2), shown for the first selected trait of each dataset. Boxes show the interquartile range and whiskers 1.5 × IQR. Larger d means weaker relatedness to the training set.

Alt text: Left: horizontal bars of sample sizes for ten species, ranging from about 320 to 4,400 individuals. Right: paired box plots per species; cluster-out candidates have systematically larger d than random-CV candidates.

**Figure 3** Coverage of 90% prediction intervals by quintile of relatedness to the training set (GBLUP base predictor). Points are means over 24 dataset × trait units, with 95% bootstrap confidence intervals. Q1 contains the candidates most closely related to the training set; Q5 the least related. The dashed line marks the 0.90 target.

Alt text: Three panels of line plots, one per validation regime. Split conformal and CV+ fall from about 0.93 coverage for close relatives to about 0.88 for distant ones under random CV, and to about 0.81 to 0.84 under cluster-out validation. KinCP, CalPred-style and Gauss-PEV stay near 0.90 across quintiles.

**Figure 4** Marginal coverage of 90% intervals for every dataset × trait unit under random (R1) and cluster-out (R2) validation (GBLUP base predictor).

Alt text: Dot plot with one row per species and trait. Under cluster-out validation, split conformal and CV+ fall below 0.80 for several units, while KinCP points cluster closer to 0.90.

**Figure 5** Ablation of KinCP components (GBLUP base predictor): (A) relatedness-diverse calibration pool, (B) PEV-normalised scores, (C) localisation in log d. Bars show the mean relatedness-conditional coverage error over units; error bars are 95% bootstrap confidence intervals.

Alt text: Horizontal bar charts for random and cluster-out validation, comparing the full method with every subset of its three components. Under cluster-out validation, removing the diverse calibration pool raises the error most.

**Figure 6** Generalisation across base predictors. Marginal coverage (a) and relatedness-conditional coverage error (b) for GBLUP, RKHS regression and LightGBM under random (R1) and cluster-out (R2) validation. Means over units with 95% bootstrap confidence intervals. Gauss-PEV is not shown because it exists only for GBLUP.

Alt text: Two panels of grouped point estimates by base predictor and regime, comparing split conformal, CV+, CalPred-style and KinCP.

**Figure 7** Simulation with known genetic values on real loblolly pine, pig and maize genotypes (additive traits; 10 or 1,000 QTL; five replicates). (a) Worst-quintile coverage and (b) relatedness-conditional coverage error by regime and heritability. Means over genotype sets, QTL numbers and replicates, with 95% bootstrap confidence intervals.

Alt text: Two panels of point estimates by regime and heritability, comparing five interval methods.

**Figure 8** Computational cost per outer fold (one CPU thread) against training-set size: a single model fit versus the ten cross-fitted fits used to build KinCP's calibration pools, for each base predictor.

Alt text: Log-log scatter plot. Pool construction costs roughly ten single fits for every base predictor and training-set size.

**Figure 9** Sensitivity analyses (GBLUP). (a) Relatedness-conditional coverage error of KinCP for localisation bandwidths h = 0.25–2 (in units of SD(log d)), without the mass floor, and with floors n_min = 25 and 100. (b) Coverage minus nominal coverage at 1 − α = 0.80, 0.90 and 0.95. Solid lines: R1; dotted lines: R2.

Alt text: Left: line plot of error against bandwidth variant for the two regimes. Right: coverage deviation at three nominal levels for five methods.

**Figure 10** Error analysis under cluster-out validation (GBLUP). Marginal coverage of each unit against (a) the excess kurtosis of the phenotype and (b) the predictive ability of GBLUP.

Alt text: Two scatter plots comparing Gauss-PEV and KinCP coverage across units.

**Figure 11** Interval validity among selected candidates. In each outer fold the top 10% of candidates by predicted value were selected. (a) Coverage among the selected candidates. (b) Share of selected candidates whose phenotype fell below the lower interval bound (target 0.05 for a two-sided 90% interval). Means over units with 95% bootstrap confidence intervals.

Alt text: Two panels of point estimates for random and cluster-out validation, comparing five interval methods among selected candidates.

**Figure 12** Paired comparison of relatedness-conditional coverage error, competitor minus KinCP (GBLUP; positive values favour KinCP). Points are median paired differences across units, with 95% bootstrap confidence intervals. Asterisks mark Holm-adjusted P < 0.05 (two-sided Wilcoxon signed-rank tests).

Alt text: Forest plots for three regimes, showing one median difference with its confidence interval for each competing method.

