# Match and Correct: A Repeated Computational Motif in Evoformer Layers

Code and result tables for the paper

> Ishan Khire, Naren Manikandan, Tyler Hayes, Giri Krishnan.
> *Match and Correct: A Repeated Computational Motif in Evoformer Layers.*
> Interpretability for Discovery Workshop, NeurIPS 2026. arXiv: _link to be added_.

We probe the pair representation after each of OpenFold's 48 Evoformer blocks. Four probe
families decode final Cα–Cα distances: a shared linear probe, per-protein linear probes, a
sequence-gated linear probe, and XGBoost. Each probe is trained with five-fold
cross-validation on 552 CAMEO and ECOD proteins. From the decoded distances we
reconstruct 3D structures with classical MDS, measure triangle-inequality violations,
compare them with null models, and relate them to cumulative layerwise ablations of
Evoformer components.

This repository is a frozen snapshot of the code that produced the paper (tag `v1.0`).
It contains every result table behind the figures, so **all figures can be regenerated on
a laptop in a few minutes**. Recomputing the tables themselves requires the Evoformer pair
representations and a SLURM cluster; see [Full pipeline](#full-pipeline).

## Quick start

```bash
git clone https://github.com/ishankhire/match-and-correct-evoformer.git
cd match-and-correct-evoformer
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/verify_figures.py
```

`verify_figures.py` copies the repository to a temporary directory, reruns every figure
script there, and compares each regenerated PNG byte for byte with the committed one. To
redraw the figures in place instead:

```bash
python scripts/multi_protein/generate_sept_2_publication_plots.py --from-source-data
python scripts/multi_protein/plot_layerwise_ablation_tm_scores.py
python scripts/multi_protein/null_triangles/analyze_null_triangles.py
python scripts/multi_protein/make_shared_ols_mds_pymol_grid.py
```

**Matplotlib versions.** The committed figures were drawn with two matplotlib versions.
`requirements.txt` pins 3.10.8, which reproduces 34 of the 47 committed PNGs byte for
byte. The other 13 (`main_figure_01`, `main_figure_15_spatial_distance_mae_combined`, the
all-triangle overlay, decodability and legend panels, the four stratified triangle figures,
the sequence-separation figure, and three individual-protein figures) were drawn with
3.11.1. They match exactly after `pip install matplotlib==3.11.1`; under 3.10.8 they
differ only in sub-pixel text rasterisation. The PNG `Software` metadata records which
version drew each file. `verify_figures.py` reports this split and fails only on a mismatch
that the version cannot explain.

## Figures

| Paper | Script | Output |
|---|---|---|
| Fig. 1a, 1b, 1c | `generate_sept_2_publication_plots.py` | `sept_2_plots/main_figures/main_figure_{03_tm_score, 01_mean_per_protein_r2, 15_spatial_distance_mae_combined}` |
| Fig. 2 (a, b, legend) | `generate_sept_2_publication_plots.py` | `sept_2_plots/main_figures/main_figure_all_triangles_{peak_troughs_overlay, decodability_consistency, shared_legend}` |
| Fig. 3 | `null_triangles/analyze_null_triangles.py` | `null_triangles_5fold_v1/figures/main/observed_vs_nulls_normalized_violation` |
| Fig. 4 | `plot_layerwise_ablation_tm_scores.py` | `sept_2_plots/layerwise_ablation_trajectories/combined_layerwise_ablation_tm_score_trajectories` |
| Fig. S1a, S1b | `generate_sept_2_publication_plots.py` | `sept_2_plots/supplemental_figures/supp_figure_{top3_eigenvalue_fraction, mds_stress}` |
| Fig. S2 | `null_triangles/analyze_null_triangles.py` | `null_triangles_5fold_v1/figures/supplement/observed_vs_nulls_violation_fraction` |
| Fig. S3 | `null_triangles/analyze_null_triangles.py` | `null_triangles_5fold_v1/figures/supplement/sensitivity_binning_shared_ols` |
| Fig. S4–S7 | `generate_sept_2_publication_plots.py` | `sept_2_plots/supplemental_figures/triangle_annotated_trajectories/figure_0{2,3,4,5}_*` |
| Fig. S8, S9 | `generate_sept_2_publication_plots.py` | `sept_2_plots/supplemental_figures/supp_figure_all_triangles_violation_fraction_{peak_troughs_overlay, decodability_consistency}` |
| Fig. S10 | `plot_layerwise_ablation_tm_scores.py` | `sept_2_plots/layerwise_ablation_trajectories/tmu_triangle_attention_{fwd,rev}_tm_score_trajectory` |
| Fig. S11 | `generate_sept_2_publication_plots.py` | `sept_2_plots/supplemental_figures/supp_figure_sequence_separation_mae_combined` |
| Fig. S12 | `render_shared_ols_mds_pymol_panels.py` (PyMOL), then `make_shared_ols_mds_pymol_grid.py` | `shared_ols_mds_pdb_exports/shared_ols_mds_structures_visualized.png` |
| Fig. S13–S16 | `generate_sept_2_publication_plots.py` | `sept_2_plots/supplemental_figures/individual_protein_trajectories/supp_figure_individual_proteins_*_by_model` |

Scripts live in `scripts/multi_protein/`. Outputs are under `delta_files/publication_plots/`,
`delta_files/regression_5fold_v1/analysis/` and `delta_files/shared_ols_mds_pdb_exports/`.
The tables each figure reads are listed in `sept_2_plots/figure_manifest.csv` and
`sept_2_plots/generation_summary.json`.

Numbers quoted in the text come from the same tables. Decodability and TM-score values
come from `source_data/{r2,tm_score}_plot_summary.csv`. Peak/trough counts and
Benjamini–Hochberg support come from `source_data/triangle_candidate_extrema.csv`.
Null-model statistics come from `null_triangles_5fold_v1/RESULTS.md`.

## Repository layout

The layout mirrors the working repository, so paths inside the scripts and manifests resolve
unchanged. `delta_files/` holds results synced from the cluster (named after NCSA Delta).

```
scripts/
  multi_protein/        figure scripts (run locally) and their tests
  cluster_scripts/      SLURM jobs that produced the result tables (run on a cluster)
  verify_figures.py     regenerate-and-compare check
delta_files/
  publication_plots/sept_2_plots/      figures, source_data/ tables, figure manifest
  regression_5fold_v1/
    metadata/                          cohort and fold assignments (552 proteins)
    <probe>/                           per-probe fold, pooled and geometry summaries
    triangle_violation_subgroups_5fold_v1/
    analysis/null_triangles_5fold_v1/  null-model tables, figures, RESULTS.md
    analysis/tm_score_optimization_comparison_v1/
  layerwise_ablation_csvs/             per-protein TM-scores from the OpenFold ablations
  shared_ols_mds_pdb_exports/          exported MDS structures and PyMOL panels (Fig. S12)
  xgboost_hyperparameter_search/       XGBoost configuration selection
ecod_protein_categories.csv
```

## Cohort

`scripts/cluster_scripts/regression_protocol_data/regression_master_split_v1.csv` lists all
554 proteins (CAMEO and ECOD). Two ECOD proteins (`000196893`, `001681437`) are excluded
from every analysis, leaving the 552-protein cohort in
`delta_files/regression_5fold_v1/metadata/regression_outer_folds_v1.csv`. The layerwise
ablation CSVs contain all 554, and the plotting script drops the same two.

## Full pipeline

Each step below ran as SLURM array jobs on NCSA Delta. Each `scripts/cluster_scripts/<step>/`
directory has a README with the exact job order. Before running, set `CSV_ROOT` (or edit
`canonical_storage.py`) to your data root. Then replace the placeholders `/path/to/data`,
`/path/to/code`, `/path/to/representations/...`, `YOUR_EMAIL` and `YOUR_ALLOCATION` in the
`.sbatch` files and in `cluster_regression_helpers.py`.

1. **Pair representations.** OpenFold inference on each protein, saving the pair
   representation `z` (128 channels) after every Evoformer block, plus the final structure.
   This step used OpenFold instrumentation that is not part of this repository. The
   arrays are too large to distribute here.
2. **Probes** (`cross_validation/`). Five-fold, protein-level cross-validation of the four
   probe families at every layer. Features are the directional pair vectors
   `[z_ij | z_ji]` (256 dimensions; `regression_protocol.py`). Out-of-fold predictions are
   scored (R², MAE) and reconstructed with classical MDS. XGBoost settings were chosen
   by `xgboost_search/`.
3. **TM-score** (`tm_scores/`). Reconstructions are scored against the final OpenFold
   structure with the `TMscore` program (built from USalign; see that README).
4. **Distance-stratified error** (`publication_figures/`). Per-protein MAE by spatial
   distance and sequence separation.
5. **Triangle violations** (`triangle_violation_subgroups/`). Violation metrics over all
   triangles and by triangle shape and size.
6. **Null models** (`predicted_distances/`, then `null_triangles/`). Out-of-fold predicted
   distances are exported, and the two null models are scored on the cluster.
   `scripts/multi_protein/null_triangles/analyze_null_triangles.py` then produces the
   tables and figures locally.
7. **MDS structure export** (`diagnostics/diagnostic_shared_ols_mds_pdb_export.*`). Writes
   PDB files for the ten-protein panel in Fig. S12. The panels are rendered with PyMOL
   (`render_shared_ols_mds_pymol_panels.py`).
8. **Layerwise ablations.** Cumulative forward and reverse bypass of Evoformer components
   during OpenFold inference. This also used the external OpenFold instrumentation; the
   resulting per-protein TM-scores are in `delta_files/layerwise_ablation_csvs/`.
9. **Summary tables** (`generate_sept_2_publication_plots.py` without
   `--from-source-data`). Reads the per-protein outputs of steps 2–5 and computes the
   paired-protein bootstrap intervals (2,000 replicates, seed 20260902) and the
   peak/trough tests. It writes `source_data/`, which `--from-source-data` reads back.

The cluster runs recorded Python 3.13.5, numpy 2.4.2, scipy 1.17.1, scikit-learn 1.8.0
and xgboost 3.2.0.

## Tests

```bash
TMSCORE_BINARY=/path/to/TMscore pytest scripts
```

The geometry and cross-validation tests call the `TMscore` program (see
`scripts/cluster_scripts/tm_scores/README.md`). Without it, those 17 tests fail with
`TMscore executable unavailable` and the rest pass. On macOS, importing xgboost also
requires the OpenMP runtime (`brew install libomp`). The figure scripts need neither.

## Citation

```bibtex
@inproceedings{khire2026matchcorrect,
  title     = {Match and Correct: A Repeated Computational Motif in Evoformer Layers},
  author    = {Khire, Ishan and Manikandan, Naren and Hayes, Tyler and Krishnan, Giri},
  booktitle = {Interpretability for Discovery Workshop, NeurIPS},
  year      = {2026}
}
```

## License

MIT; see [LICENSE](LICENSE).
