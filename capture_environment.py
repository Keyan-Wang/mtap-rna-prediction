"""Record selected package versions without exporting research data or paths."""

import argparse
from datetime import datetime, timezone
from importlib import metadata
import json
from pathlib import Path
import platform

CORE = (
    "numpy", "pandas", "scipy", "scikit-learn", "matplotlib",
    "torch", "h5py", "anndata", "joblib", "ipython", "jupyterlab",
)
OPTIONAL = ("openpyxl", "xlrd", "nbformat", "nbclient")


def capture(output_dir):
    """Record the environment being inspected; this does not validate models."""
    versions = {}
    for package in CORE + OPTIONAL:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None

    report = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "operating_system": platform.system(),
        "machine": platform.machine(),
        "packages": versions,
        "missing_core_packages": [p for p in CORE if versions[p] is None],
        "optional_excel_readers": ["openpyxl", "xlrd"],
        "scientific_workflow_executed_by_this_script": False,
        "note": (
            "Observed package versions are not a validated environment lock. "
            "Record this environment only if it is used for the actual analysis."
        ),
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "environment_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "requirements.observed.txt").write_text(
        "# Observed environment only; full scientific replay remains separate.\n"
        + "".join(
            f"{p}=={versions[p]}\n"
            for p in CORE + OPTIONAL if versions[p] is not None
        ),
        encoding="utf-8",
    )
    print(f"Python: {report['python']}")
    for package, version in versions.items():
        print(f"{package}: {version or 'NOT INSTALLED'}")
    print("Saved environment_report.json and requirements.observed.txt.")
    print("No patient data, model outputs, or local paths were exported.")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path("outputs") / "environment_audit",
    )
    args = parser.parse_args()
    capture(args.output_dir)


if __name__ == "__main__":
    main()
