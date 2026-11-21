# Reproducibility

## Scope

`Model.ipynb` contains the three-model research workflow in nine sections.
`Model.py` contains the same Python code. Notebook execution outputs are cleared.
The repository includes code and documentation; scientific inputs and trained
artifacts must be obtained or generated separately.

## Required local inputs

- Audited TCGA RNA/DNA tables, source expression matrices, fixed patient splits,
  and model-specific feature specifications.
- CPTAC expression, genomic labels, and patient/sample mappings.
- GBM UMI matrices, annotations, DNA labels, and all-gene UMI denominators.
- GSE327167 matrices, cell annotations, supplementary sample-to-patient mapping,
  and an independently verified local OGM reference table.
- Trusted source utilities, network definitions, model checkpoints, and manifests
  required by the corresponding analysis stages.

Paths are relative to `MTAP_PROJECT_ROOT`. Expected fields are checked by the
notebook. See [GSE327167 inputs](docs/GSE327167_INPUTS.md) for its local preparation.
Do not infer missing genomic outcomes from RNA predictions or aggregate class counts.

## Execution

By default, the notebook registers analysis stages and summarizes cached predictions.
Set `MTAP_RUN_WORKFLOW=1` before launching Jupyter to execute the research workflow
in its declared dependency order. Required local inputs must be available.

The analysis branches use different cohorts, expression units, feature sets, and
artifacts. Use the preprocessing and checkpoint specified for each branch.
TCGA development performance uses out-of-fold predictions; the original holdout
has been examined during research and is not a prospective validation cohort.
The original-holdout bootstrap stage uses 1,000 resamples.

The 0.75 deployment threshold was selected in the GBM transfer setting.
Comparisons at 0.50 and 0.80 are sensitivity analyses. GSE327167 evaluations at
0.50 and 0.75 are retained without selecting a new threshold from that cohort.

## GSE327167 evaluation

The evaluated reference comprises 31 patients, with four OGM-detected MTAP deep
deletions and 27 with no OGM-detected MTAP deep deletion. Absence of a reported OGM
event does not establish copy neutrality. Whole-tissue evaluation uses 31 patients;
malignant-cell evaluation follows its recorded cell-count eligibility criteria.

Sample mapping checks supplementary library and sample-set identifiers before
patient-level aggregation. Three core L2 features must be observed. Missing noncore
features, including SCARNA8, use GBM training medians for Elastic Net and checkpoint
training means for DL. External cohort labels are not used for model fitting.

## Validation status

Checks cover Python syntax, notebook/script consistency, stage ordering, cleared
outputs, public-source privacy, local reference export, and default-mode execution.
The GSE327167 input stage was tested with 93,351 synthetic cells and a minimal torch
import stub. That test did not perform model inference.

The complete scientific pipeline has not been executed in the preparation environment.
Syntax and synthetic checks do not establish numerical reproduction of research
results. The pinned core dependencies describe the preparation/test environment,
not a validated environment lock for the full workflow. See `validation_report.json`.

Before a manuscript release, record exact input provenance, source revisions,
checkpoint checksums, and a tested package/CUDA environment; verify final analyses
from a fresh kernel and archive the publication version. Select a code license
before adding a license badge. Patient-level outputs must remain outside Git.
