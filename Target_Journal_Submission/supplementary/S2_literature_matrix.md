# Literature matrix (Phase 3)

Every entry was verified against Crossref, PubMed, arXiv or the publisher page (see `citations/verified_refs.json`).
"—" means the item does not apply.

| Paper | Year / venue | Problem | Data (size) | Method | Validation | Uncertainty output | Limitation relevant here | Code/data |
|---|---|---|---|---|---|---|---|---|
| Meuwissen, Hayes & Goddard | 2001 GENETICS | Genome-wide prediction of genetic value | Simulation | BLUP / BayesA / BayesB | Simulated true breeding values | — | Point prediction only | — |
| VanRaden | 2008 J Dairy Sci | GRM construction, genomic prediction | US Holstein | GBLUP (GRM) | Reliability of predictions | Reliability / PEV (model-based) | Assumes a correct Gaussian model | — |
| Habier, Fernando & Dekkers | 2007 GENETICS | Contribution of relationships to GEBV accuracy | Simulation | RR-BLUP, BayesB | Accuracy across generations | — | Accuracy, not calibrated intervals | — |
| Clark et al. | 2012 Genet Sel Evol | Value of relatives in the reference set | Simulated and real sheep (1,750 reference) | gBLUP vs. pedigree BLUP | Accuracy by relationship group | — | Accuracy decreases with relatedness; no intervals | — |
| Pszczola et al. | 2012 J Dairy Sci | Reliability vs. relationship to reference population | Simulated dairy | Selection-index reliability | Deterministic reliabilities | Model-based reliability | Simulation-only; model-based | — |
| Wientjes, Veerkamp & Calus | 2013 GENETICS | Linkage disequilibrium vs. family relationships in reliability | Simulation (529 reference) | Genomic relationships, Me formula | Deterministic vs. empirical reliability | Reliability | Family relationships dominate reliability; no calibration of intervals | — |
| Legarra & Reverter | 2018 Genet Sel Evol | Population accuracy and bias from partial vs. whole data (LR method) | Brahman cattle (2,111) | Method LR | Repeated partitioning | Population-level accuracy and dispersion | Population-level, not individual intervals | — |
| Werner et al. | 2020 Front Plant Sci | Population structure inflates CV accuracy | *Brassica napus* hybrids (940, 46 families) | GBLUP | Random vs. within-family CV | — | Accuracy only; no intervals | — |
| Gibbs, Paril & Fournier-Level | 2025 GENETICS | Model choice vs. architecture and structure | *A. thaliana* (1,000+ accessions, 36 traits) | Penalised regression, RF, MLP | CV | — | No uncertainty quantification | — |
| Quesada-Traver et al. (EasyGeSe) | 2025 BMC Genomics | Benchmark resource | 10 species | 10 models | 5 × 5-fold CV | — | Pearson r / RMSE only; random CV only | Zenodo, CC-BY |
| Ahlinder & Waldmann | 2026 GENETICS | Uncertainty-aware optimum contribution selection | QTL-MAS 2010 (3,226), Norway spruce (5,525), loblolly pine (926) | MCMC posterior + CVaR | Simulation with oracle; real data | Bayesian posterior | Uses posterior uncertainty without checking calibration | — |
| Ding et al. | 2023 Nature | PGS accuracy vs. genetic ancestry continuum | UK Biobank, ATLAS | Individual-level genetic distance | Accuracy along genetic distance | — | Human; accuracy, not intervals | — |
| Hou et al. (CalPred) | 2024 Nat Genet | Context-specific calibrated PGS intervals | All of Us, UK Biobank (72 traits) | Heteroscedastic model of contexts | Coverage across contexts | Prediction intervals (parametric) | Human, largely unrelated individuals; parametric; no finite-sample guarantee | yes |
| Xu, Ganesh & Zhou (PredInterval) | 2025 Nat Genet | Calibrated PGS intervals | 17 traits | Quantiles of CV residuals | Coverage | Nonparametric intervals (marginal) | Marginal calibration; no relatedness conditioning | yes |
| Kumar (CalGS), preprint / code archive | 2025–26 Zenodo | Split-conformal intervals for deep GS | Simulated sesame-like panel (430) | Split CP around GBLUP/MLP/CNN/transformer | Coverage on simulated data | Marginal split-CP intervals | Simulated data only; marginal coverage; no relatedness shift | GitHub/Zenodo |
| Vovk, Gammerman & Shafer | 2022 (2nd edn) Springer | Conformal prediction theory | — | (Inductive) conformal prediction | Theory | Valid sets/intervals | Exchangeability assumed | — |
| Lei et al. | 2018 JASA | Distribution-free predictive inference | — | Split CP, locally weighted CP | Theory and simulation | Intervals | Exchangeability | — |
| Barber et al. (jackknife+ / CV+) | 2021 Ann Stat | Cross-conformal intervals | — | Jackknife+, CV+ | Theory | Intervals (≥1−2α) | Exchangeability | — |
| Tibshirani et al. | 2019 NeurIPS | Covariate-shift conformal | — | Likelihood-ratio weighted CP | Theory and experiments | Intervals | Needs the shift density ratio | — |
| Barber et al. | 2023 Ann Stat | CP beyond exchangeability | — | Weighted, nonsymmetric CP | Theory | Intervals with coverage-gap bound | General; not genetics-specific | — |
| Guan | 2023 Biometrika | Localized conformal prediction | — | Kernel-localised CP | Theory | Approximately conditional intervals | General | — |
| Gibbs, Cherian & Candès | 2025 JRSSB | Conditional guarantees | — | Conformal with function-class conditional coverage | Theory | Intervals | General | — |
| Dunn, Wasserman & Ramdas | 2023 JASA | Two-layer hierarchical models | — | Group-level CP | Theory | Intervals | Hierarchical groups, not continuous kinship | — |
| Bhattacharyya & Barber | 2026 Electron J Stat | Group-weighted CP | — | Group-weighted CP under subpopulation shift | Theory | Intervals | Discrete groups | — |
| Jin & Candès | 2023 JMLR | Selection with conformal p-values | — | Conformal selection | Theory | FDR-controlled selection | Selection, not intervals | — |

## Gaps (what exists → what is missing → why it matters → what we add → how it is verified)

1. **Methodological gap.**
   * *Exists:* in breeding, model-based PEV intervals (VanRaden, Henderson) and marginal split CP (CalGS).
   * *Missing:* distribution-free intervals whose calibration is maintained across levels of relatedness to the training set.
   * *Why it matters:* coverage that is nominal on average can hide over-coverage for close relatives and under-coverage for distant candidates. Distant candidates are exactly where breeders need honest uncertainty.
   * *Adds:* KinCP.
   * *Verified by:* E1–E3, using quintile-conditional coverage.
2. **Experimental gap.** Uncertainty intervals for genomic prediction have not been benchmarked across many species, or under cluster-out deployment. EasyGeSe reports point accuracy only. We add 10 species × 3 regimes (E1, E4, E5).
3. **Robustness and generalisation gap.** There is no evidence on whether calibration transfers across base predictors (kernel, tree ensembles) for which no PEV exists. Tested in E5.
4. **Statistical-validation gap.** CalGS uses simulated data only, and the human-PGS work deals with unrelated individuals. We add pre-specified paired tests across 24 dataset × trait units.
5. **Reproducibility gap.** We provide an end-to-end pipeline that regenerates every number from the public data.
