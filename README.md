# MTAP deletion prediction from RNA expression

Research code for pan-cancer prediction of **MTAP deep deletion**, accompanying the manuscript in preparation:

*Pan-cancer multi-omics landscape of MTAP loss: decoding microenvironment remodeling and synthetic lethality vulnerability.*

## Models

- **Three-gene L2 logistic regression:** MTAP, CDKN2A, and CDKN2B.
- **44-gene Elastic Net:** regularization selected within development data.
- **Deep learning:** regional multitask PyTorch models, including independent retraining of the 44-member TPM branch and patient-level input adaptation.

Earlier three-gene, eight-gene, 28-gene, and 45-feature comparisons are retained as supporting development analyses. Feature order, preprocessing, cohort eligibility, checkpoints, and thresholds are model-specific.

## Workflow

`Model.ipynb` contains nine sections:

1. Environment setup and data ingestion.
2. EDA and cohort definition.
3. Preprocessing and the fixed 80/20 patient split.
4. TCGA development-set training of the three models.
5. Frozen-model evaluation on the original TCGA holdout.
6. CPTAC external validation across mapped cancer types.
7. GBM single-nucleus and GSE327167 single-cell pseudobulk transfer.
8. Whole-tissue/malignant-cell comparisons, threshold sensitivity, and cross-cohort performance metrics.
9. ROC/PR curves, annotated metric heatmaps, and coefficient plots.

TCGA development performance uses out-of-fold predictions. The original holdout audit uses 1,000 bootstrap resamples and evaluates the available matched expression subset. The 16-patient GBM snRNA analysis is a separate transfer cohort. Pseudobulk predictions are patient-level and do not establish genomic labels for individual cells.

## Data sources

This repository contains analysis code only. Raw data, patient-level tables,
and author-provided mapping files are not redistributed.

- **TCGA Pan-Cancer Atlas:** processed RNA expression matrices and gene-level
  GISTIC copy-number calls for model development and internal evaluation.
  [Data access](https://gdc.cancer.gov/about-data/publications/pancanatlas)

- **CPTAC:** processed bulk RNA expression and matched genomic annotations
  from published CPTAC cohorts for external validation.
  [CPTAC resources](https://proteomics.cancer.gov/programs/cptac)

- **GBM snRNA-seq:** a 16-patient analysis subset from the CPTAC GBM study
  by Wang et al. (Cancer Cell, 2021).
  [Publication](https://doi.org/10.1016/j.ccell.2021.01.006) |
  [CPTAC-3](https://portal.gdc.cancer.gov/projects/CPTAC-3)

- **GSE327167 scRNA-seq:** processed expression matrices and cell annotations
  from GEO. OGM-derived reference labels were assembled from published
  supplementary data and additional sample-to-patient mapping information
  provided by the study authors. Labels distinguish OGM-detected MTAP deep
  deletion from no OGM-detected MTAP deep deletion.
  [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327167)

Access conditions follow the original repositories and studies.

## Installation and usage

```bash
python -m pip install -r requirements.txt
python -m jupyterlab Model.ipynb
```

Set `MTAP_PROJECT_ROOT` to the local research project directory. By default, the notebook registers the scientific stages and summarizes existing prediction files. Set `MTAP_RUN_WORKFLOW=1` before launching Jupyter to execute the source pipeline in dependency order.

Python 3.12 and the pinned core dependencies describe the preparation/test
environment; they are not a validated environment lock for the full workflow.

## Reproducibility

`Model.py` provides the Python script corresponding to `Model.ipynb`.

The GSE327167 analysis requires the original verified upstream setup.
Complete reproduction from a fresh kernel remains to be verified.
See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and
`validation_report.json` for dependencies, required inputs, and current
limitations.

Keep local research outputs outside Git and clear notebook outputs before
committing changes.

Publication citation and software-release details will be added when available.


