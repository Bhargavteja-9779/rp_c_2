# Review round 3 — Reviewer #3 (statistical validity, experimental fairness, leakage)

These points are new relative to Reviewers #1 and #2.

## MAJOR
**S1. Endpoint–method alignment.**
* *Problem:* The primary endpoint bins test individuals by *d*, which is exactly the covariate KinCP localises on. A method that equalises coverage across bins of *d* will score well on this endpoint by construction, even if it is no better calibrated with respect to relatedness in general.
* *Fix:* evaluate conditional coverage on quintiles of a relatedness measure that KinCP does not use, such as the maximum standardised genomic relationship to the training set.

**S2. Correlated repeats.**
* *Problem:* Under R1, the five EasyGeSe repeats re-use the same individuals; under R2, the five seeds share identical outer folds and differ only in inner randomness. The "mean ± SD over units" in Table 2 is fine. But per-unit uncertainty from repeats must not be read as independent replication.
* *Fix:* state this.

**S3. Baseline fairness.**
* *SCP:* fits on only 80% of the training set by design. This is inherent to split conformal and should be stated, not "fixed".
* *CalPred-style:* receives pool A, which is fair. *Gauss-PEV:* uses REML on the full training set, which is fair.
* *LightGBM:* hyper-parameters were fixed, not tuned. This affects every interval method equally, because they all share the same base predictor. It should still be noted that point accuracy for LightGBM may be sub-optimal.

**S4. Upstream phenotype preprocessing.**
* *Problem:* For some datasets (e.g. maize and barley), EasyGeSe provides BLUEs estimated across all lines and environments. Phenotypes of test individuals may therefore share adjusted environmental effects with training individuals. This is a mild form of preprocessing leakage that affects all methods equally.
* *Fix:* state this as a limitation.

## MODERATE
1. *Holm families.* These span three regimes and seven competitors per endpoint (21 tests). This is conservative. Keep it, but say so.
2. *Wilcoxon ties.* Ties were handled with `zero_method="wilcox"`, which drops zero differences. Report the number of units actually used (already in Table 3 as "Units").
3. *Bootstrap CI of the median.* With 24 units, percentile CIs of the median can be asymmetric (e.g. CV+ in R2: 0.007 to 0.064). This is acceptable, but readers should be warned that the CI reflects heterogeneity between units.

## MINOR
1. Report the number of R2 test folds that were skipped because they had fewer than five test individuals. This can happen for pine, where one k-means cluster has three individuals.

---
# Author response and changes (Round 3)

| Issue | Action | Status |
|---|---|---|
| S1 | **New analysis:** `secondary_analyses.py::alt_relatedness_endpoint` computes conditional coverage error on quintiles of *maximum standardised genomic relationship to the training set* (maxkin) for every main job, with paired Wilcoxon/Holm tests (`alt_relatedness_statistics.csv`). Result: under **R2**, KinCP remained better than Gauss-PEV, CV+, SCP and the CalPred-style random-pool calibration (Holm *P* ≤ 0.001). Under **R1 and R3** the differences were small and not significant. The random-CV advantage on the primary endpoint therefore partly reflects alignment between endpoint and method. Results and Discussion now say this explicitly, and the R1 claims are tempered. | Fixed (analysis run; claims revised) |
| S2 | Methods state that R1 repeats and R2 seeds are not independent replicates. | Fixed |
| S3 | Methods state the SCP data split and the untuned LightGBM hyper-parameters. | Fixed |
| S4 | Added to Limitations. | Fixed |
| Moderate 1–3 | Holm family statement and CI-interpretation note added. | Fixed |
| Minor 1 | Skipped folds are counted from the timing logs and reported in Methods: the number of R2 folds analysed is compared with the expected number. | Fixed |
