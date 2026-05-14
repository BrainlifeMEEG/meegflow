"""Tests for meegflow.savers module."""

import sys
import pickle
import tempfile
from pathlib import Path

import numpy as np
import pytest

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))


def _make_raw(n_channels=4, sfreq=100.0, duration=1.0):
    import mne
    n_times = int(sfreq * duration)
    data = np.random.randn(n_channels, n_times) * 1e-6
    ch_names = [f"EEG{i:03d}" for i in range(n_channels)]
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")
    return mne.io.RawArray(data, info)


class TestSaversModule:
    def test_savers_dict_keys(self):
        from meegflow.savers import SAVERS
        assert set(SAVERS.keys()) == {"fif", "pickle", "hdf5", "numpy"}

    def test_format_extensions_keys(self):
        from meegflow.savers import FORMAT_EXTENSIONS
        assert set(FORMAT_EXTENSIONS.keys()) == {"fif", "pickle", "hdf5", "numpy"}

    def test_format_extensions_values(self):
        from meegflow.savers import FORMAT_EXTENSIONS
        assert FORMAT_EXTENSIONS["fif"] == ".fif"
        assert FORMAT_EXTENSIONS["pickle"] == ".pkl"
        assert FORMAT_EXTENSIONS["hdf5"] == ".h5"
        assert FORMAT_EXTENSIONS["numpy"] == ".npy"

    def test_savers_are_callable(self):
        from meegflow.savers import SAVERS
        for fmt, fn in SAVERS.items():
            assert callable(fn), f"SAVERS['{fmt}'] is not callable"


class TestSaveFif:
    def test_saves_raw_to_fif(self):
        from meegflow.savers import _save_fif
        import mne
        raw = _make_raw()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test_raw.fif"
            _save_fif(raw, path, overwrite=True)
            assert path.exists()
            loaded = mne.io.read_raw_fif(path, preload=True, verbose=False)
            assert loaded.info["nchan"] == raw.info["nchan"]

    def test_overwrite_false_raises(self):
        from meegflow.savers import _save_fif
        raw = _make_raw()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test_raw.fif"
            _save_fif(raw, path, overwrite=True)
            with pytest.raises(FileExistsError):
                _save_fif(raw, path, overwrite=False)


class TestSavePickle:
    def test_saves_arbitrary_object(self):
        from meegflow.savers import _save_pickle
        obj = {"key": [1, 2, 3], "nested": {"a": True}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.pkl"
            _save_pickle(obj, path, overwrite=True)
            assert path.exists()
            with open(path, "rb") as f:
                loaded = pickle.load(f)
            assert loaded == obj

    def test_overwrite_false_raises(self):
        from meegflow.savers import _save_pickle
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.pkl"
            _save_pickle({}, path, overwrite=True)
            with pytest.raises(FileExistsError):
                _save_pickle({}, path, overwrite=False)


class TestSaveNumpy:
    def test_saves_array_directly(self):
        from meegflow.savers import _save_numpy
        arr = np.random.randn(3, 100)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.npy"
            _save_numpy(arr, path, overwrite=True)
            assert path.exists()
            loaded = np.load(path)
            np.testing.assert_array_equal(loaded, arr)

    def test_saves_mne_object_via_get_data(self):
        from meegflow.savers import _save_numpy
        raw = _make_raw(n_channels=3)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.npy"
            _save_numpy(raw, path, overwrite=True)
            assert path.exists()
            loaded = np.load(path)
            np.testing.assert_array_almost_equal(loaded, raw.get_data())

    def test_overwrite_false_raises(self):
        from meegflow.savers import _save_numpy
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.npy"
            _save_numpy(np.zeros(5), path, overwrite=True)
            with pytest.raises(FileExistsError):
                _save_numpy(np.zeros(5), path, overwrite=False)


class TestSaveHdf5:
    def test_saves_raw_via_h5py(self):
        """BaseRaw goes through h5py (MNE Raw.save() does not support .h5)."""
        import h5py
        from meegflow.savers import _save_hdf5
        raw = _make_raw()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data_raw.h5"
            _save_hdf5(raw, path, overwrite=True)
            assert path.exists()
            with h5py.File(path, "r") as f:
                assert "data" in f
                np.testing.assert_array_almost_equal(f["data"][:], raw.get_data())

    def test_saves_arbitrary_object_via_h5py(self):
        import h5py
        from meegflow.savers import _save_hdf5

        class FakeObj:
            def get_data(self):
                return np.random.randn(2, 50)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.h5"
            _save_hdf5(FakeObj(), path, overwrite=True)
            assert path.exists()
            with h5py.File(path, "r") as f:
                assert "data" in f

    def test_overwrite_false_raises(self):
        from meegflow.savers import _save_hdf5

        class FakeObj:
            def get_data(self):
                return np.zeros((2, 10))

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.h5"
            _save_hdf5(FakeObj(), path, overwrite=True)
            with pytest.raises(FileExistsError):
                _save_hdf5(FakeObj(), path, overwrite=False)
