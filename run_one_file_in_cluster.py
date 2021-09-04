import sorting
import util

INPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files'
OUTPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files_ms4_sorting_300_6000'

def sort_several(files):
    for file in files:
        sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, file)

def create_sorting_task(files):
    return (lambda f: lambda: sort_several(f))(files)

filename = sys.argv[1]
sort_task = create_sorting_task([filename])
sort_task()
