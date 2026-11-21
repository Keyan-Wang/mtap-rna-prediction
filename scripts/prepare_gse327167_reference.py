#!/usr/bin/env python3
"""Extract audited OGM labels locally without executing a private notebook.

The output is a private research input, not a file for the public repository.
"""

import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path


def extract_reference(notebook_path):
    """Read literal cohort definitions; never evaluate notebook code."""
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    candidates = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        source = source if isinstance(source, str) else "".join(source)
        if "GSE327167" not in source:
            continue
        definitions = {}
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {
                    "OGM_PATIENTS",
                    "OGM_DEEP_DELETION_PATIENTS",
                }:
                    try:
                        value = ast.literal_eval(node.value)
                    except (ValueError, TypeError, SyntaxError):
                        continue
                    if target.id in definitions and definitions[target.id] != value:
                        raise ValueError(
                            "Conflicting reference definitions within one cell."
                        )
                    definitions[target.id] = value
        if len(definitions) != 2:
            continue
        patients = [str(v).strip() for v in definitions["OGM_PATIENTS"]]
        positive = {str(v).strip() for v in definitions["OGM_DEEP_DELETION_PATIENTS"]}
        if (
            len(patients) != 31
            or len(set(patients)) != 31
            or not all(patients)
            or len(positive) != 4
            or not positive.issubset(patients)
        ):
            raise ValueError(
                "Expected a verified 31-patient reference with four detected deletions."
            )
        candidates.append({p: int(p in positive) for p in patients})
    if not candidates:
        raise ValueError("No complete literal GSE327167 cohort definition was found.")
    if any(candidate != candidates[0] for candidate in candidates[1:]):
        raise ValueError(
            "Conflicting GSE327167 cohort definitions; review before exporting."
        )
    return candidates[0]


def export_reference(notebook_path, output_root):
    """Write the verified reference and source digest outside version control."""
    reference = extract_reference(notebook_path)
    destination = output_root / "metadata/GSE327167_OGM_reference_labels.tsv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Refuse accidental replacement of a previous local audit.
    with destination.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["patient_id", "OGM_deep_deletion_label"])
        writer.writerows(reference.items())
    provenance = {
        "source_notebook_sha256": hashlib.sha256(
            notebook_path.read_bytes()
        ).hexdigest(),
        "label_file_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "n_patients": len(reference),
        "n_OGM_detected_deep_deletion": sum(reference.values()),
        "interpretation_1": "OGM-detected MTAP deep deletion",
        "interpretation_0": "No OGM-detected MTAP deep deletion",
    }
    destination.with_suffix(".provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    print("Prepared local reference: 31 patients; 4 detected and 27 not detected.")
    print("Keep the reference table, provenance, and private source notebook outside Git.")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    export_reference(
        args.notebook.expanduser().resolve(), args.output_root.expanduser().resolve()
    )


if __name__ == "__main__":
    main()
