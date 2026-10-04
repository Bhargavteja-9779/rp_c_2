# Review round 5 — Reviewer #5 (dataset validity, generalisation, domain shift, external validity)

**Goal:** try to invalidate the central claim that relatedness-aware calibration restores coverage when candidates are weakly related to the training set. These points are new relative to Reviewers #1–4.

## Attacks attempted

**E1. "The R2 result is an artefact of *k* = 5."** (MAJOR)
* *Argument:* If deployment clusters are coarser than KinCP's inner clusters, the pool may not reach the relevant relatedness range. If they are finer, relatedness-blind methods might already be fine.
* *Test required:* other *k*, with KinCP's inner *k* held fixed.

**E2. "k-means clusters are not biology."** (MAJOR)
* *Argument:* Breeders deploy to new *families* or crosses, not to k-means clusters of principal components.
* *Test required:* at least one dataset with real pedigree groups.

**E3. "Duplicated germplasm drives the results."** (MODERATE)
* *Argument:* Barley has 2,600 near-identical pairs and soybean 192. Near-duplicates across folds could make random CV look well calibrated.
* *Test required:* compare against the dedup sensitivity analysis.

**E4. "Simulated additive traits are too easy."** (MODERATE)
* *Argument:* The simulation favours Gauss-PEV by construction, so it cannot validate KinCP.
* *Test required:* none. The authors already present it as a correctly specified reference; check that the text does not over-interpret it.

**E5. "No temporal or environmental shift."** (MAJOR, not fixable with these data)
* *Argument:* Real deployment is across breeding cycles and environments.
* *Test required:* none possible; EasyGeSe lacks cycle labels, and the maize data are BLUEs across environments. This must be a stated limitation.

**E6. "Phenotype coverage hides genetic-value miscalibration."** (Covered by Reviewer #1.) Not repeated.

## Outcomes of the tests (run in this round)

| Attack | Experiment | Result | Verdict |
|---|---|---|---|
| E1 | Cluster-out regime with *k* = 3 and *k* = 10 deployment clusters; GBLUP; all 24 units; KinCP inner folds kept at *k* = 5 | *k* = 3: coverage 0.906 (KinCP), 0.822 (CV+), 0.886 (Gauss-PEV). *k* = 10: 0.891, 0.859, 0.885. KinCP had a lower conditional error than CV+ in 17/24 units (*P* = 0.001) and 14/24 units (*P* = 0.009), and than Gauss-PEV at both *k* (*P* < 0.001). It did not differ from CalPred-style on pool A (*k* = 3: *P* = 0.966). | Claim survives |
| E2 | Leave-one-F2-family-out for eastern oyster: 4 real families, 5 seeds | Coverage 0.923 (KinCP), 0.930 (Gauss-PEV), 0.865 (CV+), 0.860 (SCP) | Claim survives (one species only, which is a limitation) |
| E3 | Dedup sensitivity, already run | R2 coverage 0.892 (KinCP) and 0.845 (CV+) without near-duplicates | Claim survives |
| E4 | Text check | The simulation paragraph states that Gauss-PEV is the correctly specified reference, and that KinCP approaches it while CV+ and SCP under-cover (R2: 0.882, 0.875). The PEV-calibration diagnostic (ratio 0.95–1.04) validates *d*. | No over-interpretation found |
| E5 | — | Added to Limitations; the existing sentence on temporal deployment was retained | Stated as a limitation |

## Remaining external-validity weaknesses (honest)
* Real-family validation covers one species (oyster). Pine has 61 families, but the family labels are not in the distributed files.
* With five clusters (or four families) per dataset, R2 coverage per unit is estimated from few deployment groups.
* All traits come from single public panels. Programme-scale, multi-cycle validation is outside this study's data.

---
# Author response and changes (Round 5)
* Added regimes `R2k3`, `R2k10` and `R2fam` (`kincp.training.runner._outer_folds`; job tags `granularity` and `families`), results in `results/raw_results.csv`, and a Results paragraph ("Granularity of the deployment clusters") with all numbers from `key_numbers.json`.
* Methods describe the added regimes and say they were added after internal review (deviation D7).
* Limitations: temporal/environmental shift and single-species family validation are stated.
