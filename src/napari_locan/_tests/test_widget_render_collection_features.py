import napari
import pytest

from napari_locan import RenderCollectionFeaturesQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestRenderCollectionFeaturesQWidget:
    def test_RenderCollectionFeaturesQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        render_widget = RenderCollectionFeaturesQWidget(viewer, smlm_data=smlm_data)
        assert render_widget

    def test_RenderCollectionFeaturesQWidget(
        self,
        make_napari_viewer,
        locdata_two_cluster_with_noise_2d,
        collection_two_cluster_2d,
    ):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(
            locdatas=[locdata_two_cluster_with_noise_2d, collection_two_cluster_2d]
        )
        smlm_data.index = 1
        my_widget = RenderCollectionFeaturesQWidget(viewer, smlm_data=smlm_data)
        my_widget._centroid_check_box.setChecked(True)
        my_widget._bounding_box_check_box.setChecked(True)
        my_widget._oriented_bounding_box_check_box.setChecked(True)
        my_widget._convex_hull_check_box.setChecked(True)
        my_widget._alpha_shape_check_box.setChecked(True)

        my_widget._render_button_on_click()
        assert len(viewer.layers) == 5
        for i in range(4):
            assert len(viewer.layers[i].data) == 2

        my_widget._translation_check_box.setChecked(True)
        my_widget._render_button_on_click()
        assert len(viewer.layers) == 10
        for i in range(5, 10):
            assert len(viewer.layers[i].data) == 2

        my_widget._translation_check_box.setChecked(False)
        my_widget._render_as_series_button_on_click()
        assert len(viewer.layers) == 15

        with pytest.raises(TypeError):
            smlm_data.index = 0
            my_widget._render_button_on_click()


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_points")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Compute cluster"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Render collection features"
    )
    napari.run()
