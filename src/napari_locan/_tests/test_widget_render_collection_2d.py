import napari
import pytest

from napari_locan import RenderCollection2dQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestCollectionSeriesQWidget:
    def test_CollectionSeriesQWidget_init(
        self,
        make_napari_viewer,
        locdata_two_cluster_with_noise_2d,
        collection_two_cluster_2d,
    ):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        collection_series_widget = RenderCollection2dQWidget(
            viewer, smlm_data=smlm_data
        )
        assert collection_series_widget

        smlm_data = SmlmData(locdatas=[locdata_two_cluster_with_noise_2d])
        collection_series_widget = RenderCollection2dQWidget(
            viewer, smlm_data=smlm_data
        )
        assert collection_series_widget

        smlm_data = SmlmData(
            locdatas=[locdata_two_cluster_with_noise_2d, collection_two_cluster_2d]
        )
        smlm_data.index = 1

        collection_series_widget = RenderCollection2dQWidget(
            viewer, smlm_data=smlm_data
        )
        assert collection_series_widget._loc_properties_x_combobox.currentIndex() == 0
        assert collection_series_widget._loc_properties_y_combobox.currentIndex() == 1
        assert (
            collection_series_widget._loc_properties_other_combobox.currentText() == ""
        )
        assert (
            collection_series_widget._loc_properties_other_combobox.currentIndex() == 0
        )

    def test_CollectionSeriesQWidget_features(
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
        collection_series_widget = RenderCollection2dQWidget(
            viewer, smlm_data=smlm_data
        )
        collection_series_widget._render_points_as_series_button_on_click()
        assert len(viewer.layers) == 1

        collection_series_widget._loc_properties_other_combobox.setCurrentIndex(1)
        collection_series_widget._render_points_as_series_button_on_click()
        assert len(viewer.layers) == 2

        collection_series_widget._loc_properties_other_combobox.setCurrentIndex(0)
        collection_series_widget._translation_check_box.setChecked(True)
        collection_series_widget._render_points_as_series_button_on_click()
        assert len(viewer.layers) == 3

        collection_series_widget._loc_properties_other_combobox.setCurrentIndex(0)
        collection_series_widget._render_points_button_on_click()
        assert len(viewer.layers) == 4

        assert len(collection_series_widget.smlm_data.locdatas) == 2
        collection_series_widget._concatenate_button_on_click()
        assert len(collection_series_widget.smlm_data.locdatas) == 3


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
        plugin_name="napari-locan", widget_name="Render collection 2d"
    )
    napari.run()
