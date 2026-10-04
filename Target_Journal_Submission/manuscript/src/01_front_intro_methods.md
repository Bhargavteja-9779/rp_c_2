# Relatedness-aware calibration of genomic prediction intervals: kinship-aware conformal prediction across ten plant and animal species

**Running title:** Relatedness-aware genomic prediction intervals

[Author names to be inserted]¹

¹[Affiliation to be inserted]

**Corresponding author:** [Name, address, e-mail to be inserted]

**Keywords:** genomic prediction; genomic selection; prediction interval; conformal prediction; prediction error variance; genomic relationship; uncertainty quantification; GBLUP

## Abstract

Genomic prediction guides selection in plant and animal breeding, but breeders acting on an individual prediction also need honest uncertainty. Distribution-free conformal prediction intervals assume that calibration individuals are exchangeable with selection candidates; we show that relatedness to the training population breaks this assumption. We measure each candidate's relatedness by the prediction error variance of genomic best linear unbiased prediction and propose kinship-aware conformal prediction, which calibrates on residuals from random and genomic-cluster cross-fitting, normalises them by this variance and localises the conformal quantile in relatedness. We compared it with seven alternatives on {{n_units}} traits from barley, common bean, lentil, loblolly pine, eastern oyster, maize, pig, rice, soybean and wheat, under random and cluster-out validation, with three prediction models, and in simulations on real genotypes. {{abstract_results}} {{abstract_conclusion}}

## Article summary

{{article_summary}}

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

Traits were selected by a rule fixed in advance that does not look at results. A trait was eligible if it had at least 200 phenotyped individuals and at least 30 distinct values. Within each dataset we took up to three eligible traits with the largest number of records, breaking ties by column order. This gave {{n_units}} dataset × trait units (Table 1).

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

For a training set *S* (the outer training set *T*, or an inner subset of it) and a candidate *j* with relationship vector *k* = *G*_{S,j}, let *V* = *G*_{S,S} + δ*I*. The prediction error variance of the GBLUP phenotype prediction (universal kriging form, including the uncertainty of the estimated mean) is σ²_g *d*ⱼ + σ²_e, with

*d*ⱼ = *G*ⱼⱼ − *k*ᵀ*V*⁻¹*k* + (1 − 1ᵀ*V*⁻¹*k*)² / (1ᵀ*V*⁻¹1).     (1)

*d*ⱼ is the PEV of the genetic value in units of σ²_g. It is small for candidates with many close relatives in *S* and approaches *G*ⱼⱼ for unrelated candidates; 1 − *d*ⱼ/*G*ⱼⱼ is the classical reliability. *d*ⱼ depends only on genotypes, on the training set and on δ. It can therefore be computed for any candidate and used with any base predictor. All variance components came from the outer training set.

### Prediction-interval methods

Let *ŷ*ⱼ be the base prediction for candidate *j* from the model fitted on the training set *T*, and let σ(*d*) = (σ̂²_g *d* + σ̂²_e)^{1/2}. The nominal coverage was 1 − α = 0.90; α = 0.05 and 0.20 were used for sensitivity analyses. Eight methods were compared: KinCP and seven alternatives. CalPred-style calibration was fitted in two variants, which are counted as one alternative.

1. **Gauss-PEV** (GBLUP only): *ŷ*ⱼ ± *z*_{1−α/2} σ(*d*ⱼ). This is the classical model-based interval.
2. **Gauss-homosc**: *ŷ*ⱼ ± *z*_{1−α/2} times the standard deviation of random five-fold out-of-fold residuals in *T*.
3. **SCP** (split conformal): the model is refitted on a random 80% of *T* (at least 10 individuals are kept for calibration). With absolute residuals *R*ᵢ on the remaining 20% (*n*_c individuals), the interval is *ŷ*ⱼ ± the ⌈(1 − α)(*n*_c + 1)⌉-th smallest *R*ᵢ (Lei *et al.* 2018).
4. **NormCP**: as SCP, with scores *R*ᵢ/σ(*d*ᵢ) and half-width scaled by σ(*d*ⱼ). This is component B alone, with *d* measured relative to the 80% fitting subset.
5. **CV+** (Barber *et al.* 2021): random five-fold cross-fitting in *T*. Here *ŷ*ⱼ^{(−k(i))} is the prediction for *j* from the model fitted without the fold *k*(*i*) that contains training individual *i*, and *R*ᵢ is the absolute out-of-fold residual of *i*. The bounds are the ⌊α(*n* + 1)⌋-th smallest of {*ŷ*ⱼ^{(−k(i))} − *R*ᵢ} and the ⌈(1 − α)(*n* + 1)⌉-th smallest of {*ŷ*ⱼ^{(−k(i))} + *R*ᵢ}.
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

Two further cluster-out variants tested the sensitivity of R2 to cluster granularity, both with GBLUP and one seed: *k*-means with *k* = 3 and with *k* = 10 deployment clusters. KinCP's inner folds were left at *k* = 5 in both. For eastern oyster, whose individuals belong to four F2 families identified in the EasyGeSe identifiers, each family was also held out in turn (five seeds). These analyses were added at the request of internal review, after the main results had been seen.

RKHS was run on R1 (first repeat) and R2 (two seeds). LightGBM was run on R1 (first repeat) and R2 (one seed), and not on maize (compute; deviation D5).

Phenotype scaling, REML, hyper-parameters, cross-fitting, calibration scores and the variance components in σ(*d*) used outer-training individuals only. Inner cross-fitting reused the outer-fold δ (deviation D3). Seeds {11, 22, 33, 44, 55} were fixed in advance and tied to repeats. No seed was selected after viewing results. The R1 repeats re-use the same individuals, and the R2 seeds share identical outer folds and differ only in inner randomness, so neither is an independent replicate. Test folds with fewer than five individuals were skipped. This affected only one loblolly-pine cluster of three trees, leaving {{n_folds_r2_pine}} of 25 R2 folds per pine trait.

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

### Robustness analyses requested by internal review

The following analyses were added after the main results had been seen (deviation D7):
* the granularity and family regimes described above;
* conditional coverage on quintiles of maximum genomic relationship;
* species-level paired tests, averaging traits within species (10 units);
* a PEV-calibration diagnostic in the simulation, comparing the realised mean squared error of the genetic-value prediction with σ̂²_g *d* by quintile of *d*;
* a single-thread scaling benchmark on random subsets of the maize genotypes;
* two competitor analyses:
  * an *oracle rescaling*, in which each method's intervals were rescaled about their centre by the one constant giving exactly 0.90 pooled coverage on the test data, before recomputing the conditional error;
  * *group CV+*, i.e. CV+ computed with the genomic-cluster folds of pool A, alone or combined with the random folds (GBLUP, R1 first repeat and R2 first seed).

### Software, reproducibility and pre-specification

The analysis uses Python 3.11, NumPy, SciPy, scikit-learn and LightGBM. All computations ran on a 4-core CPU without a GPU. A single command (`python run_all.py --mode full`) regenerates every result, table and figure from the public data, and every number in this article is inserted automatically from the generated result files. The study design was committed to version control before any model was fitted. File S1 lists all seven deviations from the pre-specified design: five made for compute reasons or found in a pipeline smoke test, and two (the exploratory variants and the robustness analyses requested by internal review) added after the main results had been seen.
