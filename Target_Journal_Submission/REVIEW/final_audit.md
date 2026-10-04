# Final audit (Phases 22, 23, 34, 35)

## 1. Claim → evidence map (Phase 22)

All numbers below are inserted into the manuscript from `results/key_numbers.json` (token names in brackets). The build aborts if any token is unresolved.

| # | Claim (manuscript) | Evidence | Experiment | Table / Figure | Status |
|---|---|---|---|---|---|
| C1 | Relatedness-blind conformal intervals over-cover close relatives and under-cover distant ones (along *d*) under R1 | Quintile coverage, SCP 0.921 → 0.880 and CV+ 0.931 → 0.881 (`scp_R1_q1/q5`, `cvp_R1_q1/q5`) | E1/E2 | Fig 3, Table 2 | Supported. Qualified: on the maxkin measure, only the over-coverage of close relatives holds (Round 3). |
| C2 | Under cluster-out deployment, SCP/CV+ marginal coverage falls to 0.828/0.838 | `scp_R2_cov`, `cvp_R2_cov`; 11/24 units below 0.85 | E1/E2 | Fig 3–4, Table 2 | Supported |
| C3 | Gauss-PEV is calibrated under R1 but under-covers under R2 (0.881) | `pev_R1_cond`, `pev_R2_cov` | E2 | Table 2 | Supported |
| C4 | KinCP has the lowest conditional error among the 8 methods with GBLUP in every regime | Table 2 means (0.017 / 0.036 / 0.014). CalPred-style on pool A is 0.0365 under R2 (KinCP 0.0362). | E1 | Table 2 | Supported for GBLUP. Elsewhere worded "smallest or joint-smallest" (RKHS R2: CalPred-style 0.0376 *vs.* 0.0377). |
| C5 | KinCP better than CV+, SCP, Gauss-PEV, NormCP and CalPred(random) on the primary endpoint under R2 | Holm *P* 0.003 / 0.002 / 0.004 / 0.033 / 0.003 | E2 + statistics | Table 3, Fig 12 | Supported |
| C6 | KinCP not different from CalPred-style on pool A | *P* = 0.900 | E2 | Table 3 | Supported (negative result reported) |
| C7 | Pool A is the decisive component | Without A, R2 error 0.053 *vs.* 0.036 | E3 | Table 4, Fig 5 | Supported |
| C8 | No improvement in interval score over CV+, Gauss-PEV or CalPred-style | *P* 0.983 / 1.000 / 1.000 | E2 | Results text; File S2 | Supported (negative result reported) |
| C9 | The R2 advantage holds on an independent relatedness measure; the R1 advantage does not | maxkin: R2 *P* < 0.001 against PEV and CV+; R1 all *P* ≥ 0.15 | Round 3 analysis | File S2 sheet S5 | Supported |
| C10 | Holds for RKHS and LightGBM | R2 coverage 0.891 / 0.895; *P* 0.004 / 0.007 against CV+ | E5 | Table 5, Fig 6 | Supported |
| C11 | Simulation: KinCP matches the correctly specified Gauss-PEV; *d* is calibrated for genetic values | Coverage 0.901 *vs.* 0.900; MSE/PEV ratio 0.95–1.04 | E5b + Round 1 diagnostic | Table 6, Fig 7, S2 sheet S9 | Supported |
| C12 | Robust to cluster granularity and to real families | *k* = 3: 0.906 *vs.* 0.822; *k* = 10: 0.891 *vs.* 0.859; oyster families 0.923 *vs.* 0.865 | Round 5 | S2 sheet S15 | Supported. Family validation covers 1 species (disclosed). |
| C13 | Under R2 the gain is mainly the overall level; group CV+ is comparable under R2 but conservative under R1 | Oracle factors 1.19 (CV+) *vs.* 1.02 (KinCP); group CV+ R2 *P* = 0.218, R1 *P* < 0.001 | Round 8 | Results text; S2 sheets S6 and S15 | Supported (narrowed claim) |
| C14 | Cost is about two CVs; benchmark 10.0 s fit, 7.3 s pools, 303 MB at *n* = 3,500 | `results/scaling.csv` | E6 + Round 6 | Table 7, Fig 8 | Supported |
| C15 | Insensitive to *h* and *n*_min | R2 conditional error 0.036–0.040 | E7 | Table 8, Fig 9 | Supported |
| C16 | Ranking by lower bound does not increase gain (slightly reduces it under R1) | −0.011 SD, *P* = 0.005 | E9 | Table 9, Fig 11 | Supported |
| C17 | Exploratory fixes (KinCP-G, Mondrian-d) do not close the remaining gap | 0.038 / 0.040 *vs.* 0.037 | D6 | Results text; S2 sheet S15 | Supported (negative result) |
| C18 | The design was pre-specified before any model fit | Git commit `bb7247f` ("pre-specified research design (before any experiments)") precedes all code commits | — | File S1 | Supported. Deviations D1–D7 are logged. |

