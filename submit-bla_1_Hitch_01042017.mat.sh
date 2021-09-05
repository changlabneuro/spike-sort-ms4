!/bin/bash
#SBATCH --job-name=60-bla_1_Hitch_01042017.mat
#SBATCH --nodes=1 --ntasks=1 --cpus-per-task=28
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=ALL
#SBATCH --partition=psych_day --time=12:00:00
    
module load miniconda
conda activate ms4_sorting_env
python run_one_file_in_cluster.py bla_1_Hitch_01042017.mat