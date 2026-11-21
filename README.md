# MTAP deletion prediction from RNA expression

Research code for pan-cancer prediction of **MTAP deep deletion**, accompanying the manuscript in preparation:

*Pan-cancer single-cell analysis of MTAP deletion reveals distinct metabolic and immune reprogramming.*

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

## Installation and usage

```bash
python -m pip install -r requirements.txt
python -m jupyterlab Model.ipynb
```

Set `MTAP_PROJECT_ROOT` to the local research project directory. By default, the notebook registers the scientific stages and summarizes existing prediction files. Set `MTAP_RUN_WORKFLOW=1` before launching Jupyter to execute the source pipeline in dependency order.

Python 3.12 and the pinned core package versions describe the preparation/test environment. The complete scientific workflow has not been validated in that environment. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and `validation_report.json` for current dependencies and limitations.

## Data and reproducibility

**No patient-level data, expression matrices, individual predictions, fitted models, or checkpoints are included.** Obtain public data and supporting artifacts separately under their original reuse conditions. Author-provided OGM mappings are not redistributed.

The supplied GSE327167 continuation requires its original verified upstream setup. This repository is a development code archive; complete fresh-kernel reproduction remains to be verified. Local research outputs must stay outside Git. Clear execution outputs before committing a rerun.

`Model.py` provides the corresponding Python script. Publication citation and software-release details will be added when available.
