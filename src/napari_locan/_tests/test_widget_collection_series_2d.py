import locan as lc

from napari_locan import CollectionSeriesQWidget
from napari_locan.data_model._locdata import SmlmData


class TestCollectionSeriesQWidget:
    def test_CollectionSeriesQWidget_init(
        self, make_napari_viewer, locdata_two_cluster_with_noise_2d
    ):
        viewer = make_napari_viewer()
        collection_series_widget = CollectionSeriesQWidget(viewer)
        assert collection_series_widget

        smlm_data = SmlmData(locdatas=[locdata_two_cluster_with_noise_2d])
        collection_series_widget = CollectionSeriesQWidget(viewer, smlm_data=smlm_data)
        assert collection_series_widget

        smlm_data = SmlmData(locdatas=[locdata_two_cluster_with_noise_2d])
        sel_1 = lc.LocData.from_selection(
            locdata=locdata_two_cluster_with_noise_2d, indices=[0, 1, 2]
        )
        sel_2 = lc.LocData.from_selection(
            locdata=locdata_two_cluster_with_noise_2d, indices=[3, 4, 5]
        )
        collection = lc.LocData.concat([sel_1, sel_2])
        smlm_data.append_locdata(locdata=collection)

        collection_series_widget = CollectionSeriesQWidget(viewer, smlm_data=smlm_data)
        assert collection_series_widget._loc_properties_x_combobox.currentIndex() == 0
        assert collection_series_widget._loc_properties_y_combobox.currentIndex() == 1
        assert (
            collection_series_widget._loc_properties_other_combobox.currentText() == ""
        )
        assert (
            collection_series_widget._loc_properties_other_combobox.currentIndex() == 0
        )

    def test_CollectionSeriesQWidget_features(
        self, make_napari_viewer, locdata_two_cluster_with_noise_2d
    ):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[locdata_two_cluster_with_noise_2d])
        sel_1 = lc.LocData.from_selection(
            locdata=locdata_two_cluster_with_noise_2d, indices=[0, 1, 2]
        )
        sel_2 = lc.LocData.from_selection(
            locdata=locdata_two_cluster_with_noise_2d, indices=[3, 4, 5]
        )
        collection = lc.LocData.concat([sel_1, sel_2])
        smlm_data.append_locdata(locdata=collection)

        collection_series_widget = CollectionSeriesQWidget(viewer, smlm_data=smlm_data)
        collection_series_widget._points_button_on_click()
        assert len(viewer.layers) == 1

        collection_series_widget._loc_properties_other_combobox.setCurrentIndex(1)
        collection_series_widget._points_button_on_click()
        assert len(viewer.layers) == 2

        collection_series_widget._loc_properties_other_combobox.setCurrentIndex(0)
        collection_series_widget._translation_check_box.setChecked(True)
        collection_series_widget._points_button_on_click()
        assert len(viewer.layers) == 3
