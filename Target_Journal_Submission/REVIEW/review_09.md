# Review round 9 — Associate Editor, GENETICS (Systems & Computational Genetics)

*Not acting as author.* Evaluation of the revised manuscript together with reviews 1–8 and the authors' responses.

## Assessment by criterion

| Criterion | Assessment |
|---|---|
| Scope | Statistical methodology for genomic prediction, grounded in quantitative-genetic theory (PEV, reliability, relatedness) and applied across plant and animal species. This is in scope for the Systems & Computational Genetics area, and similar papers appeared in GENETICS in 2025–26. ✓ |
| Novelty | Moderate. The conformal machinery is established, and the authors now say so plainly. The new elements are the identification and measurement of relatedness as the axis of miscalibration, the calibration-pool design, and a pre-specified 10-species evaluation. Rival constructions (group CV+, a parametric calibration on the same pool) are shown to match KinCP within a single known regime. The paper is honest about this, which strengthens it. |
| Technical quality | High. The design was pre-specified with logged deviations. The study includes unit tests, MD5-verified data, ablations, alternative endpoints, species-level tests, a simulation with a known-truth diagnostic, scaling, and competitor analyses. |
| Evidence and claims | After rounds 3, 7 and 8 the claims are bounded: calibration rather than interval score; a small R1 advantage that is specific to *d*; under R2, mainly the level of the intervals. No overclaiming remains in the abstract (checked). |
| Completeness | The research questions are answered. Temporal shift is not available in the data and is stated as a limitation. |
| Reproducibility | One command; resumable; tokenised numbers. Phase 35 will check this from a clean checkout. |
| Clarity | Long Results section, but logically ordered by research question. Acceptable for an Investigation (no length limit). |
| Guidelines | The Round 7 checklist is complete. Supplementary files S1–S3 still need to be assembled and their sizes checked. |

## Remaining concerns (author action required)
1. **Title.** It foregrounded the method, whereas the main message is that calibration must be relatedness-aware. → Retitled "Relatedness-aware calibration of genomic prediction intervals: kinship-aware conformal prediction across ten plant and animal species". ✓
2. **Methods completeness.** The oracle-rescaling and group-CV+ analyses (Round 8) were in Results but not in Methods. → New Methods subsection "Robustness analyses requested by internal review". ✓
3. **Conclusions.** These must mention that simpler fixes suffice within a known regime. → Done. ✓
4. **Cover letter.** Its findings must match the narrowed claims. → Finding 3 revised; title updated. ✓
5. **Supplementary files.** Assemble File S1 (pre-specified design and deviations), File S2 (supplementary tables, including per-unit results) and File S3 (code), each within the size limits (≤ 2 MB per file, ≤ 10 MB in total; the code archive should go to Zenodo). → To be done at packaging (Phase 40).
6. **Author placeholders.** Names, affiliations, funding and ORCID are placeholders, to be completed by the human authors before submission. This must be listed in the final report.

## Would it survive peer review at GENETICS?
Likely to receive **major or minor revision** rather than rejection. The most probable reviewer objection is a perceived lack of methodological novelty ("weighted conformal plus group CV"). The authors' framing, honest comparisons and the breadth of the evaluation are the best defence available. A reviewer from animal breeding may also ask for a large-population demonstration, which the data do not allow.

**Recommendation:** proceed to final adversarial review (Round 10) after the fixes above.
