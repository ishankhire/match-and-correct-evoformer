#!/usr/bin/env python3
"""Regenerate every paper figure in a scratch copy and compare it with the committed files.

Runs the four figure scripts on a temporary copy of `scripts/` and `delta_files/`, so the
repository itself is never modified. Each regenerated PNG is compared byte for byte with
the committed PNG. Matplotlib's text rasterisation changes slightly between releases, so a
PNG is only expected to match exactly when the installed matplotlib is the version that
drew the committed file (recorded in the PNG's `Software` metadata). Text outputs of the
null-triangle analysis (tables and RESULTS.md) must match regardless of version.

Exit status is non-zero if any figure is missing, or if any file that should match exactly
does not.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib

ROOT = Path(__file__).resolve().parents[1]
STEPS = (
    ["scripts/multi_protein/generate_sept_2_publication_plots.py", "--from-source-data"],
    ["scripts/multi_protein/plot_layerwise_ablation_tm_scores.py"],
    ["scripts/multi_protein/null_triangles/analyze_null_triangles.py"],
    ["scripts/multi_protein/make_shared_ols_mds_pymol_grid.py"],
)
FIGURE_DIRS = (
    "delta_files/publication_plots/sept_2_plots",
    "delta_files/regression_5fold_v1/analysis/null_triangles_5fold_v1/figures",
)
EXTRA_PNGS = ("delta_files/shared_ols_mds_pdb_exports/shared_ols_mds_structures_visualized.png",)
NULL_ROOT = "delta_files/regression_5fold_v1/analysis/null_triangles_5fold_v1"
TEXT_OUTPUTS = tuple(f"{NULL_ROOT}/{name}" for name in (
    "RESULTS.md", "sanity_checks.md", "summary_table.csv",
    "calibration_by_layer.csv", "clipped_side_fraction.csv",
))


def drawn_with(png: Path) -> str:
    match = re.search(rb"Matplotlib version([0-9.]+)", png.read_bytes()[:4096])
    return match.group(1).decode() if match else "unknown"


def main() -> int:
    installed = matplotlib.__version__
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        for name in ("scripts", "delta_files"):
            shutil.copytree(ROOT / name, work / name)
        for step in STEPS:
            print(f"$ python {' '.join(step)}", flush=True)
            subprocess.run([sys.executable, *step], cwd=work, check=True,
                           stdout=subprocess.DEVNULL)

        committed = sorted({p.relative_to(ROOT) for d in FIGURE_DIRS
                            for p in (ROOT / d).rglob("*.png")} | {Path(p) for p in EXTRA_PNGS})
        rows, failures = [], []
        for rel in committed:
            new = work / rel
            version = drawn_with(ROOT / rel)
            if not new.exists():
                failures.append(f"missing: {rel}")
                continue
            same = new.read_bytes() == (ROOT / rel).read_bytes()
            rows.append((rel, version, same))
            if version == installed and not same:
                failures.append(f"differs although drawn with matplotlib {version}: {rel}")
        for rel in TEXT_OUTPUTS:
            if (work / rel).read_bytes() != (ROOT / rel).read_bytes():
                failures.append(f"text output differs: {rel}")

    exact = sum(same for _, _, same in rows)
    comparable = [r for r in rows if r[1] == installed]
    print(f"\nmatplotlib {installed}: {exact}/{len(rows)} PNGs byte-identical "
          f"({sum(s for _, _, s in comparable)}/{len(comparable)} of those drawn with {installed}).")
    for version in sorted({v for _, v, _ in rows} - {installed}):
        other = [r for r in rows if r[1] == version]
        print(f"  {len(other)} PNGs were drawn with matplotlib {version}; install that version "
              f"to reproduce them byte for byte ({sum(s for _, _, s in other)} match already).")
    print(f"Null-triangle tables and RESULTS.md: "
          f"{'identical' if not any('text output' in f for f in failures) else 'DIFFER'}.")
    if failures:
        print("\nFAILURES:\n  " + "\n  ".join(failures))
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
