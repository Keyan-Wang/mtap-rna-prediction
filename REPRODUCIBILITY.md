# Reproducibility status

The source notebook contains the complete supplied three-model research workflow. Syntax checks and matching notebook/script content do not establish numerical reproduction of published results. The complete scientific pipeline has not been executed in the preparation environment.

## Required local material

- Audited TCGA patient/DNA tables, source RNA matrices, fixed patient splits, and model-specific expression/feature specifications.
- CPTAC expression, DNA calls, and patient/sample mappings for the mapped cancer types.
- Trusted external source utilities, their exact revisions, saved network definitions, and matching model checkpoints/manifests.
- GBM raw UMI matrices, annotations, DNA labels, and all-gene UMI denominators.
- The original GSE327167 upstream setup, verified patient/sample mapping and OGM outcome mapping, and the transfer-model artifacts it references.

Relative paths and expected fields are recorded in Model.ipynb. Set MTAP_PROJECT_ROOT before use. Do not infer missing OGM outcomes from RNA scores or aggregate class counts.

## Execution modes

The default mode registers analysis stages and reads cached prediction files. A full research rerun requires MTAP_RUN_WORKFLOW=1. The stage registry preserves source dependency order. GSE327167 will stop if the required upstream objects are absent.

Historical analysis branches use different cohort sizes, expression units, feature sets, and model artifacts. Do not treat one branch's denominator or checkpoint as universal. The original holdout has been inspected historically and is not a new prospective validation.

The 0.75 rule was selected in the GBM transfer setting. Comparisons at 0.50 and 0.80 remain sensitivity analyses. Existing source bootstrap analyses have their own settings; the TCGA original-holdout stage uses 1,000 resamples.

## Before a manuscript release

Restore the missing upstream setup, document input acquisition and external source revisions, record exact checkpoint checksums and a tested package/CUDA environment, verify the final model branches from a fresh kernel, and archive the exact publication version. Choose an appropriate code license before labeling the repository with a license badge.

The public repository contains code and documentation only. Full scientific execution writes local patient-level files, which must not be staged or committed.
