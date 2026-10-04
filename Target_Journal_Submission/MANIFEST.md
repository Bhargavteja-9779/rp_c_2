# Submission package — GENETICS (OUP / Genetics Society of America)

**Manuscript:** *Relatedness-aware calibration of genomic prediction intervals: kinship-aware conformal prediction across ten plant and animal species*

**Status:** READY FOR SUBMISSION after the author actions listed in `REVIEW/rejection_risk_report.md`: author details, Zenodo DOI, preprint decision.

```
Target_Journal_Submission/
├── MANIFEST.md                        this file
├── journal_selection/
│   ├── selected_journal.md            target journal, JCR/JIF/quartile, measured acceptance time, guidelines, risks
│   ├── journal_comparison.md          27 candidates screened against the ≤72-day and Q1 constraints
│   ├── journal_verification.md        verification log (legitimacy, JIF, timeline method)
│   └── evidence/                      PubMed/Crossref timeline scripts + outputs (*.jsonl)
├── manuscript/
│   ├── Final_Manuscript.docx          GENETICS-formatted master (double spacing, line numbers, tables at end, figure legends with alt text)
│   ├── Final_Manuscript.pdf           review copy (headless Chromium render)
│   ├── Final_Manuscript.md            built text (all numbers filled from results/key_numbers.json)
│   ├── cover_letter.docx / .md
│   └── src/                           text sources with {{tokens}}, tables.json, figures.json, references
├── code/
│   ├── src/kincp/                     package: data, preprocessing, models, conformal, training, evaluation, statistics
│   ├── experiments/run_experiments.py 535 jobs (quick/full), resumable
│   ├── scripts/                       prepare_data, aggregate, secondary_analyses, make_figures, make_tables,
│   │                                  key_numbers, build_references, build_manuscript, build_pdf,
│   │                                  package_supplement, benchmark_scaling
│   ├── tests/test_core.py             12 unit tests
│   ├── config/study.yaml              seeds, α, inner folds, KinCP bandwidth/floor, LightGBM, simulation, clusters
│   ├── run_all.py                     python run_all.py --mode quick | full
│   ├── requirements.txt, environment.yml
│   └── README.md                      install, data, reproduction, code map
├── results/
│   ├── raw_results.csv                every job × method × α summary (all metrics)
│   ├── metrics.json                   medians per base/regime/method
│   ├── statistics.json, statistics_table.csv, statistics_species.csv
│   ├── alt_relatedness_*.csv/json, oracle_inflation_*.csv, pev_calibration*.csv/json
│   ├── decision_*.csv/json, error_analysis*.csv/json, scaling.csv, timings.csv
│   ├── key_numbers.json               the 1,695 numbers used in the manuscript text
│   ├── data_audit.json, data_md5_verification.json
│   ├── jobs/                          per-job summaries and timings (records parquet: Zenodo)
│   └── experiment_logs/               run logs, environment.json
├── figures/                           Fig1–Fig12 (.pdf vector for submission; .png 600 dpi)
├── tables/                            Table1–Table9 + supplementary tables (.csv, .md)
├── supplementary/
│   ├── File_S1_design_and_deviations.pdf (0.1 MB)   pre-specified design (committed before experiments) + deviations D1–D7
│   ├── File_S2_supplementary_tables.xlsx (0.8 MB)    15 machine-generated supplementary tables
│   ├── File_S3_code.zip (≈0.1 MB)                    code archive (also to Zenodo)
│   ├── supplement_size_check.json                    all files ≤ 2 MB, total ≤ 10 MB
│   ├── S0_preregistered_design.md, S9_deviations.md
│   ├── S1_topic_selection.md, S2_literature_matrix.md, S3_novelty_map.md
│   └── citations/                     verified_refs.json, manual_refs.json, citation_audit.json, scripts
└── REVIEW/
    ├── review_01.md … review_10.md    ten independent adversarial review rounds with author responses
    ├── final_audit.md                 claim→evidence map, citation audit, consistency and reproducibility audits
    └── rejection_risk_report.md       remaining risks and the final self-decision
```

**Not included (size):**
* Raw EasyGeSe data (about 2.5 GB). Downloaded and MD5-verified by `prepare_data.py`.
* Genotype caches.
* Per-individual record files (326 MB), to be deposited on Zenodo.
