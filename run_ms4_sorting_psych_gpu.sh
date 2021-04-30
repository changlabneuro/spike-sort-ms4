#!/bin/bash
#SBATCH --job-name=nn_all_raw_files_ms4_sorting
#SBATCH --nodes=1 --ntasks=1 --cpus-per-task=1
#SBATCH --mem-per-cpu=256G --gres=gpu:rtx2080ti:2
#SBATCH --mail-type=ALL
#SBATCH --partition=psych_gpu --time=2-00:00:00


module load miniconda
conda activate ms4_sorting_env

echo "Starting at $(date)"
echo "Job submitted to the ${SLURM_JOB_PARTITION} partition, the default partition on ${SLURM_CLUSTER_NAME}"
echo "Job name: ${SLURM_JOB_NAME}, Job ID: ${SLURM_JOB_ID}"
echo "  I have ${SLURM_CPUS_ON_NODE} CPUs and ${mem_gbytes}GiB of RAM on compute node $(hostname)"

python run_files_cluster.py

