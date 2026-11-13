#!/bin/bash
#SBATCH --job-name=NullTriAgg
#SBATCH --account=YOUR_ALLOCATION
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4g
#SBATCH --time=00:30:00
#SBATCH --constraint="scratch&work"
#SBATCH -o /path/to/data/main_experiments/null_triangles_5fold_v1/logs/aggregate_null_triangles_%j.out
#SBATCH -e /path/to/data/main_experiments/null_triangles_5fold_v1/logs/aggregate_null_triangles_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL

# Collects the 48 layer shards into tables/ after the replay array (submit with
# --dependency=afterok:<array job>). Refuses to run unless every layer validated.
module reset
module load python
source ~/protein_venv/bin/activate

export CSV_ROOT=${CSV_ROOT:-/path/to/data}
export NULL_TRIANGLES_OUTPUT_ROOT=${NULL_TRIANGLES_OUTPUT_ROOT:-$CSV_ROOT/main_experiments/null_triangles_5fold_v1}
SCRIPT_DIR=${SLURM_SUBMIT_DIR:-$(pwd)}
echo "[$(date -u +%FT%TZ)] start aggregation output=$NULL_TRIANGLES_OUTPUT_ROOT"
srun python3 -u "$SCRIPT_DIR/aggregate_null_triangles.py"
status=$?
echo "[$(date -u +%FT%TZ)] end aggregation status=$status"
exit $status
