import warnings

import locan as lc
import pytest

from napari_locan.data_model.smlm_data import SmlmData


class TestSmlmData:
    def test_init(self):
        smlm_data = SmlmData()
        assert smlm_data.locdatas == []
        assert smlm_data.locdata_names == []
        assert smlm_data.index == -1
        assert smlm_data.locdata is None
        assert smlm_data.locdata_name == ""

        smlm_data = SmlmData(locdatas=[lc.LocData(), lc.LocData()])
        assert len(smlm_data.locdatas) == 2
        assert len(smlm_data.locdata_names) == 2
        assert smlm_data.index == 1
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["name_1", "name_2"]
        )
        assert len(smlm_data.locdatas) == 2
        assert smlm_data.locdata_names == ["name_1", "name_2"]
        assert smlm_data.index == 1
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert smlm_data.locdata_name == "name_2"

    def test_index(self):
        smlm_data = SmlmData(locdatas=[lc.LocData(), lc.LocData()])
        assert smlm_data.index == 1
        assert smlm_data.locdata is smlm_data.locdatas[smlm_data.index]

        smlm_data.index = 0
        assert smlm_data.index == 0
        assert smlm_data.locdata is smlm_data.locdatas[smlm_data.index]

        with pytest.raises(IndexError):
            smlm_data.index = 3

        smlm_data.index = -1
        assert smlm_data.index == -1
        assert smlm_data.locdata is None
        assert smlm_data.locdata_name == ""

    def test_locdata_name(self):
        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["name", "name"]
        )
        smlm_data.index = 0
        smlm_data.locdata_name += "_1"
        smlm_data.index = 1
        smlm_data.locdata_name += "_2"
        assert smlm_data.locdata_names == ["name_1", "name_2"]
        smlm_data.locdata_names[1] = "other name"
        assert smlm_data.locdata_names == ["name_1", "other name"]

    def test_delete_item(self):
        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        smlm_data.delete_item()
        assert len(smlm_data.locdatas) == 1
        assert smlm_data.locdata_names == ["1"]

        smlm_data.delete_all()
        assert smlm_data.index == -1
        assert smlm_data.locdatas == []
        assert smlm_data.locdata_names == []

        # delete on empty container
        smlm_data.delete_all()
        assert smlm_data.index == -1
        assert smlm_data.locdatas == []
        assert smlm_data.locdata_names == []

    def test_append_item(self):
        smlm_data = SmlmData()
        assert smlm_data.index == -1
        smlm_data.append_item(locdata=lc.LocData(), locdata_name="1")
        assert smlm_data.index == 0
        assert len(smlm_data.locdatas) == 1
        assert smlm_data.locdata_names == ["1"]

        smlm_data.append_item(locdata=lc.LocData(), locdata_name="2")
        assert smlm_data.index == 1
        assert len(smlm_data.locdatas) == 2
        assert smlm_data.locdata_names == ["1", "2"]

    def test_connect(self):
        def locdata_names_slot(locdata_names):
            warnings.warn("Name changed.", stacklevel=1)

        def index_slot(index):
            warnings.warn("index changed - is not -1.", stacklevel=1)

        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        smlm_data.locdata_names_changed_signal.connect(locdata_names_slot)
        smlm_data.index_changed_signal.connect(index_slot)

        with pytest.warns():
            smlm_data.index = 0

        with pytest.warns():
            smlm_data.locdata_name = "other name"
