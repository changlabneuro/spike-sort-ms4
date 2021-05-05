import util
from common import MSSortingIO, MSSortingParameters, MSPreprocessingParameters, MSPostprocessingParameters
import numpy as np
import scipy
import os
import random

import spikeinterface.extractors as se
import spikeinterface.sorters as ss
import spikeinterface.toolkit as st

def extract_recording(timeseries, sorting_params):
    sampling_frequency = sorting_params.sampling_frequency
    num_channels = timeseries.shape[0]
    geom = sorting_params.get_geometry(num_channels)
    return se.NumpyRecordingExtractor(timeseries=timeseries, geom=geom, sampling_frequency=sampling_frequency)

def preprocess_recording(recording, preprocess_params):
    return st.preprocessing.bandpass_filter(recording, filter_type=preprocess_params.filter_type, 
                                                       freq_min=preprocess_params.filter_freq_min, 
                                                       freq_max=preprocess_params.filter_freq_max)

def sort_recording_ms4(recording_f, sorting_params, io):
    output_dir = io.sort_directory()
    util.require_directory(output_dir)
    ms4_params = sorting_params.ms_params()
    return ss.run_mountainsort4(recording_f, **ms4_params, output_folder=output_dir)

def make_mat_file(src_filename, wf_sem, max_norm_templates, example_wf, templates, max_chan, \
                  metrics, features, pre_params, sort_params, post_params):
    return {
        'src_filename': src_filename,
        'wf_sem': wf_sem,
        'max_normalized_templates': max_norm_templates,
        'example_wf': example_wf,
        'templates': templates,
        'maxchn': max_chan,
        'metrics': metrics,
        'features': features,
        'preprocess_params': pre_params.to_dict(),
        'sort_params': sort_params.to_dict(),
        'postprocess_params': post_params.to_dict()
    }

def waveform_sem(all_wf):
    wf_sem = []
    for unit_num in range(len(all_wf)):
        wf = all_wf[unit_num]
        wf_sem.append(scipy.stats.sem(wf, axis=0))
    return wf_sem

def extract_example_waveforms(all_wf, max_num_wfs):
    example_wf = []
    for i in range(len(all_wf)):
        wf = all_wf[i]
        random_max_num_wfs = random.sample(range(wf.shape[0]), min(wf.shape[0], int(max_num_wfs)))
        examples = wf[random_max_num_wfs, :, :]
        example_wf.append(examples)
    return example_wf

def max_normalized_template(wf):
    denom = np.max(np.abs(wf), axis=2)
    res = wf.copy()
    for i in range(res.shape[2]):
        res[:, :, i] /= denom
    return np.mean(res, axis=0)

def max_normalized_templates(all_wf):
    templates = []
    for i in range(len(all_wf)):
        templates.append(max_normalized_template(all_wf[i]))
    return templates

def save_mat_file(mat_file, io):
    mat_dir = io.matlab_directory()
    util.require_directory(mat_dir)
    mat_file_path = os.path.join(mat_dir, io.matlab_filename())
    scipy.io.savemat(mat_file_path, mat_file, do_compression=True)

def postprocess_recording(recording_f, sorting, io, pre_params, sort_params, post_params, save=True):
    ##########################################
    # Extract each waveform for each spike   #
    ##########################################
    all_wf = st.postprocessing.get_unit_waveforms(recording_f, sorting, #ms_before=post_params.waveform_ms_before, 
                                                                        #ms_after=post_params.waveform_ms_after, 
                                                                        max_spikes_per_unit=None,
                                                                        save_as_features=True, 
                                                                        verbose=True)
    max_norm_templates = max_normalized_templates(all_wf)
    wf_sem = waveform_sem(all_wf)
    example_wf = extract_example_waveforms(all_wf, post_params.max_num_example_waveforms_per_unit)

    ##########################################
    # Get the average waveform for each unit #
    ##########################################
    templates = st.postprocessing.get_unit_templates(recording_f, sorting, 
                                                     max_spikes_per_unit=None,
                                                     save_as_property=True, 
                                                     verbose=False)
    templates = np.array(templates)

    #######################################################
    # Retreive the channel of highest prob. for each unit #
    #######################################################
    max_chan = st.postprocessing.get_unit_max_channels(recording_f, sorting, 
                                                       save_as_property=True, 
                                                       verbose=False)

    ###################################################
    # Compute verification metrics like isi violation #
    ###################################################
    metrics = st.validation.compute_quality_metrics(sorting=sorting, 
                                                    recording=recording_f,
                                                    metric_names=post_params.metric_names,
                                                    as_dataframe=False)

    #######################################################################
    # Compute waveform features like half-max width and peak-trough ratio #
    #######################################################################
    features = st.postprocessing.compute_unit_template_features(recording_f, sorting, 
                                                                max_spikes_per_unit=None, 
                                                                as_dataframe=False, 
                                                                upsampling_factor=post_params.unit_template_upsampling_factor)

    mat_file = make_mat_file(io.src_filename, wf_sem, max_norm_templates, example_wf, \
                             templates, max_chan, metrics, features, \
                             pre_params, sort_params, post_params)

    if save:
        save_mat_file(mat_file, io)

    return mat_file

def export_params_for_phy(recording_f, sorting, io):
    vis_dir = io.visualization_directory()
    util.require_directory(vis_dir)
    st.postprocessing.export_to_phy(recording_f, sorting, output_folder=vis_dir, verbose=True)

def pipeline(timeseries, io, preprocess_params, sort_params, postprocess_params):
    recording = extract_recording(timeseries, sort_params)
    recording_f = preprocess_recording(recording, preprocess_params)
    sorter = sort_recording_ms4(recording_f, sort_params, io)
    postprocess_recording(recording_f, sorter, io, preprocess_params, sort_params, postprocess_params)
    export_params_for_phy(recording_f, sorter, io)

def matlab_source_file_default_pipeline(input_root, output_root, src_filename, 
                                        preprocess_params=MSPreprocessingParameters(),
                                        sort_params=MSSortingParameters(),
                                        postprocess_params=MSPostprocessingParameters()):
    input_file = os.path.join(input_root, src_filename)
    timeseries = util.mat_to_timeseries(util.load_mat(input_file))

    io = MSSortingIO(output_root, src_filename)
    pipeline(timeseries, io, preprocess_params, sort_params, postprocess_params)