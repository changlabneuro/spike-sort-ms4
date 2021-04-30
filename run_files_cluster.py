import sorting
import util
import multiprocess
import numpy as np
import os

INPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files'
OUTPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files_ms4_sorting'
PARALLEL = True
NUM_PARALLEL_PROCESSES = 28

def sort_several(files):
    for file in files:
        sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, file)

def create_sorting_task(files):
    return (lambda f: lambda: sort_several(f))(files)

if __name__ == '__main__':
    _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')
    filename_sets = np.array_split(src_filenames, NUM_PARALLEL_PROCESSES)
    fs = [create_sorting_task(f) for f in filename_sets]

    if PARALLEL:
        multiprocess.run_tasks(multiprocess.make_tasks(fs))
    else:
        for f in fs:
            f()