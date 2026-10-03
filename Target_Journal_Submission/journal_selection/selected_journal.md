# Selected target journal

| Field | Value (with source / verification status) |
|---|---|
| **TARGET JOURNAL** | **GENETICS** (official journal of the Genetics Society of America) |
| **PUBLISHER** | Oxford University Press on behalf of the Genetics Society of America (GSA) |
| **ISSN** | 0016-6731 (print); 1943-2631 (online) |
| **JCR STATUS** | Indexed in Clarivate Journal Citation Reports (Science Citation Index Expanded) |
| **JOURNAL IMPACT FACTOR** | **6.5** (2025 JIF, JCR 2026 release), as displayed on the publisher journal page, academic.oup.com/genetics, accessed 2026-10-03 |
| **JCR SUBJECT CATEGORY / RANK** | Genetics & Heredity; rank **19/192** (publisher page, same access date) |
| **JCR QUARTILE** | **Q1** (19/192 = 9.9th percentile from the top, inside the first quartile) |
| **VERIFIED REVIEW/DECISION TIMELINE** | Not published by the journal as an official statistic. **Not independently verified.** |
| **VERIFIED ACCEPTANCE TIMELINE (submission→acceptance)** | **Empirical median 69 days** (IQR 41–112). Computed from PubMed `received`/`accepted` history dates for every GENETICS journal article received 1 Jan–30 Jun 2025 that had been published by Oct 2026 (n = 137). 54.7% of these were accepted in ≤72 days and 40.9% in ≤60 days. Script: `evidence/cohort.py`; output: `evidence/cohort_received_2025H1.jsonl`. This is a **submission-to-acceptance** figure. It is not a first-decision figure. It covers accepted papers only, so rejected submissions are not included. |
| **APC** | Open access: US$4,124 (GSA members) / US$4,795 (non-members). Standard licence: page charges of US$90/page (members) or US$125/page (non-members). Waivers are considered case by case. Source: GENETICS author guidelines. |
| **SCOPE FIT** | The scope lists "Systems & Computational Genetics – functional genomics, machine learning, mathematical analysis, and statistical methods" as one of five main subject areas. GENETICS regularly publishes genomic-prediction methodology. Examples from 2024–2026: Gibbs et al. 2025 (iyaf003), Ahlinder & Waldmann 2026 (iyag205), Hu et al. 2025 MegaLMM (iyae171), Liu et al. 2026 (iyag114), Lee et al. 2026 (iyag074), Fu et al. 2026 (iyaf245). |
| **RESEARCH FIT** | Statistical methodology for the uncertainty of genomic predictions, tied to quantitative-genetic theory (genomic relationships, prediction error variance) and evaluated across 10 plant and animal species. This matches the journal's statistical-genetics / genomic-prediction profile. |
| **KEY AUTHOR GUIDELINES** | Article type "Investigation" (no length limit). Abstract ≤250 words, with no citations or abbreviations, and naming the organisms studied. Section order: Title page (with keywords), Abstract, Introduction, Materials and Methods, Results and Discussion, Data Availability, Acknowledgments, Funding, Conflict of Interest, References. Also required: a 100-word "Article summary". References use CSE name-year style. Tables go at the end of the main text, in editable form. Each figure is a separate file (vector PDF or ≥600 dpi line art); .doc/.docx/.jpg figures are not accepted. Every figure needs alt text under its legend. All data and code must be publicly released (a DOI-issuing repository such as Zenodo or figshare is encouraged). Supplementary files must be ≤2 MB each and ≤10 MB in total. Use of AI tools must be disclosed. Review is single-anonymized. Any format is accepted at initial submission (a single PDF under 15 MB is fine). |
| **KEY REJECTION RISKS** | (1) Editors may see the work as "applying conformal prediction" with too little genetic insight. Mitigation: link to GBLUP prediction error variance and reliability theory, plus a simulation on real genotypes with known genetic values. (2) Reviewers from animal breeding may expect to see the LR method and classical reliability compared. (3) The coverage target is the phenotype, not the true breeding value. This must be stated clearly and also addressed by simulation. (4) Supplementary size limits. |

## Requirements that could not be satisfied or verified
* The ≤72-day requirement holds for the **median** accepted GENETICS paper (69 days). Roughly 45% of accepted papers took longer. No reputable journal can guarantee an acceptance time for an individual manuscript.
* GENETICS publishes no official "submission-to-acceptance" statistic. The figure above is our own computation from public PubMed history dates.
* The JIF and rank come from the publisher's display of Clarivate data. We could not query JCR directly because it needs a subscription.
