# Review round 8 — Reviewer #8 (competing researcher with a similar method)

**Stance:** "I work on conformal calibration of genomic predictions. I believe your gains come from wider intervals, from an under-tuned baseline, and from a benchmark that suits your design." Each attack below is new relative to Reviewers #1–7.

## Attacks

**A1. "It is just width."** (MAJOR)
* *Argument:* Under R2, KinCP's intervals are wider than CV+'s (2.83 *vs.* 2.46 SD). Any method inflated by about 15% would look as good.
* *Test:* rescale every method by an oracle constant that gives exactly 90% marginal coverage on the test data, then compare conditional errors.

**A2. "You gave CV+ the wrong folds."** (MAJOR)
* *Argument:* The natural competitor is CV+ with *group* folds (genomic clusters), which is standard practice for structured data. Comparing against random-fold CV+ is a straw man.
* *Test:* run group CV+ and a combined-fold CV+.

**A3. "Your proper score says otherwise."** (MAJOR)
* *Argument:* On the interval score, KinCP is not better than CV+ or Gauss-PEV.
* *Already addressed:* this was found and reported in an earlier round (Results "Interval score"; Abstract "gains were in calibration, not in interval score"). The reviewer checked that the wording is not hedged. ✓

**A4. "The ablation hides that pool A is a known trick."** (MODERATE)
* *Argument:* Group cross-validation for structured data is old.
* *Response checked:* the paper now explicitly calls the pool the main contribution *in this context* and cites the structured-CV literature (Werner *et al.* 2020). The novelty claim is bounded in the Introduction. ✓

**A5. "The benchmark favours you: EasyGeSe panels are small and highly structured."** (MODERATE)
* *Partly addressed* by the granularity, family, dedup and simulation analyses.
* *Remaining:* no large commercial populations were tested. Stated in Limitations. ✓

## Results of the new tests (run in this round)

| Attack | Result | Consequence for the claims |
|---|---|---|
| A1 | Oracle inflation factors under R2 were 1.19 for CV+, 1.21 for SCP, 1.06 for Gauss-PEV and **1.02 for KinCP**. After rescaling, R2 conditional errors converged: 0.030 for KinCP *vs.* 0.035 for CV+ (*P* = 0.034, unadjusted) and 0.033 for Gauss-PEV (*P* = 0.41). Under R1, rescaled CV+ remained worse (0.025 *vs.* 0.017, *P* < 0.001). | **The attack is partly valid.** Under R2, most of KinCP's advantage is setting the correct overall level. The text now says so, and frames KinCP's contribution there as estimating the level *without candidate phenotypes*. |
| A2 | Group CV+ under R2: coverage 0.915, conditional error 0.042 against 0.037 for KinCP (*P* = 0.22, not significant). Under R1 it was over-conservative: coverage 0.944, conditional error 0.049 against 0.023 (*P* < 0.001). | **The attack is valid for R2.** Group CV+ is an adequate alternative when deployment is known to be cluster-out. KinCP's advantage is being calibrated in both regimes without knowing which applies. Reported in Results ("Competing explanations") and in the Discussion ("What KinCP adds over simpler fixes"). |

## Verdict
The core claim survives in a narrower form: relatedness-aware calibration is necessary, and KinCP achieves it without knowledge of the regime. Claims of superiority over well-chosen simpler fixes are, rightly, not made.

---
# Author response
* New jobs with tag `competitor` (48 jobs) implement group CV+ (`cv_plus(..., which="clus"|"both")`).
* New analysis `secondary_analyses.py::oracle_inflation`.
* Results and Discussion updated, with all numbers token-driven.
* Recommendations revised: "use group CV+ if deployment is known to be to new clusters".
