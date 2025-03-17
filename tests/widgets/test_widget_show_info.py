import locan as lc
import napari
import pytest

from napari_locan import ShowInfoQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestShowInfoQWidget:
    def test_ShowInfoQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = ShowInfoQWidget(viewer, smlm_data=smlm_data)

        assert my_widget._information_collection_checkbox.isChecked() is False
        assert my_widget._information_selection_checkbox.isChecked() is False
        assert my_widget._information_coordinate_dimension_text_edit.text() == ""
        assert my_widget._information_localization_count_text_edit.text() == ""

    def test_ShowInfoQWidget_with_locdata(
        self, make_napari_viewer, locdata_2d, locdata_3d
    ):
        smlm_data = SmlmData(locdatas=[lc.LocData(), locdata_2d, locdata_3d])
        viewer = make_napari_viewer()
        my_widget = ShowInfoQWidget(viewer, smlm_data=smlm_data)

        smlm_data.index = 0
        assert my_widget._information_collection_checkbox.isChecked() is False
        assert my_widget._information_selection_checkbox.isChecked() is False
        assert my_widget._information_coordinate_dimension_text_edit.text() == "0"
        assert my_widget._information_localization_count_text_edit.text() == "0"

        smlm_data.index = 1
        assert my_widget._information_collection_checkbox.isChecked() is False
        assert my_widget._information_selection_checkbox.isChecked() is False
        assert my_widget._information_coordinate_dimension_text_edit.text() == "2"
        assert my_widget._information_localization_count_text_edit.text() == "6"

        smlm_data.index = 2
        assert my_widget._information_collection_checkbox.isChecked() is False
        assert my_widget._information_selection_checkbox.isChecked() is False
        assert my_widget._information_coordinate_dimension_text_edit.text() == "3"
        assert my_widget._information_localization_count_text_edit.text() == "6"


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_points")
    viewer.open_sample("napari-locan", "npc_points")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show information"
    )
    napari.run()
