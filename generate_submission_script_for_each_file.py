import sys
import os

if len(sys.argv) > 1:
    target_filename = sys.argv[1]
    i = sys.argv[2]
    script = r"""#!/bin/bash
#SBATCH --job-name={}-{}
#SBATCH --nodes=1 --ntasks=1 --cpus-per-task=28
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=ALL
#SBATCH --partition=psych_day --time=12:00:00
    
module load miniconda
conda activate ms4_sorting_env
python run_one_file_in_cluster.py {}""".format(i, target_filename, target_filename)
    print('The script generated is:')
    print(script)
    with open('submit-{}.sh'.format(target_filename), 'w') as f:
        f.write(script)
