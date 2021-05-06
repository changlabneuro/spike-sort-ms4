import sorting
import common
import util
import multiprocess
import numpy as np
import os
import itertools

# INPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/raw_data'
# OUTPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/test_output'
INPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files'
OUTPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files_ms4_param_comp'
PARALLEL = True
NUM_PARALLEL_PROCESSES = 8

def make_parameters(freq_min, filter_type, noise_overlap_thresh, detect_thresh):
    preprocess_params = common.MSPreprocessingParameters(filter_freq_min=freq_min, filter_type=filter_type)
    sort_params = common.MSSortingParameters(detect_threshold=detect_thresh, 
                                             noise_overlap_threshold=noise_overlap_thresh)
    return preprocess_params, sort_params

def parameter_subdir(freq_min, filter_type, noise_overlap_thresh, detect_thresh):
    return '{}-{}-{}-{}'.format(freq_min, filter_type, noise_overlap_thresh, detect_thresh)

def sort_several(combinations):
    for c in combinations:
        file, freq_min, filter_type, noise_overlap_thresh, detect_thresh = c
        preprocess_params, sort_params = make_parameters(freq_min, filter_type, noise_overlap_thresh, detect_thresh)
        output_subdir = parameter_subdir(freq_min, filter_type, noise_overlap_thresh, detect_thresh)
        sorting.matlab_source_file_default_pipeline(INPUT_ROOT, os.path.join(OUTPUT_ROOT, output_subdir), file,
                                                    sort_params=sort_params, 
                                                    preprocess_params=preprocess_params)

def create_sorting_task(combination):
    return (lambda c: lambda: sort_several(c))(combination)

def get_src_filenames():
    src_filenames = ['acc_05122016_KurosawaCoppola.mat', 'acc_1_04052016_kurocoppola_pre.mat', 'acc_1_Hitch_01052016.mat', 'acc_1_Hitch_01172017_OT.mat']
    # _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')
    return src_filenames

def get_sorting_combinations(src_filenames):
    freq_mins = [300, 400, 500, 600]
    filter_types = ['fft', 'butter']
    noise_overlap_threshs = [0.15, 0.5]
    detect_threshs = [4, 5]
    return list(itertools.product(src_filenames, freq_mins, filter_types, noise_overlap_threshs, detect_threshs))

if __name__ == '__main__':
    src_filenames = get_src_filenames()
    sorting_combs = get_sorting_combinations(src_filenames)

    sorting_sets = np.array_split(sorting_combs, NUM_PARALLEL_PROCESSES)
    fs = [create_sorting_task(s) for s in sorting_sets]

    if PARALLEL:
        multiprocess.run_tasks(multiprocess.make_tasks(fs))
    else:
        for f in fs:
            f()