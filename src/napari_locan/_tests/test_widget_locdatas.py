import locan as lc
import pytest

from napari_locan import LocdatasQWidget
from napari_locan._locdata import SmlmData


class TestLocdatasQWidget:
    def test_LocdatasQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = LocdatasQWidget(viewer, smlm_data=smlm_data)
        assert not my_widget._locdatas_combobox.isEditable()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""

    def test_LocdatasQWidget_changing_locdatas(self, make_napari_viewer):
        smlm_data = SmlmData()
        locdata_0, locdata_1 = lc.LocData(), lc.LocData()
        smlm_data.locdatas = [locdata_0, locdata_1]
        viewer = make_napari_viewer()
        my_widget = LocdatasQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""

        my_widget._locdatas_combobox.setCurrentIndex(1)
        assert my_widget._locdatas_combobox.currentIndex() == 1
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.index == 1

        smlm_data.locdatas = []
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""

    def test_LocdatasQWidget_buttons(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = LocdatasQWidget(viewer, smlm_data=smlm_data)

        with pytest.raises(KeyError):
            my_widget._delete_button_on_click()

        locdata_0, locdata_1 = lc.LocData(), lc.LocData()
        smlm_data.locdatas = [locdata_0, locdata_1]
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.locdatas == [locdata_0, locdata_1]

        my_widget._delete_button_on_click()
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.locdatas == [locdata_1]

        my_widget._delete_button_on_click()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""
        assert smlm_data.locdatas == []
