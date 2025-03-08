import warnings

import locan as lc
import pytest

from napari_locan.data_model.data_model_base import DataModel
from napari_locan.data_model.roi_specifications import RoiSpecifications


class TestRoiSpecifications:
    def test_init(self):
        roi_specs = RoiSpecifications()
        assert isinstance(roi_specs, DataModel)
        assert roi_specs.datasets == []
        assert roi_specs.names == []
        assert roi_specs.index == -1
        assert roi_specs.dataset is None
        assert roi_specs.name == ""

        roi_specs = RoiSpecifications(
            datasets=[lc.Roi(region=lc.Rectangle()), lc.Roi(region=lc.Rectangle())],
            names=["1", "2"],
        )
        assert len(roi_specs.datasets) == 2
        assert len(roi_specs.names) == 2
        assert roi_specs.index == 1
        assert isinstance(roi_specs.dataset, lc.Roi)
        assert isinstance(roi_specs.name, str)
        assert roi_specs.name == "2"

    def test_connect(self):
        def names_slot(locdata_names):
            warnings.warn("Name changed.", stacklevel=1)

        def index_slot(index):
            warnings.warn("index changed - is not -1.", stacklevel=1)

        roi_specs = RoiSpecifications(
            datasets=[lc.Roi(region=lc.Rectangle()), lc.Roi(region=lc.Rectangle())],
            names=["1", "2"],
        )
        roi_specs.names_changed_signal.connect(names_slot)
        roi_specs.index_changed_signal.connect(index_slot)

        with pytest.warns():
            roi_specs.index = 0
        with pytest.warns():
            roi_specs.name = "other name"
        with pytest.warns():
            roi_specs.append_item(dataset=lc.Roi(region=lc.Rectangle()), name="3")
