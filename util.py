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

def _find_files(files, exts, src, root, paths, names, subdirs):
    for f in files:
        for ext in exts:
            if f.endswith(ext):
                p = os.path.join(root, f)
                paths.append(p)
                names.append(f)
                subdirs.append(os.path.dirname(p.split(src)[1]).lstrip(os.path.sep))
                break

def find_files(p, exts, rec=False):
    exts = list(exts)
    paths = []
    names = []
    subdirs = []
    if rec:
        for root, dirs, files in os.walk(p):
            _find_files(files, exts, p, root, paths, names, subdirs)
    else:
        _find_files(os.listdir(p), exts, p, p, paths, names, subdirs)
    return paths, names, subdirs