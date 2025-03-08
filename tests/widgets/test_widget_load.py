from pathlib import Path

import locan as lc
import napari
import pytest

from napari_locan import LoadQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestLoadQWidget:
    def test_LoadQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = LoadQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._file_path_edit.text() == ""

    @pytest.mark.skip("needs user interaction")
    def test_LoadQWidget_load(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = LoadQWidget(viewer, smlm_data=smlm_data)

        locan_test_data = Path(__file__).resolve().parents / "npc_gp210.asdf"

        my_widget._file_path_edit.insert(str(locan_test_data))
        my_widget._file_type_combobox.setCurrentIndex(lc.FileType.ASDF.value)

        my_widget._kwargs_edit.setText("nrows=10")

        my_widget._load_button_on_click()
        assert Path(smlm_data.locdata.meta.file.path) == locan_test_data

        my_widget._file_path_select_button_on_click()
        assert Path(smlm_data.locdata.meta.file.path)

        my_widget._file_path_delete_button_on_click()
        assert my_widget._file_path_edit.text() == ""


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_image")
    viewer.add_shapes(data=None, text="ROI shapes")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    viewer.window.add_plugin_dock_widget(plugin_name="napari-locan", widget_name="Load")
    napari.run()
