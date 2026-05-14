"""Format-specific save helpers for MEEGFlow pipeline output."""

from __future__ import annotations

import pickle
from pathlib import Path

import mne
import numpy as np


def _save_fif(obj, path, overwrite):
    """Save an MNE object using its native ``.save()`` method (produces a .fif file)."""
    obj.save(path, overwrite=overwrite)


def _save_pickle(obj, path, overwrite):
    """Serialize any Python object to disk with ``pickle``."""
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def _save_hdf5(obj, path, overwrite):
    """Save to HDF5: uses MNE's native .save() for Raw/Epochs, h5py otherwise."""
    # MNE Raw and Epochs support .h5 natively via save()
    if isinstance(obj, (mne.BaseRaw, mne.BaseEpochs)):
        obj.save(path, overwrite=overwrite)
    else:
        try:
            import h5py
        except ImportError:
            raise ImportError("h5py is required for hdf5 format: pip install h5py")
        path = Path(path)
        if path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {path}")
        with h5py.File(path, 'w') as f:
            data = obj.get_data() if hasattr(obj, 'get_data') else np.asarray(obj)
            f.create_dataset('data', data=data)


def _save_numpy(obj, path, overwrite):
    """Save the raw data array to a ``.npy`` file via ``numpy.save``."""
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")
    data = obj.get_data() if hasattr(obj, 'get_data') else np.asarray(obj)
    np.save(path, data)


SAVERS = {
    'fif':    _save_fif,
    'pickle': _save_pickle,
    'hdf5':   _save_hdf5,
    'numpy':  _save_numpy,
}

FORMAT_EXTENSIONS = {
    'fif':    '.fif',
    'pickle': '.pkl',
    'hdf5':   '.h5',
    'numpy':  '.npy',
}
