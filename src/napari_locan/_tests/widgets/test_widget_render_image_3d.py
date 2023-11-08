import locan as lc
import napari
import pytest

from napari_locan import RenderImage3dQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestRenderImage3dQWidget:
    def test_RenderImage3dQWidget_init(self, make_napari_viewer, locdata_3d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        render_widget = RenderImage3dQWidget(viewer, smlm_data=smlm_data)
        assert render_widget

        smlm_data = SmlmData(locdatas=[locdata_3d])
        render_widget = RenderImage3dQWidget(viewer, smlm_data=smlm_data)
        assert render_widget._loc_properties_x_combobox.currentIndex() == 0
        assert render_widget._loc_properties_y_combobox.currentIndex() == 1
        assert render_widget._loc_properties_z_combobox.currentIndex() == 2
        assert render_widget._loc_properties_other_combobox.currentText() == ""
        assert render_widget._loc_properties_other_combobox.currentIndex() == 0

    def test_RenderImage3dQWidget(self, make_napari_viewer, locdata_3d):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[lc.LocData(), locdata_3d])

        render_widget = RenderImage3dQWidget(viewer, smlm_data=smlm_data)
        render_widget._render_button_on_click()

        smlm_data.index = 1
        render_widget._render_button_on_click()
        assert len(viewer.layers) == 2

        render_widget._loc_properties_other_combobox.setCurrentIndex(1)
        render_widget._rescale_combobox.setCurrentIndex(0)
        render_widget._render_button_on_click()
        assert len(viewer.layers) == 3


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    # todo: add 3d sample data
    # viewer.open_sample("napari-locan", "tubulin_image")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    viewer.window.add_plugin_dock_widget(plugin_name="napari-locan", widget_name="Load")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Render image 3d"
    )
    napari.run()
