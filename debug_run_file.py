import sorting
import util
import multiprocess
import os

INPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/raw_data'
OUTPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/test_output'
PARALLEL = True

if __name__ == '__main__':
    # _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')
    
    src_filenames = ['acc_1_04072016_kurosawacoppola_pre.mat', 
                     'acc_1_04122016_kurosawacoppola_pre.mat', 
                     'acc_1_04192016_kurosawacoppola_pre.mat',
                     'acc_1_04202016_kurosawacoppola_pre.mat']

    if PARALLEL:
        fs = [lambda _: sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f) for f in src_filenames]
        tasks = multiprocess.make_tasks(fs)
        multiprocess.run_tasks(tasks)

    else:
        for f in src_filenames:
            sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f)
