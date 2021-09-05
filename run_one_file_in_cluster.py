import sorting
import util
import sys

INPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files'
OUTPUT_ROOT = '/gpfs/milgram/project/chang/pg496/nn_all_raw_files_ms4_sorting_300_6000'

def create_sorting_task(file):
    return (lambda f: lambda: sorting.matlab_source_file_default_pipeline(INPUT_ROOT, OUTPUT_ROOT, f))(file)

if __name__ == '__main__':
    filename = sys.argv[1]
    print(sys.argv[1])
    sort_task = create_sorting_task(filename)
    sort_task()
