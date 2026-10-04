[Date]

The Editor-in-Chief
GENETICS
Genetics Society of America

Dear Editor,

We submit our manuscript **"Relatedness-aware calibration of genomic prediction intervals: kinship-aware conformal prediction across ten plant and animal species"** for consideration as an Investigation in GENETICS, in the area of Systems & Computational Genetics (statistical methods / genomic prediction).

**What the manuscript does.** Breeders act on individual genomic predictions, so they need uncertainty statements that are valid for the candidates actually being selected. Distribution-free conformal intervals are increasingly proposed for this purpose. We show that their guarantee is undermined in breeding data along a known quantitative-genetic axis: the relatedness of each candidate to the training population. We measure this relatedness with the GBLUP prediction error variance and propose kinship-aware conformal prediction (KinCP), which has three components: a calibration pool spanning close and distant relatives, PEV-normalised scores, and localisation in the relatedness metric.

The study covers 24 traits from ten species in the EasyGeSe resource, three prediction models, three deployment regimes, and simulations on real genotypes with known genetic values:
* Relatedness-blind conformal intervals (split conformal, CV+) over-cover close relatives and, along the PEV-based relatedness covariate, under-cover distant candidates. For candidates from held-out genomic clusters, their mean coverage of nominal 90% intervals fell to 0.828–0.838.
* KinCP achieved the lowest, or joint-lowest, relatedness-conditional coverage error in all deployment regimes and for all three predictors (GBLUP, RKHS, LightGBM). The classical PEV-based Gaussian interval lost calibration under cluster-out deployment (mean coverage 0.881; KinCP 0.894).
* Ablations and competitor analyses show that a relatedness-diverse calibration pool, rather than conformalisation itself, is the decisive ingredient. Within a single known regime, simpler fixes (a parametric calibration on the same pool, or group CV+ for new clusters) perform comparably. We report this openly and give practical recommendations.

**Why GENETICS.** The work joins classical quantitative-genetic theory (prediction error variance, reliability and the effect of relatedness, a tradition with deep roots in GENETICS, e.g. Habier *et al.* 2007; Wientjes *et al.* 2013) with modern distribution-free inference. It continues the journal's recent genomic-prediction methods literature, for example Gibbs, Paril and Fournier-Level (2025, doi:10.1093/genetics/iyaf003) and Ahlinder and Waldmann (2026, doi:10.1093/genetics/iyag205).

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
