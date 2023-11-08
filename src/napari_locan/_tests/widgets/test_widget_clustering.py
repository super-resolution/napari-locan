from napari_locan import ClusteringQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestClusteringQWidgetQWidget:
    def test_ClusteringQWidget_init(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = ClusteringQWidget(viewer, smlm_data=smlm_data)
        assert my_widget

        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = ClusteringQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._cluster_method_combobox.currentText() == "DBSCAN"
        assert my_widget._loc_properties_x_combobox.currentText() == "position_x"
        assert my_widget._loc_properties_y_combobox.currentText() == "position_y"
        assert my_widget._eps_spin_box.value() == 20
        assert my_widget._min_points_spin_box.value() == 3

    def test_ClusteringQWidget_compute_button_worker(
        self, make_napari_viewer, locdata_2d
    ):
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = ClusteringQWidget(viewer, smlm_data=smlm_data)

        my_widget._compute_button_on_click_main_thread()
        assert len(smlm_data.locdatas) == 3
        assert (
            "'eps': 20, 'min_samples': 3" in smlm_data.locdata.meta.history[0].parameter
        )
        assert my_widget._eps_spin_box.value() == 20
        assert my_widget._min_points_spin_box.value() == 3
        assert isinstance(smlm_data.locdata.references, list)
        assert smlm_data.index == 2
        assert smlm_data.locdata_name.endswith("cluster")

        smlm_data.index = 0
        my_widget._compute_button_on_click_thread_worker()
        # you would have to wait for worker.finished() to assert - so we skip this:
        # assert len(smlm_data.locdatas) == 5
