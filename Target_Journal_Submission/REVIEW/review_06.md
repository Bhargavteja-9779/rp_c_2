# Review round 6 — Reviewer #6 (computational complexity, latency, memory, scalability, deployment)

These points are new relative to Reviewers #1–5.

## Questions
1. Is the improvement worth its computational cost?
2. Are the reported costs measured fairly? The original per-fold timings were taken while four jobs shared four cores.
3. How does the cost scale, and where does the method stop being feasible?
4. Memory?
5. Is deployment realistic: do breeders have to refit everything for each candidate batch?

## Findings
**P1 (MAJOR). Contended timings.**
* *Problem:* Table 7 timings come from the main runs, in which four worker processes shared four CPU cores. Ratios are interpretable, but absolute times are inflated and noisy.
* *Fix:* run a controlled benchmark on an idle machine with one thread.

**P2 (MAJOR). No memory figures.** Dense *n* × *n* relationship matrices dominate memory, and this must be reported.

**P3 (MODERATE). LightGBM cost.** For tree models the pools cost about 8× a single fit, because the inner fits are full refits. That is still "two cross-validation runs", but it should be stated per predictor.

**P4 (MODERATE). Scalability ceiling.** Dense GBLUP at 10⁵–10⁶ animals (national dairy evaluations) is infeasible, so the method as implemented applies to plant-breeding and moderate-size animal panels. The text must say so and point to approximate reliabilities for large evaluations.

**P5 (MINOR). Deployment cost.** The pools depend only on the training set, so they are built once per training set and reused for any number of candidate batches. Interval computation per candidate is cheap. Say so.

## Verdict on cost–benefit
* *Cost:* the extra cost is about two cross-validations. For kernel models this is less than one REML fit (the fixed-δ Cholesky inner fits are cheap).
* *Benefit:* calibration is restored for weakly related candidates, which is where uncertainty statements matter.
* *Caveat:* there is no improvement in interval score.
* *Overall:* worth it whenever intervals will be used as risk statements. Not worth it if only point rankings matter.

---
# Author response and changes (Round 6)

| Issue | Action | Status |
|---|---|---|
| P1 | **New benchmark** `scripts/benchmark_scaling.py`: idle machine, one thread, maize genotypes, *n*_train ∈ {500, 1000, 2000, 3500}, 3 replicates. At *n* = 3,500: REML fit 10.0 s, both pools 7.3 s, intervals 0.07 s for 300 candidates. Time exponent about 2.0 over this range. `results/scaling.csv`; Figure 8 replaced. | Fixed (experiment run) |
| P2 | Peak traced memory reported: about 303 MB at *n* = 3,500, with exponent about 1.7 (*n*² matrices). | Fixed |
| P3 | Per-predictor overhead ratios are reported in the text (GBLUP 1.9×, RKHS 1.3×, LightGBM 8.3×) and in Table 7. | Fixed |
| P4 | Scale limitation added to Discussion, citing approximate reliability methods (Misztal *et al.* 2013, DOI-verified). | Fixed |
| P5 | Sentence added (see below). | Fixed |
