import locan as lc
import napari
import pytest

from napari_locan.data_model.filter import FilterSpecifications
from napari_locan.data_model.smlm_data import SmlmData
from napari_locan.widgets.widget_napari_locan_project import NapariLocanProjectQWidget


class TestNapariLocanStateQWidget:
    def test_NapariLocanProjectQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        filter_specifications = FilterSpecifications()
        viewer = make_napari_viewer()
        my_widget = NapariLocanProjectQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget

    def test_NapariLocanProjectQWidget_new(self, make_napari_viewer, locdata_2d):
        smlm_data_0 = SmlmData(locdatas=[locdata_2d], locdata_names=["locdata_2d"])
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications = FilterSpecifications()
        filter_specifications.append_item(filter=selectors)
        filter_specifications.append_item(filter=selectors)

        viewer = make_napari_viewer()
        my_widget = NapariLocanProjectQWidget(
            viewer, smlm_data=smlm_data_0, filter_specifications=filter_specifications
        )

        my_widget._new_button_on_click()
        assert my_widget.smlm_data.index == -1
        assert my_widget.smlm_data.locdatas == []
        assert my_widget.smlm_data.locdata_names == []
        assert my_widget.filter_specifications.index == -1
        assert my_widget.filter_specifications.filters == []
        assert my_widget.filter_specifications.filter_names == []

    @pytest.mark.skip("needs user interaction")
    def test_NapariLocanProjectQWidget_save_and_load(
        self, make_napari_viewer, locdata_2d
    ):
        smlm_data_0 = SmlmData(locdatas=[locdata_2d], locdata_names=["locdata_2d"])
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications_0 = FilterSpecifications()
        filter_specifications_0.append_item(filter=selectors)
        viewer = make_napari_viewer()
        my_widget = NapariLocanProjectQWidget(
            viewer, smlm_data=smlm_data_0, filter_specifications=filter_specifications_0
        )

        my_widget._save_button_on_click()

        smlm_data_1 = SmlmData()
        filter_specifications_1 = FilterSpecifications()
        viewer = make_napari_viewer()
        new_widget = NapariLocanProjectQWidget(
            viewer, smlm_data=smlm_data_1, filter_specifications=filter_specifications_1
        )

        new_widget._load_button_on_click()

        assert (
            my_widget.smlm_data._locdatas[0].meta
            == new_widget.smlm_data._locdatas[0].meta
        )
        assert my_widget.smlm_data._locdata_names == new_widget.smlm_data._locdata_names
        assert my_widget.smlm_data._index == new_widget.smlm_data._index
        assert new_widget.smlm_data == smlm_data_1

        assert repr(my_widget.filter_specifications._filters) == repr(
            new_widget.filter_specifications._filters
        )
        assert (
            my_widget.filter_specifications._filter_names
            == new_widget.filter_specifications._filter_names
        )
        assert (
            my_widget.filter_specifications._index
            == new_widget.filter_specifications._index
        )
        assert new_widget.filter_specifications == filter_specifications_1


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_points")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    _, filter_widget = viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Filter specifications"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="napari-locan project"
    )
    selectors = {
        "position_x": lc.Selector(
            loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
        ),
        "position_y": lc.Selector(
            loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
        ),
    }
    filter_widget.filter_specifications.append_item(filter=selectors)
    napari.run()