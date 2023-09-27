import locan as lc
import pytest

from napari_locan import RenderPoints3dQWidget
from napari_locan.data_model._locdata import SmlmData


class TestRenderQWidget:
    def test_ShowPoints3dQWidget_init(self, make_napari_viewer, locdata_3d):
        viewer = make_napari_viewer()
        render_widget = RenderPoints3dQWidget(viewer)
        assert render_widget

        smlm_data = SmlmData(locdatas=[locdata_3d])
        render_widget = RenderPoints3dQWidget(viewer, smlm_data=smlm_data)
        assert render_widget._loc_properties_x_combobox.currentIndex() == 0
        assert render_widget._loc_properties_y_combobox.currentIndex() == 1
        assert render_widget._loc_properties_z_combobox.currentIndex() == 2
        assert render_widget._loc_properties_other_combobox.currentText() == ""
        assert render_widget._loc_properties_other_combobox.currentIndex() == 0

    def test_RenderQWidget(self, make_napari_viewer, locdata_3d):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[lc.LocData(), locdata_3d])

        render_widget = RenderPoints3dQWidget(viewer, smlm_data=smlm_data)

        with pytest.raises(ValueError):
            render_widget._points_button_on_click()

        smlm_data.index = 1

        render_widget._points_button_on_click()
        assert len(viewer.layers) == 1

        render_widget._loc_properties_other_combobox.setCurrentIndex(1)
        render_widget._points_button_on_click()
        assert len(viewer.layers) == 2
