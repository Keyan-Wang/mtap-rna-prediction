"""Run a small synthetic L2 example, separate from the manuscript workflow.

The feature values, labels, and fitted coefficients are synthetic. This example
checks basic installation, patient-row splitting, scaling, evaluation, and
plotting. It does not validate the published model or any biological claim.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score, brier_score_loss, precision_recall_curve,
    roc_auc_score, roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


SEED = 20261121
FEATURES = ["MTAP", "CDKN2A", "CDKN2B"]


def run(output_dir):
    """Use simulated rows only; fit scaling exclusively on training rows."""
    rng = np.random.default_rng(SEED)
    features = pd.DataFrame(
        rng.normal(size=(300, 3)), columns=FEATURES
    )
    # This arbitrary generating mechanism is not a biological model.
    logits = features.to_numpy() @ np.array([-1.2, -0.5, -0.3]) - 1.5
    probability = 1 / (1 + np.exp(-logits))
    labels = rng.binomial(1, probability)
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.20, stratify=labels, random_state=SEED
    )
    if not x_train.index.intersection(x_test.index).empty:
        raise RuntimeError("Training and test rows overlap.")

    model = Pipeline([
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(
            C=1.0, solver="lbfgs", max_iter=1000, random_state=SEED
        )),
    ])
    model.fit(x_train, y_train)
    scores = model.predict_proba(x_test)[:, 1]
    result = {
        "data_type": "SYNTHETIC_DEMONSTRATION_ONLY",
        "seed": SEED,
        "n_rows": len(features),
        "n_training_rows": len(x_train),
        "n_test_rows": len(x_test),
        "features": FEATURES,
        "AUROC": float(roc_auc_score(y_test, scores)),
        "AP": float(average_precision_score(y_test, scores)),
        "Brier": float(brier_score_loss(y_test, scores)),
        "manuscript_model_validated": False,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "synthetic_demo_metrics.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    with plt.rc_context({"font.size": 10, "pdf.fonttype": 42}):
        fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8))
        fpr, tpr, _ = roc_curve(y_test, scores)
        precision, recall, _ = precision_recall_curve(y_test, scores)
        axes[0].plot(fpr, tpr, color="#33539E", lw=2)
        axes[0].plot([0, 1], [0, 1], ls="--", color="#A0A0A0", lw=1)
        axes[0].set(xlabel="False-positive rate", ylabel="True-positive rate",
                    title=f"Synthetic ROC | AUROC {result['AUROC']:.3f}")
        axes[1].step(recall, precision, where="post", color="#A5678E", lw=2)
        axes[1].axhline(y_test.mean(), ls="--", color="#A0A0A0", lw=1)
        axes[1].set(xlabel="Recall", ylabel="Precision",
                    title=f"Synthetic PR | AP {result['AP']:.3f}")
        for ax in axes:
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1.02)
            ax.spines[["top", "right"]].set_visible(False)
        fig.suptitle("Synthetic installation demonstration only", fontsize=11)
        fig.tight_layout()
        fig.savefig(output_dir / "synthetic_demo_curves.pdf", bbox_inches="tight")
        fig.savefig(output_dir / "synthetic_demo_curves.png", dpi=200,
                    bbox_inches="tight")
        plt.close(fig)

    print("SYNTHETIC DEMONSTRATION ONLY. Not manuscript performance.")
    print(f"Training rows: {len(x_train)}; test rows: {len(x_test)}")
    print(f"AUROC={result['AUROC']:.3f}; AP={result['AP']:.3f}; "
          f"Brier={result['Brier']:.3f}")
    print("Saved synthetic_demo_metrics.json and synthetic_demo_curves.pdf/.png.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path("outputs") / "synthetic_demo",
    )
    args = parser.parse_args()
    run(args.output_dir)


if __name__ == "__main__":
    main()
