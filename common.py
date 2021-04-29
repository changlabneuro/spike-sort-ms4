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
        self.sort_subdir = 'ms4'
        self.matlab_subdir = 'matlab'
        self.visualization_subdir = 'visualization_phy'

    def src_filename_sans_ext(self):
        return os.path.splitext(self.src_filename)[0]

    def sort_directory(self):
        return os.path.join(self.root, self.src_filename_sans_ext(), self.sort_subdir)
    
    def matlab_directory(self):
        return os.path.join(self.root, self.src_filename_sans_ext(), self.matlab_subdir)

    def matlab_filename(self, ext='.mat'):
        return 'sort{}'.format(ext)

    def visualization_directory(self):
        return os.path.join(self.root, self.src_filename_sans_ext(), self.visualization_subdir)

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

    def get_geometry(self, num_channels):
        geom = self.geometry
        if geom is None:
            geom = np.zeros((num_channels, 2))
            geom[:, 0] = range(num_channels)
        return geom

    def to_dict(self):
        return {
            'detect_threshold': self.detect_threshold,
            'filter_on_sort': self.filter_on_sort,
            'sampling_frequency': self.sampling_frequency,
            'geometry': [] if self.geometry is None else self.geometry.copy()
        }

class MSPreprocessingParameters(object):
    def __init__(self, **kwargs):
        self.filter_type = kwargs.get('filter_type', 'butter')
        self.filter_freq_min = kwargs.get('filter_freq_min', 300)
        self.filter_freq_max = kwargs.get('filter_freq_max', 6000)

    def to_dict(self):
        return {
            'filter_type': self.filter_type,
            'filter_freq_min': self.filter_freq_min,
            'filter_freq_max': self.filter_freq_max
        }

class MSPostprocessingParameters(object):
    def __init__(self, **kwargs):
        self.waveform_ms_before = kwargs.get('waveform_ms_before', 1)
        self.waveform_ms_after = kwargs.get('waveform_ms_after', 2)
        self.unit_template_upsampling_factor = kwargs.get('unit_template_upsampling_factor', 1)
        self.metric_names = kwargs.get('metric_names', ['firing_rate', 'isi_violation', 'snr'])

    def to_dict(self):
        return {
            'waveform_ms_before': self.waveform_ms_before,
            'waveform_ms_after': self.waveform_ms_after,
            'unit_template_upsampling_factor': self.unit_template_upsampling_factor,
            'metric_names': list(self.metric_names)
        }
