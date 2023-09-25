import logging
from pathlib import Path

import locan as lc
import numpy as np
import pandas as pd
import pytest

logger = logging.getLogger(__name__)


# fixtures for LocData objects


@pytest.fixture(scope="session")
def locdata_empty():
    """
    Fixture for returning empty `LocData`.
    """
    df = pd.DataFrame()
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_single_localization():
    """
    Fixture for returning `LocData` carrying a single 2D localization.
    """
    locdata_dict = {
        "position_x": np.array([1]),
        "position_y": np.array([1]),
        "frame": np.array([1]),
        "intensity": np.array([1]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_single_localization_3d():
    """
    Fixture for returning `LocData` carrying a single 3D localization.
    """
    locdata_dict = {
        "position_x": np.array([1]),
        "position_y": np.array([1]),
        "position_z": np.array([1]),
        "frame": np.array([1]),
        "intensity": np.array([1]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_1d():
    """
    Fixture for returning `LocData` carrying 1D localizations.
    """
    locdata_dict = {
        "position_x": np.array([1, 1, 2, 3, 4, 5]),
        "frame": np.array([1, 2, 2, 4, 5, 6]),
        "intensity": np.array([100, 150, 110, 80, 105, 95]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_2d():
    """
    Fixture for returning `LocData` carrying 2D localizations.
    """
    locdata_dict = {
        "position_x": np.array([1, 1, 2, 3, 4, 5]),
        "position_y": np.array([1, 5, 3, 6, 2, 5]),
        "frame": np.array([1, 2, 2, 4, 5, 6]),
        "intensity": np.array([100, 150, 110, 80, 105, 95]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_2d_negative():
    """
    Fixture for returning `LocData` carrying 2D localizations including
    negative coordinates.
    """
    locdata_dict = {
        "position_x": np.array([1, -1, 2, 3, 4, 5]),
        "position_y": np.array([1, 5, 3, 6, -2, 5]),
        "frame": np.array([1, 2, 2, 4, 5, 6]),
        "intensity": np.array([100, 150, 110, 80, 105, 95]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_3d():
    """
    Fixture for returning `LocData` carrying 3D localizations.
    """
    locdata_dict = {
        "position_x": np.array([1, 1, 2, 3, 4, 5]),
        "position_y": np.array([1, 5, 3, 6, 2, 5]),
        "position_z": np.array([1, 2, 5, 4, 3, 2]),
        "frame": np.array([1, 2, 2, 4, 5, 6]),
        "intensity": np.array([100, 150, 110, 80, 105, 95]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_non_standard_index():
    """
    Fixture for returning `LocData` carrying 2D localizations with arbitrary
    index.
    """
    locdata_dict = {
        "position_x": np.array([1, 1, 2, 3, 4, 5]),
        "position_y": np.array([1, 5, 3, 6, 2, 5]),
        "frame": np.array([1, 2, 2, 4, 5, 6]),
        "intensity": np.array([100, 150, 110, 80, 105, 95]),
    }
    df = pd.DataFrame(locdata_dict)
    df.index = [2, 1, 5, 10, 100, 200]
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    return lc.LocData.from_dataframe(dataframe=df, meta=meta_)


@pytest.fixture(scope="session")
def locdata_blobs_2d():
    """
    Fixture for returning `LocData` carrying 2D localizations from
    five_blobs.txt.
    """
    path = Path(lc.ROOT_DIR / "tests/test_data/five_blobs.txt")
    dat = lc.load_txt_file(path)
    dat.meta.creation_time.FromSeconds(1)
    return dat


@pytest.fixture(scope="session")
def locdata_blobs_3d():
    """
    Fixture for returning `LocData` carrying 3D localizations from
    five_blobs.txt.
    """
    path = Path(lc.ROOT_DIR / "tests/test_data/five_blobs_3D.txt")
    dat = lc.load_txt_file(path)
    dat.meta.creation_time.FromSeconds(1)
    return dat


@pytest.fixture(scope="session")
def locdata_two_cluster_with_noise_2d():
    """
    Fixture for returning `LocData` carrying 2D localizations grouped in two
    clusters as indicated by `cluster_label` and noise.
    """
    points = np.array(
        [[0.5, 0.5], [1, 0.6], [1.1, 1], [5, 5.6], [5.1, 6], [5.5, 5], [100, 100]]
    )
    locdata_dict = {
        "position_x": points.T[0],
        "position_y": points.T[1],
        "cluster_label": np.array([1, 1, 1, 2, 2, 2, -1]),
    }
    df = pd.DataFrame(locdata_dict)
    meta_ = lc.data.metadata_pb2.Metadata()
    meta_.creation_time.seconds = 1
    locdata = lc.LocData.from_dataframe(dataframe=df, meta=meta_)
    locdata.region = locdata.bounding_box.region
    return locdata
