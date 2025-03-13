import locan as lc
import napari
import pytest

from napari_locan import SaveSmlmDataQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestSaveSmlmDataQWidget:
    def test_SaveSmlmDataQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = SaveSmlmDataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._file_path_edit.text() == ""

    def test_SaveSmlmDataQWidget_save(self, make_napari_viewer, locdata_2d, tmp_path):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[lc.LocData(), locdata_2d])
        my_widget = SaveSmlmDataQWidget(viewer, smlm_data=smlm_data)

        test_file_path = tmp_path / "test.asdf"
        my_widget._file_path_edit.setText(str(test_file_path))
        my_widget._file_type_combobox.setCurrentText(lc.FileType.ASDF.name)
        assert my_widget._file_type_combobox.currentText() == "ASDF"
        # my_widget._kwargs_edit.setText("")

        smlm_data.index = 0
        my_widget._save_button_on_click()
        assert test_file_path.exists()

        smlm_data.index = 1
        my_widget._save_button_on_click()
        assert test_file_path.exists()

        test_file_path = tmp_path / "test.csv"
        my_widget._file_path_edit.setText(str(test_file_path))
        my_widget._file_type_combobox.setCurrentText(lc.FileType.THUNDERSTORM.name)
        assert my_widget._file_type_combobox.currentText() == "THUNDERSTORM"
        smlm_data.index = 1
        my_widget._save_button_on_click()
        assert test_file_path.exists()

        test_file_path = tmp_path / "test.zip"
        my_widget._file_path_edit.setText(str(test_file_path))
        my_widget._file_type_combobox.setCurrentText(lc.FileType.SMLM.name)
        assert my_widget._file_type_combobox.currentText() == "SMLM"
        smlm_data.index = 1
        my_widget._save_button_on_click()
        assert test_file_path.exists()

        test_file_path = tmp_path / "test.csv"
        my_widget._file_path_edit.setText(str(test_file_path))
        my_widget._file_type_combobox.setCurrentText(lc.FileType.SMAP.name)
        assert my_widget._file_type_combobox.currentText() == "SMAP"
        smlm_data.index = 1
        my_widget._save_button_on_click()
        assert test_file_path.exists()

        my_widget._file_path_delete_button_on_click()
        assert my_widget._file_path_edit.text() == ""


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
    viewer.window.add_plugin_dock_widget(plugin_name="napari-locan", widget_name="Save")
    napari.run()
