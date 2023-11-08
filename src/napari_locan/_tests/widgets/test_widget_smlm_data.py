import locan as lc
import napari
import pytest

from napari_locan import SmlmDataQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestSmlmDataQWidget:
    def test_SmlmDataQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)
        assert not my_widget._locdatas_combobox.isEditable()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""

        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._locdatas_combobox.currentIndex() == 1
        assert my_widget._locdatas_combobox.currentText() != ""

        smlm_data.delete_all()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""

    def test_SmlmDataQWidget_changing_locdatas(self, make_napari_viewer):
        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._locdatas_combobox.currentIndex() == 1
        assert my_widget._locdatas_combobox.currentText() != ""

        my_widget._locdatas_combobox.setCurrentIndex(0)
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.index == 0

        smlm_data.delete_all()
        assert len(smlm_data.locdatas) == 0
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""
        assert smlm_data.index == -1

        smlm_data.append_item(locdata=lc.LocData())
        assert len(smlm_data.locdatas) == 1
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.index == 0

        smlm_data.append_item(locdata=lc.LocData(), set_index=False)
        assert len(smlm_data.locdatas) == 2
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.index == 0

        smlm_data.append_item(locdata=lc.LocData())
        assert len(smlm_data.locdatas) == 3
        assert my_widget._locdatas_combobox.currentIndex() == 2
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.index == 2

    def test_SmlmDataQWidget_delete_button(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)

        with pytest.raises(IndexError):
            my_widget._delete_button_on_click()

        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)

        my_widget._delete_button_on_click()
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
        assert smlm_data.locdata_names == ["1"]

        my_widget._delete_button_on_click()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""
        assert smlm_data.locdatas == []

    @pytest.mark.skip("Needs user interaction")
    def test_SmlmDataQWidget_delete_all_button(self, make_napari_viewer):
        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)

        my_widget._delete_all_button_on_click()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""
        assert smlm_data.locdatas == []

    @pytest.mark.skip("Needs user interaction")
    def test_SmlmDataQWidget_save_button(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)

        with pytest.raises(KeyError):
            my_widget._save_button_on_click()

        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        viewer = make_napari_viewer()
        my_widget = SmlmDataQWidget(viewer, smlm_data=smlm_data)
        my_widget._locdatas_combobox.setCurrentIndex(0)
        my_widget._save_button_on_click()
        my_widget._locdatas_combobox.setCurrentIndex(1)
        my_widget._save_button_on_click()


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_points")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    napari.run()
