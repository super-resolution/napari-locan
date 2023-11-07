import warnings

import locan as lc
import pytest

from napari_locan.data_model.data_model_base import DataModel


class TestDataModel:
    def test_init(self):
        data_model = DataModel()
        assert isinstance(data_model, DataModel)
        assert data_model.datasets == []
        assert data_model.names == []
        assert data_model.index == -1
        assert data_model.dataset is None
        assert data_model.name == ""

        data_model = DataModel(datasets=[1, 2])
        assert len(data_model.datasets) == 2
        assert len(data_model.names) == 2
        assert data_model.index == 1
        assert isinstance(data_model.dataset, int)
        assert isinstance(data_model.name, str)
        assert data_model.name == "1"

        data_model = DataModel(datasets=[1, 2], names=["1", "2"])
        assert len(data_model.datasets) == 2
        assert len(data_model.names) == 2
        assert data_model.index == 1
        assert isinstance(data_model.dataset, int)
        assert isinstance(data_model.name, str)
        assert data_model.name == "2"

    def test_index(self):
        data_model = DataModel(datasets=[1, 2])
        assert data_model.index == 1
        assert data_model.dataset is data_model.datasets[data_model.index]

        data_model.index = 0
        assert data_model.index == 0
        assert data_model.dataset is data_model.datasets[data_model.index]

        with pytest.raises(IndexError):
            data_model.index = 3

        data_model.index = -1
        assert data_model.index == -1
        assert data_model.dataset is None
        assert data_model.name == ""

    def test_name(self):
        data_model = DataModel(datasets=[1, 2])
        data_model.index = 0
        data_model.name += "_1"
        data_model.index = 1
        data_model.name += "_2"
        assert data_model.names == ["0_1", "1_2"]
        with pytest.raises(AttributeError):
            data_model.names = []
        data_model.names[1] = "other name"
        assert data_model.names == ["0_1", "other name"]

    def test_delete_item(self):
        data_model = DataModel(datasets=[1, 2])
        data_model.delete_item()
        assert len(data_model.datasets) == 1
        assert data_model.names == ["0"]

        data_model.delete_all()
        assert data_model.index == -1
        assert data_model.datasets == []
        assert data_model.names == []

        # delete on empty container
        data_model.delete_all()
        assert data_model.index == -1
        assert data_model.datasets == []
        assert data_model.names == []

    def test_append_item(self):
        data_model = DataModel()
        assert data_model.index == -1
        data_model.append_item(dataset=lc.LocData(), name="1")
        assert data_model.index == 0
        assert len(data_model.datasets) == 1
        assert data_model.names == ["1"]

        data_model.append_item(dataset=lc.LocData(), name="2")
        assert data_model.index == 1
        assert len(data_model.datasets) == 2
        assert data_model.names == ["1", "2"]

    def test_connect(self):
        def names_slot(locdata_names):
            warnings.warn("Name changed.", stacklevel=1)

        def index_slot(index):
            warnings.warn("index changed - is not -1.", stacklevel=1)

        data_model = DataModel(datasets=[1, 2])
        data_model.names_changed_signal.connect(names_slot)
        data_model.index_changed_signal.connect(index_slot)

        with pytest.warns():
            data_model.index = 0
        with pytest.warns():
            data_model.name = "other name"
        with pytest.warns():
            data_model.append_item(dataset=3, name="3")
        with pytest.warns():
            data_model.append_item(dataset=4)
