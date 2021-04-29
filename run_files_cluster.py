import sorting
import util
import multiprocess
import os

INPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files'
OUTPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files_ms4_sorting'
PARALLEL = True

def create_sorting_task(file):
    return (lambda f: lambda: sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f))(file)

if __name__ == '__main__':
    _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')

    fs = [create_sorting_task(f) for f in src_filenames]

    if PARALLEL:
        multiprocess.run_tasks(multiprocess.make_tasks(fs))
    else:
        for f in fs:
            f()