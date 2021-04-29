import sorting
import util
import os

INPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/raw_data'
OUTPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/test_output'
SRC_FILENAME = 'acc_1_04072016_kurosawacoppola_pre.mat'

if __name__ == '__main__':
    sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, SRC_FILENAME)
