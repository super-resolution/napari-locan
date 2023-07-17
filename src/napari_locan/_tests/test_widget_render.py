from napari_locan import RenderQWidget
from napari_locan._locdata import SmlmData


class TestRenderQWidget:
    def test_RenderQWidget(self, make_napari_viewer, locdata_2d):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        render_widget = RenderQWidget(viewer, smlm_data=smlm_data)

        render_widget._render_button_on_click()
        assert len(viewer.layers) == 1
