# Review round 10 — Final adversarial review (independent; goal: find one fatal reason to reject)

The reviewer re-read the built manuscript (all sections), the job list, `S9_deviations.md` and the code paths for the primary endpoint, without relying on reviews 1–9.

## Search for a fatal flaw
| Candidate fatal flaw | Investigation | Verdict |
|---|---|---|
| Test-set information used to tune KinCP | The bandwidth (*h* = 0.5 SD) was fixed before any run. The mass floor (*n*_min = 50, D1) was introduced after a smoke test on one oyster trait, which looked at test-fold coverage. **This is a small amount of data snooping.** Mitigations: the floor depends only on genotype covariates; the variants *n*_min = 25 and 100 and no floor all gave the same R2 conditional error as the default (0.036); without the floor, 0.002 of R2 intervals were infinite (Table 8). The snooped unit is 1 of 24. | Not fatal. It is disclosed (D1), and the sensitivity analysis shows no dependence on the choice. |
| Leakage through the GRM or clusters | GRM, PCs and clusters use genotypes only, which is legitimate at deployment. Phenotype scaling, REML and pools use training data only (code verified in Round 4). BLUE preprocessing upstream is disclosed. | Not fatal |
| Primary endpoint constructed to favour the method | Shown in Round 3: the R1 advantage is endpoint-specific, while the R2 advantage is robust to the relatedness measure. Disclosed. | Not fatal |
| Overclaiming relative to simpler fixes | Rounds 8–9: the claims are now bounded (group CV+, CalPred on pool A, oracle rescaling). | Not fatal |
| Numbers not traceable | All numbers are tokens filled from `results/key_numbers.json`, and the build aborts on any unresolved token. The final audit re-checks them against the result files. | Not fatal |

**Conclusion: no fatal flaw found.**

## Major weaknesses (remaining after all fixes; real ones only)
1. **Methodological novelty is modest.** The building blocks are known, and the contribution is design plus evidence. *Unfixable by experiment; mitigated by framing.*
2. **R2 advantage is mainly the overall level.** Under cluster-out deployment, KinCP's advantage over relatedness-blind methods is mainly setting the correct overall level (oracle analysis), and group CV+ matches it when the regime is known. *Disclosed.*
3. **Residual under-coverage.** KinCP under-covers the least-related quintile under R2 (0.839), and the exploratory fixes failed. *Disclosed.*
4. **Validity is the only benefit.** There is no improvement in interval score. *Disclosed.*
5. **Limited external validation.** Real-family validation covers only oyster; there is no temporal or large-population validation. *Disclosed.*

(Five real major weaknesses. Nothing was invented to reach a quota of ten.)

## Moderate weaknesses
1. Wording "*P*-values were = 0.983" was awkward. → Fixed.
2. Contended per-fold timings were reported next to the benchmark. → They are now explicitly labelled as from contended runs, and absolute times are taken from the benchmark.
3. A scaling exponent of 2.0 sat next to an *O*(*n*³) claim and looked contradictory. → Explained (asymptotics).
4. The Discussion's first bullet generalised the R1 under-coverage of distant candidates, which holds only along *d*. → Qualified.
5. "Mostly for traits with high within-cluster heritability" rested on an exploratory, unadjusted correlation. → Softened.
6. The interval-score passage was embedded in another paragraph. → Separated.
7. The Results section is long (13 sub-analyses). Acceptable for a GENETICS Investigation. Moving robustness analyses to the supplement was considered and rejected, because they carry the bounded claims.
8. Species-level tests are under-powered (10 units). Disclosed.

## Minor weaknesses
* Author, affiliation, funding and ORCID placeholders remain (by design; the authors must complete them).
* The supplementary-file references (File S1–S3) must match the actual package (checked in the Phase 40 manifest).
* Some table captions refer to "units". "Unit" is defined in the statistics section as a dataset × trait combination.

## Final verdict of this reviewer
**Major revision expected, not rejection.** The study is careful and honest. Its claims are now commensurate with the evidence, and the remaining weaknesses are disclosed rather than hidden.
