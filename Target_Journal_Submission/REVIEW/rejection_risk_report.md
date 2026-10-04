# Final rejection-risk report (Phase 41) and self-decision (Phase 42)

Target: **GENETICS** (OUP/GSA), Investigation. No risk is zero, and acceptance cannot be guaranteed.

| # | Risk | Evidence | Severity | Mitigation | Fixed? |
|---|---|---|---|---|---|
| 1 | Novelty: "weighted/localized conformal + group CV is known" | Building blocks are established (Reviewer 2). Group CV+ and a parametric calibration on pool A match KinCP within a known regime (Reviewer 8). | **High** | Contribution reframed as relatedness-aware calibration design plus a multi-species, pre-specified evidence base. Explicit "what is / is not new" paragraph. Honest competitor analyses. | Partly. This is inherent and cannot be removed by experiment. |
| 2 | Methodology: no exact finite-sample guarantee | Subset-fit residuals, duplicated individuals in the pool, deterministic kernel | Moderate | Stated in the "Rationale and guarantees" paragraph. Empirical evaluation with conditional endpoints. Simulation diagnostic shows *d* calibrated (ratio 0.95–1.04). | Disclosed |
| 3 | Dataset: public panels, small to moderate *n*, some BLUE preprocessing upstream, near-duplicates | Data audit; dedup analysis | Moderate | Dedup sensitivity, granularity and family regimes, simulation. Limitations section. | Mostly |
| 4 | Statistics: 24 non-independent units; species-level tests under-powered | Species-level Holm *P* ≈ 0.07 (9/10 species) | Moderate | Species-level analysis reported. Effect sizes and win counts shown. Holm families conservative. | Disclosed |
| 5 | Endpoint alignment (*d*-binned primary endpoint favours KinCP) | Round 3: R1 advantage vanishes on maxkin | Moderate | Independent-measure endpoint reported; R1 claims tempered | Fixed |
| 6 | Reproducibility: per-individual records (326 MB) not in git | README | Low–moderate | Zenodo deposit planned. The full run regenerates them. Summaries are in git. A clean-clone quick run is verified. | Partly (needs the Zenodo DOI at submission) |
| 7 | Baselines: LightGBM untuned; RKHS and LightGBM have fewer repeats; no LightGBM on maize | D2, D5 | Low | Same base predictor for all interval methods; disclosed | Disclosed |
| 8 | Generalisation: no temporal or cross-environment deployment; real families in one species only | Round 5 | Moderate | Stated as a limitation; granularity robustness shown | Disclosed |
| 9 | Writing: long Results (13 sub-analyses) | Round 10 | Low | Organised by research question; GENETICS has no length limit | Accepted |
| 10 | Target-journal formatting | Round 7 checklist | Low | Abstract 241 words, 100-word summary, CSE references, line numbers, double spacing, alt text, tables at end, figures as vector PDF | Fixed |
| 11 | Citations | 47 references, all DOI- or page-verified; 0 audit errors | Low | Citation audit | Fixed |
| 12 | Journal scope | GENETICS publishes genomic-prediction statistics (2025–26 examples) | Low | Scope verified | n/a |
| 13 | Journal-specific reviewer risk: animal-breeding reviewers want large-*n* or national-evaluation scale; statistical reviewers want theory | Rounds 6 and 10 | Moderate | Scale limitation and approximate-reliability pointer; guarantee discussion | Partly |
| 14 | Publication integrity / compliance | AI-use disclosure required by GSA | Low | Disclosed in Acknowledgments. Author names, affiliations, funding and ORCID are placeholders that the human authors must complete. All results are machine-generated and traceable. | Requires author action |
| 15 | Acceptance timeline | Median 69 days (our PubMed-based estimate for 2025-H1 submissions); about 45% of accepted papers took more than 72 days | n/a | Not controllable | n/a |

## Self-decision (Phase 42)

**READY FOR SUBMISSION**, subject to author actions that cannot be automated:
1. Insert author names, affiliations, ORCID, corresponding-author details, funding and acknowledgments.
2. Deposit `code/` and `results/jobs/*` (including the record files) on Zenodo, then insert the DOI in the Data availability section and the README.
3. Decide on preprint posting and update the cover letter accordingly.
4. Optionally add suggested reviewers.

Rationale:
* Every pre-specified experiment, together with the robustness experiments requested by the ten review rounds, has been run.
* All claims are mapped to machine-generated evidence (`final_audit.md`).
* Negative and narrowing results are reported.
* The package reproduces from a clean clone.

No further experiment would change the main conclusions with the data available. Remaining weaknesses are either inherent (novelty level, lack of temporal data) or disclosed.
