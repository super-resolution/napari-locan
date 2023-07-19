from napari_locan import ShowFeaturesQWidget
from napari_locan.data_model._locdata import SmlmData


class TestShowFeaturesQWidget:
    def test_ShowFeaturesQWidget(self, make_napari_viewer, locdata_2d):
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        features_widget = ShowFeaturesQWidget(viewer, smlm_data=smlm_data)
        features_widget._centroid_check_box.setChecked(True)
        features_widget._bounding_box_check_box.setChecked(True)
        features_widget._oriented_bounding_box_check_box.setChecked(True)
        features_widget._convex_hull_check_box.setChecked(True)
        features_widget._alpha_shape_check_box.setChecked(True)

        features_widget._render_button_on_click()
        assert len(viewer.layers) == 5
        for i in range(4):
            assert len(viewer.layers[i].data) == 1
