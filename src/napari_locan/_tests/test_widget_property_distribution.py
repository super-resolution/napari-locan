import napari
import pytest

from napari_locan import PropertyDistributionQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestPropertyDistributionQWidget:
    def test_PropertyDistributionQWidget_init(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = PropertyDistributionQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._loc_property_combobox.currentIndex() == -1
        viewer.close()

        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = PropertyDistributionQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._loc_property_combobox.currentIndex() == 0

        my_widget._select_button_on_click()
        viewer.close()


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_points")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show property distribution"
    )
    napari.run()
