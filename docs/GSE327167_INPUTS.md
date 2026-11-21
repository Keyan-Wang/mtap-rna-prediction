# GSE327167 local input preparation

## Scope

Section 7 audits inputs and patient mappings before missing-feature-aware
inference. Do not upload a private reference notebook,
patient labels, sample mappings, matrices, or checkpoints to this repository.

## 1. Prepare the local OGM reference

Prepare a verified reference TSV from the study supplementary results and
author-provided mappings using the schema below. Keep patient-level inputs outside
Git. If your private analysis notebook already contains the audited literal
`OGM_PATIENTS` and `OGM_DEEP_DELETION_PATIENTS` definitions, the optional helper can
export that reference without executing the notebook. Replace both example paths:

```bash
python scripts/prepare_gse327167_reference.py \
  --notebook /path/to/private/reference_source.ipynb \
  --output-root /path/to/local/research/project
```

The helper parses literal definitions without executing notebook cells. It requires
31 unique patients and four OGM-detected deep deletions, rejects conflicting definitions,
and refuses to overwrite an existing reference. It does not calculate genomic labels
from RNA predictions. It writes a local TSV and a provenance JSON under `metadata/`.

The TSV has exactly these required columns:

| Column | Meaning |
| --- | --- |
| `patient_id` | Verified Case ID matching the supplementary mapping |
| `OGM_deep_deletion_label` | 1: OGM-detected MTAP deep deletion; 0: no OGM-detected MTAP deep deletion |

No patient rows are included in this guide. The evaluated reference already excludes
the case without usable stringent expression data. Do not substitute sample IDs for
Case IDs or infer labels from the aggregate class counts.

## 2. Retain the original local inputs

All paths are relative to `MTAP_PROJECT_ROOT`.

| Directory | Required files |
| --- | --- |
| `data_raw/MESO/GSE327167/` | `GSE327167_stringent_scRNA_counts_matrix.mtx.gz`, `GSE327167_stringent_scRNA_geneIDs.tsv.gz`, `GSE327167_stringent_scRNA_cellIDs.tsv.gz`, `GSE327167_PM_cell_metadata.tsv.gz`, `NIHMS2136244-supplement-4.xlsx` |
| `data_processed/MTAP_RNA_prediction/16_scRNA_transfer/05_Tumor_UMI_and_pseudobulk/` | `Tumor_pseudobulk_44_log2CPM_plus_1.tsv`, `patient_input_audit.tsv`, `fixed_44_feature_mapping.tsv` |
| `data_processed/MTAP_RNA_prediction/16_scRNA_transfer/08_L2_cell_number_stability_and_candidate/models/` | `GBM_snRNA_three_gene_L2_candidate.joblib` |
| `data_processed/MTAP_RNA_prediction/15_region_multitask_DL/08_TPM_retraining/04_locked_models_and_thresholds/` | `region_multitask_TPM44_network.py`, `locked_manifest.json`, `models/DL_seed41.pt`, `models/DL_seed42.pt`, `models/DL_seed43.pt` |
| `metadata/` | Local `GSE327167_OGM_reference_labels.tsv` prepared above |

The supplementary sheet is `1A_SAMPLE_CHARACTERISTICS`, with fields `sc_SeqDataID`,
`sc_SampleSetID`, `TB_CaseID`, `anatomic site`, and `case diagnosis`.
The author cell table requires `cell_id`, `library_id`, `manuscript_id`,
`malignant_classification_clonal_analysis`, `stringent_cell_type`, and
`stringent_cell_class`. The fixed feature map requires `feature`, `feature_order`,
and `Ensembl_ID`. These are the required source-table fields.

Patient mapping uses the supplementary library and sample-set identifiers and checks
agreement where both are available. `manuscript_id` is a sample-set key, not a Case ID.
The stringent cell axis must contain 93,351 unique cells and align one-to-one with author
metadata. Pseudobulk combines all included tumor sites for each evaluated patient;
whole tissue includes malignant and nonmalignant cells. The original malignant-cell
eligibility rules and all-gene UMI denominators remain in the inference stage.

## 3. Execution and review

Set `MTAP_PROJECT_ROOT` to the local research project directory. The default notebook
mode registers stages and reads cached outputs; it does not rerun scientific analyses.
Set `MTAP_RUN_WORKFLOW=1` before starting Jupyter only when rerunning the complete workflow.
The input preparation stage is `s73_gse327167_setup`, immediately before `s74_0`.

A new GSE327167 run writes a timestamped output directory. Its heatmaps and unified
summary read that same run. To inspect an existing run in default mode, set
`MTAP_GSE327167_RUN_DIR` to its absolute output directory before starting Jupyter.
`MTAP_GSE327167_OGM_LABELS` optionally overrides the reference TSV location.

The 0.75 deployment rule and the 0.50 sensitivity comparison are evaluated
separately. Thresholds are not selected using this external cohort. Numerical
reproduction with the research inputs and model artifacts remains to be verified
before a manuscript release.
