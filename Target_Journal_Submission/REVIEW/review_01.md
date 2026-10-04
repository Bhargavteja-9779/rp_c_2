# Review round 1 — Reviewer #1 (general referee for GENETICS)

**Manuscript:** Kinship-aware conformal prediction intervals for genomic prediction across ten plant and animal species
**Version reviewed:** first complete draft (simulations on maize still running)

## Summary of the submission
The authors argue that relatedness to the training set breaks the exchangeability assumption of conformal prediction intervals in breeding data. They propose KinCP:
* a calibration pool from random and genomic-cluster cross-fitting;
* scores normalised by GBLUP PEV;
* localisation of the quantile in PEV.

It is benchmarked on EasyGeSe (10 species, 24 traits), three predictors, three regimes and a simulation.

## Assessment

### FATAL
None identified. The data are public, the experiments exist, and the claims are mostly supported.

### MAJOR
**M1. Target of coverage.**
* *Problem:* Breeders select on genetic merit, but every interval is evaluated against observed phenotypes. The paper must state this clearly in the abstract or introduction. The simulation records the true genetic values, so it should show whether the relatedness covariate *d* is a calibrated measure of the genetic prediction error. Otherwise the "quantitative-genetic" justification is asserted rather than shown.
* *Fix:* add a PEV-calibration diagnostic in the simulation: by quintile of *d*, compare the realised mean squared error of the genetic-value prediction with σ²_g·*d*.

**M2. Non-independence of units.**
* *Problem:* The 24 units include up to three traits per species, and traits of one species share genotypes and folds. Wilcoxon tests over the 24 units overstate the effective sample size.
* *Fix:* repeat the primary tests with species as the unit (10 units, averaging traits within species).

**M3. The method's added value over a parametric calibration is not demonstrated.**
* *Problem:* KinCP ties with CalPred-style calibration on pool A. The title and abstract present KinCP as the contribution. Either the framing should centre on the calibration design (pool A + PEV covariate) or the authors must give a reason to prefer KinCP.
* *Fix:* revise the framing in the Introduction, Discussion and cover letter, and state the reason for preferring KinCP (distribution-free quantiles) honestly. The abstract already says the pool is decisive, which is good.

**M4. Choice of five clusters for R2.**
* *Problem:* The cluster-out regime uses *k* = 5 k-means clusters. Coverage under cluster-out deployment could depend strongly on the granularity of the clusters.
* *Fix:* add a sensitivity analysis with a different *k*. This is deferred to the reviewer focused on external validity (Round 5); see `review_05.md`.

### MODERATE
1. *Error analysis over-interprets.* "Consistent with variance components estimated within the training clusters overstating how much genetic signal transfers" is a hypothesis, not a finding. Mark it as such.
2. *Selection wording.* Ranking by lower bound *decreased* the selected mean under R1 (median −0.011 SD, *P* = 0.005). "Did not increase" understates this.
3. *Cost reporting.* "1.9×" for ten fits looks contradictory. The outer fit includes REML eigendecomposition, while inner fits reuse δ and only need a Cholesky factorisation. Explain this.
4. *Interval-score results.* These are part of the pre-specified endpoints but are reported only in passing. Report the Holm-adjusted test result for the interval score in the text.
5. *Table 3 readability.* Column names are internal variable names (ref_median, p_holm…). Rename them for publication.
6. *Repeated R1 folds.* The same individual appears in five repeats, so the binomial noise floor is approximate. State this.

### MINOR
1. "KinCP had the lowest … of all methods in every regime": specify that this refers to GBLUP and the eight compared methods (Table 2).
2. Reference list formatting ("et al.." double period; capitalised author names) has been checked and is now fixed.
3. The Abstract mentions "seven alternatives" while the Methods list eight methods including KinCP. These are consistent, but make the count explicit in the Methods.

## Recommendation
Major revision.

---
# Author response and changes (Round 1)

| Issue | Action | Status |
|---|---|---|
| M1 | Added a PEV-calibration diagnostic: `secondary_analyses.py::pev_calibration` gives the realised MSE of ĝ against σ̂²_g·*d* by quintile of *d*, per regime, from the simulation records. Reported in Results (simulation paragraph) and in Table S_pevcal. The Introduction and Limitations now state that coverage is for phenotypes. | Fixed (experiment run) |
| M2 | Added species-level paired tests (`aggregate.py`, 10 species units; traits averaged within species) to `statistics_species.csv` and the Results. | Fixed (analysis run) |
| M3 | Introduction contribution statement and Discussion reframed: the calibration design (pool A + PEV covariate) is presented as the main contribution, with KinCP as its distribution-free implementation. | Fixed |
| M4 | Deferred to Round 5, where it is addressed with an additional regime (cluster granularity *k* = 3 and *k* = 10). | Addressed in Round 5 |
| Moderate 1 | Reworded as a hypothesis ("one explanation consistent with …"). | Fixed |
| Moderate 2 | Reworded: under R1, lower-bound ranking slightly *reduced* the selected mean. | Fixed |
| Moderate 3 | Cost paragraph now explains the REML (eigendecomposition) outer fit versus the fixed-δ inner Cholesky fits. | Fixed |
| Moderate 4 | Interval-score paired tests are now reported in the text. | Fixed |
| Moderate 5 | Table 3 columns renamed. | Fixed |
| Moderate 6 | Noise-floor caveat added in Methods. | Fixed |
| Minor 1–3 | Wording made specific; method count stated. | Fixed |
