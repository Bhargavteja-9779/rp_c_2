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

### What KinCP adds over simpler fixes

Two simpler fixes each capture part of KinCP's behaviour.
* *Rescaling.* Under cluster-out deployment, relatedness-blind intervals were mainly too narrow overall. A single correct inflation factor would repair most of the problem, but that factor cannot be known without phenotypes of the candidates.
* *Group CV+.* CV+ with genomic-cluster folds sets the level appropriately for new clusters but is conservative for close relatives.

KinCP combines both kinds of residuals and lets each candidate's relatedness decide which applies. This is why it remained calibrated in both regimes. The comparison also shows that the deployment regime matters: a practitioner who knows candidates will come from new families can use group CV+. One who does not, or whose candidates are a mixture of close and distant relatives, benefits from conditioning on relatedness.

### Relation to classical reliability and accuracy validation

The classical PEV interval was competitive under random cross-validation, which is the regime in which it is usually checked. It lost calibration under cluster-out deployment, mostly for traits with high within-cluster heritability. This complements the LR method of Legarra and Reverter (2018), which validates *population-level* accuracy and dispersion of predictions. Our endpoints assess *individual-level* interval calibration conditional on relatedness. Both kinds of validation are needed. Neither replaces a deployment-matched validation design (Werner *et al.* 2020).

### Practical recommendations

1. **Report calibration conditional on relatedness**, not only marginal coverage. Random cross-validation can show nominal marginal coverage while systematically misstating uncertainty for distant candidates.
2. **Build the calibration pool by cross-fitting with both random and genomic-cluster folds** whenever candidates may come from new families or sub-populations. If all candidates are known to come from new clusters, CV+ with cluster folds is a simpler alternative.
3. **Use the GBLUP PEV as the relatedness covariate**, even when the point predictor is a kernel or tree model.
4. **Use intervals to qualify, not replace, rankings.** Ranking by lower bounds did not increase mean selected phenotypes. Its value lies in identifying candidates whose predictions are unreliable, consistent with the uncertainty-aware selection framework of Ahlinder and Waldmann (2026).

### Limitations

* **Coverage target.** Coverage is assessed for observed phenotypes (the quantity breeders observe). It is not assessed for true breeding values, which are unknown in real data. The simulation reports calibration with known genetic values only as a diagnostic.
* **Guarantee.** KinCP's guarantee is approximate. The pool residuals come from models fitted to subsets of the training set, and the invariance of scores given relatedness is an assumption that we tested empirically rather than proved. A residual under-coverage remained for the least-related candidates under cluster-out deployment.
* **Deployment regimes are proxies.**
  * *Clusters.* Genomic clusters stand in for new families or populations. Five clusters per dataset give few independent deployment groups, so coverage under R2 is itself estimated with sizeable error.
  * *No temporal data.* Temporal deployment across breeding cycles, which also involves genotype-by-environment and selection effects, could not be studied because the public datasets lack cycle information. Validation against real pedigree groups was possible only for eastern oyster, whose four F2 families are identified in the data.
* **Phenotype preprocessing.** Some EasyGeSe phenotypes are BLUEs adjusted across all lines and environments (e.g. maize, barley). Test and training phenotypes may therefore share adjusted environmental effects. This mild preprocessing leakage applies equally to all methods.
* **R1 advantage.** Under random cross-validation, KinCP's advantage was small and specific to calibration along *d*. It was not significant when relatedness was measured by maximum genomic relationship.
* **Statistical units.** Traits from the same species share genotypes, so the 24 units are not fully independent. The pattern was, however, consistent across species (Figure 4).
* **Trait choice.** Traits were chosen by a rule fixed in advance. In loblolly pine this selected two closely related root traits.
* **Compute.** LightGBM was not run on maize, and the RKHS and LightGBM analyses used fewer repeats than GBLUP, both for compute reasons.
* **Scale.** All computations use dense relationship matrices. For national animal-breeding evaluations with 10⁵–10⁶ genotyped animals, the PEV in Eq. (1) would need the approximate reliability methods used in large-scale evaluation (e.g. Misztal *et al.* 2013). The cross-fitted pools would need to be built on subsamples. We did not test this.
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
