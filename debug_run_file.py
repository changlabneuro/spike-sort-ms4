import sorting
from common import MSSortingIO, MSSortingParameters, MSPreprocessingParameters, MSPostprocessingParameters
import util
import os

INPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/raw_data'
OUTPUT_ROOT = '/media/chang/T41/data/mountainsort-plexon-pipeline/test_output'
SRC_FILENAME = 'acc_1_04072016_kurosawacoppola_pre.mat'

def run(input_root, output_root, src_filename):
    input_file = os.path.join(input_root, src_filename)

    io = MSSortingIO(output_root, src_filename)
    sort_params = MSSortingParameters()
    preprocess_params = MSPreprocessingParameters()
    postprocess_params = MSPostprocessingParameters()

    timeseries = util.mat_to_timeseries(util.load_mat(input_file))
    recording = sorting.extract_recording(timeseries, sort_params)
    recording_f = sorting.preprocess_recording(recording, preprocess_params)
    sorter = sorting.sort_recording_ms4(recording_f, sort_params, io)
    sorting.postprocess_recording(recording_f, sorter, postprocess_params, io)
    sorting.export_params_for_phy(recording_f, sorter, io)

if __name__ == '__main__':
    run(INPUT_ROOT, OUTPUT_ROOT, SRC_FILENAME)
