import util
import numpy as np
import scipy
import os

import spikeinterface.extractors as se
import spikeinterface.sorters as ss
import spikeinterface.toolkit as st

def default_make_ms_params():
    return ss.Mountainsort4Sorter.default_params()

class MSSortingIO(object):
    def __init__(self, root, src_filename, **kwargs):
        self.root = root
        self.src_filename = src_filename
        self.sort_subdir = 'sorting_output'
        self.features_subdir = 'extracted_features'
        self.visualization_subdir = 'visualization_phy'

    def src_filename_sans_ext(self):
        return os.path.splitext(self.src_filename)[0]

    def sort_directory(self):
        return os.path.join(self.root, self.sort_subdir, self.src_filename_sans_ext())
    
    def features_directory(self):
        return os.path.join(self.root, self.features_subdir, self.src_filename_sans_ext())

    def features_filename(self, ext='.mat'):
        return 'extracted_features{}'.format(ext)

    def visualization_directory(self):
        return os.path.join(self.root, self.visualization_subdir, self.src_filename_sans_ext())

class MSSortingParameters(object):
    def __init__(self, **kwargs):
        self.make_ms_params = kwargs.get('make_ms_params', default_make_ms_params)
        self.sampling_frequency = kwargs.get('sampling_frequency', 40000)
        self.detect_threshold = kwargs.get('detect_threshold', 3.5)
        self.filter_on_sort = kwargs.get('filter_on_sort', False)
        self.geometry = kwargs.get('geometry', None)

    def ms_params(self):
        ms_params = self.make_ms_params()
        ms_params['detect_threshold'] = self.detect_threshold
        ms_params['filter'] = self.filter_on_sort
        return ms_params

class MSPreprocessingParameters(object):
    def __init__(self, **kwargs):
        self.filter_type = kwargs.get('filter_type', 'butter')
        self.filter_freq_min = kwargs.get('filter_freq_min', 300)
        self.filter_freq_max = kwargs.get('filter_freq_max', 6000)

class MSPostprocessingParameters(object):
    def __init__(self, **kwargs):
        self.waveform_ms_before = kwargs.get('waveform_ms_before', 1)
        self.waveform_ms_after = kwargs.get('waveform_ms_after', 2)
        self.unit_template_upsampling_factor = kwargs.get('unit_template_upsampling_factor', 1)
        self.metric_names = kwargs.get('metric_names', ['firing_rate', 'isi_violation', 'snr'])
