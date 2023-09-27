import warnings

import locan as lc
import pytest

from napari_locan.data_model._locdata import SmlmData


class TestLocdatas:
    def test_init(self):
        smlm_data = SmlmData()
        assert smlm_data.locdatas == []
        assert smlm_data.locdata_names == []
        assert smlm_data.index == -1
        assert smlm_data.locdata is None
        assert smlm_data.locdata_name == ""

        smlm_data.locdatas = [lc.LocData(), lc.LocData()]
        assert len(smlm_data.locdatas) == 2
        assert len(smlm_data.locdata_names) == 2
        assert smlm_data.index == 0
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

        smlm_data = SmlmData(locdatas=[lc.LocData(), lc.LocData()])
        assert len(smlm_data.locdatas) == 2
        assert len(smlm_data.locdata_names) == 2
        assert smlm_data.index == 0
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

    def test_index(self):
        smlm_data = SmlmData()
        smlm_data.locdatas = [lc.LocData(), lc.LocData()]
        assert smlm_data.index == 0
        assert smlm_data.locdata is smlm_data.locdatas[smlm_data.index]

        smlm_data.index = 1
        assert smlm_data.index == 1
        assert smlm_data.locdata is smlm_data.locdatas[smlm_data.index]

        with pytest.raises(IndexError):
            smlm_data.index = 3

        smlm_data.index = -1
        assert smlm_data.index == -1
        assert smlm_data.locdata is None

    def test_append_locdata(self):
        smlm_data = SmlmData()
        smlm_data.append_locdata(locdata=lc.LocData())
        smlm_data.append_locdata(locdata=lc.LocData())
        assert len(smlm_data.locdatas) == 2
        assert len(smlm_data.locdata_names) == 2
        assert smlm_data.index == 1
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

    def test_connect(self):
        def locdatas_slot(locdatas):
            if locdatas != []:
                warnings.warn("smlm_data not empty.", stacklevel=1)

        def index_slot(index):
            if index != -1:
                warnings.warn("index not -1.", stacklevel=1)

        smlm_data = SmlmData()
        smlm_data.locdatas_signal.connect(locdatas_slot)
        smlm_data.index_signal.connect(index_slot)

        smlm_data.locdatas = []
        assert smlm_data.locdatas == []
        assert smlm_data.locdata_names == []
        assert smlm_data.index == -1
        assert smlm_data.locdata is None
        assert smlm_data.locdata_name == ""

        with pytest.warns():
            smlm_data.locdatas = [lc.LocData(), lc.LocData()]
        assert len(smlm_data.locdatas) == 2
        assert len(smlm_data.locdata_names) == 2
        assert smlm_data.index == 0
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

    def test_change(self):
        smlm_data = SmlmData()
        assert smlm_data.locdatas == []
        assert smlm_data.locdata_names == []
        assert smlm_data.index == -1
        assert smlm_data.locdata is None
        assert smlm_data.locdata_name == ""

        smlm_data.locdatas = [lc.LocData(), lc.LocData()]
        assert len(smlm_data.locdatas) == 2
        assert len(smlm_data.locdata_names) == 2
        assert smlm_data.index == 0
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

        smlm_data.locdatas = smlm_data.locdatas[:1]
        assert len(smlm_data.locdatas) == 1
        assert len(smlm_data.locdata_names) == 1
        assert smlm_data.index == 0
        assert isinstance(smlm_data.locdata, lc.LocData)
        assert isinstance(smlm_data.locdata_name, str)

        smlm_data.locdatas = None
        assert len(smlm_data.locdatas) == 0
        assert len(smlm_data.locdata_names) == 0
        assert smlm_data.index == -1
        assert smlm_data.locdata is None
        assert smlm_data.locdata_name == ""
