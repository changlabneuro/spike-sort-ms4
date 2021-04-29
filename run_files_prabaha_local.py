import sorting
import util
import multiprocess
import os

INPUT_ROOT = '/Users/prabaha/Box/NeuralData/test_ms4_few_files/raw'
OUTPUT_ROOT = '/Users/prabaha/Box/NeuralData/test_ms4_few_files/sorter_output'

if __name__ == '__main__':
    _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')

    # src_filenames = ['acc_1_04072016_kurosawacoppola_pre.mat',
    #                  'acc_1_04122016_kurosawacoppola_pre.mat',
    #                  'acc_1_04192016_kurosawacoppola_pre.mat',
    #                  'acc_1_04202016_kurosawacoppola_pre.mat']

    for f in src_filenames:
        sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f)
