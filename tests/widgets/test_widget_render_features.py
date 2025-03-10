from copy import copy

import pytest

from napari_locan import RenderFeaturesQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestShowFeaturesQWidget:
    def test_ShowFeaturesQWidget_init(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        render_widget = RenderFeaturesQWidget(viewer, smlm_data=smlm_data)
        assert render_widget

        locdata_2d = copy(locdata_2d)
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        features_widget = RenderFeaturesQWidget(viewer, smlm_data=smlm_data)
        features_widget._centroid_check_box.setChecked(True)
        features_widget._bounding_box_check_box.setChecked(True)
        features_widget._oriented_bounding_box_check_box.setChecked(True)
        features_widget._convex_hull_check_box.setChecked(True)
        features_widget._alpha_shape_check_box.setChecked(True)

        features_widget._render_button_on_click()
        assert len(viewer.layers) == 5
        for i in range(4):
            assert len(viewer.layers[i].data) == 1

    @pytest.mark.parametrize(
        "fixture_name, expected",
        [
            ("locdata_empty", 0),
            ("locdata_single_localization", 0),
            ("locdata_non_standard_index", 0),
        ],
    )
    def test_ShowFeaturesQWidget_standard_data(
        self,
        make_napari_viewer,
        locdata_empty,
        locdata_single_localization,
        locdata_non_standard_index,
        fixture_name,
        expected,
    ):
        locdata = eval(fixture_name)  # noqa: S307
        viewer = make_napari_viewer()
        smlm_data = SmlmData(locdatas=[locdata])
        features_widget = RenderFeaturesQWidget(viewer, smlm_data=smlm_data)
        features_widget._centroid_check_box.setChecked(True)
        features_widget._bounding_box_check_box.setChecked(True)
        features_widget._oriented_bounding_box_check_box.setChecked(True)
        features_widget._convex_hull_check_box.setChecked(True)
        features_widget._alpha_shape_check_box.setChecked(True)

        if fixture_name in ["locdata_empty", "locdata_single_localization"]:
            with pytest.raises((NotImplementedError, IndexError)):
                features_widget._render_button_on_click()
        else:
            features_widget._render_button_on_click()
