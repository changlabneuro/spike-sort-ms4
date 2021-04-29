import util
import numpy as np
import scipy
import os

import spikeinterface.extractors as se
import spikeinterface.sorters as ss
import spikeinterface.toolkit as st

def extract_recording(timeseries, sorting_params):
    sampling_frequency = sorting_params.sampling_frequency
    num_channels = timeseries.shape[0]
    if sorting_params.geometry is None:
        geom = np.zeros((num_channels, 2))
        geom[:, 0] = range(num_channels)
    else:
        geom = sorting_params.geometry
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

def make_mat_features(wf_sem, templates, max_chan, metrics):
    return {
        'wf_sem': wf_sem,
        'templates': templates,
        'maxchn': max_chan,
        'metrics': metrics
    }

def waveform_sem(all_wf):
    wf_sem = []
    for unit_num in range(len(all_wf)):
        wf = all_wf[unit_num]
        wf_sem.append(scipy.stats.sem(wf, axis=0))
    return wf_sem

def postprocess_recording(recording_f, sorting, params, io):
    features_dir = io.features_directory()
    util.require_directory(features_dir)

    ##########################################
    # Extract each waveform for each spike   #
    ##########################################
    all_wf = st.postprocessing.get_unit_waveforms(recording_f, sorting, ms_before=params.waveform_ms_before, 
                                                                        ms_after=params.waveform_ms_after, 
                                                                        max_spikes_per_unit=None,
                                                                        save_as_features=True, 
                                                                        verbose=True)
    wf_sem = waveform_sem(all_wf)

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
                                                    metric_names=params.metric_names,
                                                    as_dataframe=False)
    # metrics.to_csv(os.path.join(features_dir, 'metrics.csv'))

    features_file = os.path.join(features_dir, 'extracted_features.mat')
    mat_features = make_mat_features(wf_sem, templates, max_chan, metrics)
    scipy.io.savemat(features_file, mat_features, do_compression=True)

    #######################################################################
    # Compute waveform features like half-max width and peak-trough ratio #
    #######################################################################
    features = st.postprocessing.compute_unit_template_features(recording_f, sorting, 
                                                                max_spikes_per_unit=None, 
                                                                as_dataframe=True, 
                                                                upsampling_factor=params.unit_template_upsampling_factor)
    features.to_csv(os.path.join(features_dir, 'features.csv'))

def export_params_for_phy(recording_f, sorting, io):
    vis_dir = io.visualization_directory()
    util.require_directory(vis_dir)
    st.postprocessing.export_to_phy(recording_f, sorting, output_folder=vis_dir, verbose=True)