**Claims removed or weakened during review:**
* "KinCP had the lowest error in every scenario" (removed; Round 9 check of RKHS).
* "Interval score was lower" (corrected; Round 8 pre-check).
* "Mostly for traits with high within-cluster heritability" (softened to exploratory; Round 10).
* "Five deviations" (corrected to seven; Round 7).
* "Standard intervals covered as little as 0.838" (corrected to 0.828–0.838; Round 7).

## 2. Citation audit (Phase 23)
* 47 references, each verified against Crossref by DOI (`supplementary/citations/verified_refs.json`) or, for NeurIPS, JMLR, JSTOR and Zenodo items without a Crossref DOI, against the publisher, arXiv or Zenodo page (`manual_refs.json`).
* Automated audit (`citation_audit.json`): 0 references missing from the text, 0 unverified, 0 uncited name-year strings.
* Errors found and fixed:
  * Crossref bibliographic search had matched wrong records for Zhao 2011, PredInterval, Gneiting 2007, Holm 1979, LightGBM, Tibshirani 2019 and Jin 2023. All were replaced by DOI- or page-verified records.
  * The Misztal 2009 paper (single-step computing) did not support the "approximate reliability" statement and was replaced by Misztal *et al.* 2013 (*Methods to approximate reliabilities in single-step genomic evaluation*).
* Attribution check:
  * CalPred (contexts, parametric), PredInterval (CV residual quantiles) and CalGS (split CP, simulated data) are described as in their abstracts or repository.
  * Ahlinder and Waldmann (CVaR-OCS, MCMC posterior) are described as in their abstract.
  * Werner *et al.* (random CV inflates accuracy) are described as in their abstract.

## 3. Consistency cross-check (Phase 34)
* **Title ↔ abstract ↔ contributions:** relatedness-aware calibration is the main message, with KinCP as its implementation. Consistent after the Round 9 retitle.
* **Method ↔ code:** Eq. 1 ↔ `KernelBLUP.predict(return_d=True)` (unit-tested against an explicit inverse). Eq. 2 ↔ `weighted_quantiles` (unit-tested). Bandwidth, floor, pools, CV+ and CalPred-style were verified line by line in Round 4.
* **Experiments ↔ tables and figures:** every table and figure is generated by `make_tables.py` or `make_figures.py` from `results/*`. No manual entries.
* **Numbers:** 1,695 tokens. A full regeneration with `run_all.py --mode full --skip-download --skip-experiments` reproduced all 1,695 values with 0 differences.
* **Hard-coded numbers in the text:** only design constants (0.90 nominal, α = 0.05/0.20, the 0.95 duplicate threshold, MAF 0.01, *h*-grid values, the 0.85 reporting threshold).
* **Figures:** all 12 regenerated from data and inspected visually (Round 7 fixes for Figures 1, 2 and 12). Every figure has alt text.

## 4. Reproducibility audit (Phase 35, "stranger" test)
| Question | Result |
|---|---|
| Can I install it? | `pip install -r requirements.txt` (pinned versions). CPU only. |
| Can I obtain the data? | `prepare_data.py` downloads from Zenodo and verifies MD5 (30/30 files OK). |
| Can I run it from a clean clone? | **First attempt failed:** `.gitignore` rule `data/` excluded the source package `src/kincp/data/`. Fixed (anchored rules). **Second attempt failed:** quick-mode record-file naming broke the secondary analyses. Fixed (mode-agnostic lookup). **Third attempt:** `run_all.py --mode quick` completed in about 1 min from a fresh `git clone`, producing results, figures and tables. |
| Tests | `pytest -q`: 12 passed. |
| Can I regenerate the exact manuscript numbers? | From the committed per-job summaries plus the per-individual record files: yes, 0 differences. **Limitation:** the record files (326 MB) are not in git and must be obtained from the Zenodo deposit, or regenerated by the full run (about 8 h on 4 cores). This is documented in the README. |
| Determinism | Fixed seeds, k-means seed 2026, single-thread BLAS. Identical re-aggregation confirmed. |
