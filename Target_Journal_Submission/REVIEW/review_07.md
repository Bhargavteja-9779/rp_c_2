# Review round 7 — Reviewer #7 (scientific writing, logic, terminology, notation, figures and tables, guideline compliance)

These points are new relative to Reviewers #1–6. The full built manuscript (Markdown, DOCX and PDF) and all 12 figures were read.

## Issues

| # | Severity | Location | Problem | Fix |
|---|---|---|---|---|
| W1 | MAJOR | Methods, "Software…" | The text said "five deviations, all made for compute reasons or found in a smoke test". After rounds 2–6 there are seven, and two were motivated by results. As written, the sentence was untrue. | Rewritten to list all seven and to state which were added after the results were seen. |
| W2 | MODERATE | Article summary | "as little as 0.838" cited CV+, but SCP was lower (0.828). | Now gives the range "0.828–0.838" from tokens. |
| W3 | MODERATE | Abstract | "Kinship-aware intervals covered 0.894" did not name the regime. | "under cluster-out validation" added. The abstract is 241 words (limit 250), has no abbreviations or citations, and names all ten organisms. |
| W4 | MODERATE | Eq. 1 | Eq. 1 uses *S* for the training set while the rest of the text uses *T*. | *S* is defined as *T* or an inner subset of *T*. |
| W5 | MODERATE | CV+ definition | *ŷ*ⱼ^{(−k(i))} and *R*ᵢ were not defined. | Definitions added. |
| W6 | MINOR | Keywords | "genomic prediction" and "Genomic Prediction" were duplicates. | Duplicate removed. |
| W7 | MODERATE | Figure 12 | The three x-axis labels overlapped and the asterisks sat on the axes. | Replaced with one shared axis label and asterisks annotated at the end of each confidence interval. |
| W8 | MODERATE | Table 2 in the PDF | The column header "\|Cov−0.90\|" contained pipe characters and broke the Markdown table. | Renamed "Abs. cov. deviation" in all tables. |
| W9 | MINOR | Figure 2 | The legend overlapped the soybean boxes, and grid lines crossed the bars. | Legend moved below the panel; y-grid removed. |
| W10 | MINOR | Figure 1 | The left boxes were clipped, and the math text in the last box did not render because the text was wrapped. | Margins fixed; math rendered. |
| W11 | MINOR | Terminology | "random CV", "R1" and "random cross-validation" were all used. | The R-labels are defined once in Methods and used consistently after that. "Cluster-out" and "R2" are used together at first mention in each section. |
| W12 | MINOR | Guideline: alt text | GENETICS requires alt text for every figure. | All 12 legends carry an "Alt text:" line. The Figure 3 alt text was re-checked against the final numbers: it gives approximate ranges (0.93 → 0.88 under R1; 0.81–0.84 under R2) that match Table 2 and the quintile coverages. |
| W13 | MINOR | Guideline: tables | Tables must be editable and placed after the main text. | They are built as Word tables from the CSV files and placed after the Data availability, Funding and References sections. |

## Compliance checklist (GENETICS author guidelines)
| Item | Status |
|---|---|
| Title, running title, keywords | ✓ |
| Abstract of 250 words or fewer, without citations or abbreviations, naming the organisms | ✓ (241 words) |
| 100-word article summary | ✓ (100 words) |
| Section order: Introduction, Materials and Methods, Results, Discussion, Data availability, Acknowledgments, Funding, Conflicts of interest, Literature cited | ✓ |
| CSE name-year references, with every reference verified | ✓ (47 references; citation audit shows nothing missing or uncited) |
| Line numbers and double spacing in the DOCX | ✓ (w:lnNumType; line spacing 2.0) |
| Figures as separate files (vector PDF) | ✓ (`figures/*.pdf`; 600-dpi PNG versions are embedded in the review DOCX only) |
| Alt text for every figure | ✓ |
| Editable tables at the end of the text | ✓ |
| Data and code availability statement; disclosure of AI use | ✓ |
| Supplementary files of 2 MB or less each and 10 MB or less in total | Checked at packaging (Phase 40) |
