import sorting
import util
import multiprocess
import os

INPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/raw_data'
OUTPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/test_output'
PARALLEL = False

if __name__ == '__main__':
    # _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')

    src_filenames = ['acc_1_04072016_kurosawacoppola_pre.mat',
                     'acc_1_04122016_kurosawacoppola_pre.mat',
                     'acc_1_04192016_kurosawacoppola_pre.mat',
                     'acc_1_04202016_kurosawacoppola_pre.mat']

    fs = [lambda: sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f) for f in src_filenames]

    if PARALLEL:
        multiprocess.run_tasks(multiprocess.make_tasks(fs))
    else:
        for task in fs:
            task()