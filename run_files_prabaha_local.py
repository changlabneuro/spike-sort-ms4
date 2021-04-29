import sorting
import util
import multiprocess
import os

INPUT_ROOT = '/Users/prabaha/Box/NeuralData/test_ms4_few_files/raw'
OUTPUT_ROOT = '/Users/prabaha/Box/NeuralData/test_ms4_few_files/sorter_output'
PARALLEL = False

def create_sorting_task(file):
    return (lambda f: lambda: sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f))(file)

if __name__ == '__main__':
    # _, src_filenames, _ = util.find_files(INPUT_ROOT, '.mat')

    # Here you can provide a list of specific files to be sorted instead
    
    # src_filenames = ['acc_1_04072016_kurosawacoppola_pre.mat',
    #                  'acc_1_04122016_kurosawacoppola_pre.mat',
    #                  'acc_1_04192016_kurosawacoppola_pre.mat',
    #                  'acc_1_04202016_kurosawacoppola_pre.mat']

    src_filenames = ['acc_kuro_05292017.mat']

    fs = [create_sorting_task(f) for f in src_filenames]

    if PARALLEL:
        multiprocess.run_tasks(multiprocess.make_tasks(fs))
    else:
        for f in fs:
            f()
