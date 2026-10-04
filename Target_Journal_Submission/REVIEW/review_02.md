# Review round 2 — Reviewer #2 (novelty, prior art, contribution differentiation)

This review deliberately does not repeat Reviewer #1's points, which covered the phenotype target, species-level tests and the framing of KinCP against a parametric calibration.

## Questions asked
1. Is the claimed gap real, or constructed?
2. Is each KinCP component new, or a renamed known tool?
3. Has relevant prior art been missed?
4. Is the contribution incremental relative to CalGS, CalPred, PredInterval and weighted/localized CP?

## Findings

### FATAL
None. Targeted searches found no published method that calibrates genomic-prediction intervals conditionally on relatedness in breeding populations. We searched PubMed for "conformal" with genomic prediction/selection, breeding values and polygenic; arXiv for "conformal" with genomic, polygenic and breeding; and the web, bioRxiv and Zenodo, all on 2026-10-04. The closest items are listed below.

### MAJOR
**N1. Components B and C are classical conformal tools, and the manuscript under-credits this.**
* PEV-normalised scores are a special case of normalised / locally weighted conformal prediction (Papadopoulos *et al.* 2002; Lei *et al.* 2018).
* Kernel-weighted quantiles are localized / weighted conformal prediction (Guan 2023; Tibshirani *et al.* 2019).
* The text must say plainly that the novelty lies in (i) the choice of covariate (GBLUP PEV, from quantitative-genetic theory), (ii) the calibration-pool design, and (iii) the empirical demonstration. It does not lie in new conformal machinery.

**N2. Missing prior art on group-conditional (Mondrian) conformal prediction for polygenic scores across ancestries.**
* Sun *et al.* (2021, *Nat Commun*) and Kodji *et al.* (2026, *PLoS Comput Biol*) used Mondrian cross-conformal prediction for PRS-based disease risk, including across ancestries.
* Discrete group-conditional guarantees also exist: Vovk (2013); Dunn *et al.* (2023) for hierarchical groups; Bhattacharyya and Barber (2026) for group-weighted CP.
* These must be cited. The authors must also justify continuous localisation over a simpler Mondrian scheme with bins of *d*, preferably empirically.

**N3. Is the "gap" just the known inflation of random CV in structured populations?**
* Werner *et al.* (2020) and many others showed that random CV overstates accuracy in structured populations.
* The authors should state what is new beyond "random CV is optimistic". The new point is that *uncertainty statements* calibrated by random hold-outs are miscalibrated in a relatedness-dependent way, *even when marginal coverage looks nominal* (R1), and that this can be corrected without candidate phenotypes.

### MODERATE
1. *Human-genetics framing.* CalPred's contexts include genetic distance or principal components. Explain why a breeding population is a harder case: dense family structure, and candidates from new crosses.
2. *Title.* "Kinship-aware" might suggest a pedigree-kinship (A-matrix) method. Clarify that genomic relationships are used. The title is acceptable as long as the abstract defines the term.
3. *Novelty boundary.* State explicitly what is *not* claimed: a new conformal theorem, or superiority over a parametric calibration on the same pool.

### MINOR
1. The *Kumar 2026* citation should state that it is a data paper and code archive on Zenodo, not peer reviewed.

## Recommendation
Minor-to-major revision. The contribution is real but must be positioned precisely.

---
# Author response and changes (Round 2)

| Issue | Action | Status |
|---|---|---|
| N1 | The Introduction now attributes B to normalised/locally weighted CP (Papadopoulos *et al.* 2002; Lei *et al.* 2018) and C to localized/weighted CP (Guan 2023; Tibshirani *et al.* 2019). A "What is and is not new" paragraph has been added. | Fixed |
| N2 | Cited Sun *et al.* 2021, Kodji *et al.* 2026, Vovk 2013, Dunn *et al.* 2023 and Bhattacharyya and Barber 2026. **New experiment:** a Mondrian alternative to C ("Mondrian-d": pool A, PEV-normalised scores, separate conformal quantiles within quintile bins of log *d*) was added to the exploratory jobs (GBLUP, R1 repeat 1 and R2 seed 11, all 24 units). It is reported with the D6 exploratory results. | Fixed (experiment run) |
| N3 | Discussion first subsection: added an explicit statement of what goes beyond the known optimism of random CV. | Fixed |
| Moderate 1 | Discussion: added a sentence on why family-structured breeding populations are a harder case. | Fixed |
| Moderate 2 | The Abstract and Introduction now say "genomic relationships", and the term is defined at first use. | Fixed |
| Moderate 3 | Claim-boundary sentence added to the Introduction. | Fixed |
| Minor 1 | The reference entry now reads "[data paper and code]" and identifies Zenodo. | Fixed |
