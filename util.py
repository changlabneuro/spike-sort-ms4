import os
import scipy
import h5py
import numpy as np

def require_directory(d):
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def load_mat(file_path):
    try:
        f = h5py.File(file_path, 'r')
    except:
        f = scipy.io.loadmat(file_path)
    return f

def maybe_transpose(ts):
    if ts.shape[0] > ts.shape[1]:
        return ts.T
    else:
        return ts

def mat_to_timeseries(f):
    timeseries = np.array(f['mat'])
    return maybe_transpose(timeseries)
