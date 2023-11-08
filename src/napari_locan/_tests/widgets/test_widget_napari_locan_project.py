import locan as lc
import napari
import pytest

from napari_locan.data_model.filter_specifications import FilterSpecifications
from napari_locan.data_model.region_specifications import RegionSpecifications
from napari_locan.data_model.roi_specifications import RoiSpecifications
from napari_locan.data_model.smlm_data import SmlmData
from napari_locan.widgets.widget_napari_locan_project import NapariLocanProjectQWidget


class TestNapariLocanStateQWidget:
    def test_NapariLocanProjectQWidget_init(self, make_napari_viewer):
        filter_specifications = FilterSpecifications()
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = NapariLocanProjectQWidget(
            viewer,
            smlm_data=smlm_data,
            filter_specifications=filter_specifications,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
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
        filter_specifications = FilterSpecifications(datasets=[selectors, selectors])

        region_specifications = RegionSpecifications(
            datasets=[lc.Rectangle(), lc.EmptyRegion()], names=["rectange", "empty"]
        )
        roi_specifications = RoiSpecifications(
            datasets=[lc.Roi(region=lc.Rectangle()), lc.Roi(region=lc.Rectangle())],
            names=["1", "2"],
        )

        viewer = make_napari_viewer()
        my_widget = NapariLocanProjectQWidget(
            viewer,
            smlm_data=smlm_data_0,
            filter_specifications=filter_specifications,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
        )

        my_widget._new_button_on_click()
        assert my_widget.filter_specifications.index == -1
        assert my_widget.filter_specifications.datasets == []
        assert my_widget.filter_specifications.names == []
        assert my_widget.region_specifications.datasets == []
        assert my_widget.region_specifications.names == []
        assert my_widget.region_specifications.index == -1
        assert my_widget.smlm_data.index == -1
        assert my_widget.smlm_data.locdatas == []
        assert my_widget.smlm_data.locdata_names == []

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
        filter_specifications_0.append_item(dataset=selectors)

        region_specifications_0 = RegionSpecifications(
            datasets=[lc.Rectangle(), lc.EmptyRegion()], names=["rectangle", "empty"]
        )
        roi_specifications_0 = RoiSpecifications(
            datasets=[lc.Roi(region=lc.Rectangle()), lc.Roi(region=lc.Rectangle())],
            names=["1", "2"],
        )

        viewer = make_napari_viewer()
        my_widget = NapariLocanProjectQWidget(
            viewer,
            smlm_data=smlm_data_0,
            filter_specifications=filter_specifications_0,
            region_specifications=region_specifications_0,
            roi_specifications=roi_specifications_0,
        )

        my_widget._save_button_on_click()

        smlm_data_1 = SmlmData()
        filter_specifications_1 = FilterSpecifications()
        region_specifications_1 = RegionSpecifications()
        roi_specifications_1 = RoiSpecifications()
        viewer = make_napari_viewer()
        new_widget = NapariLocanProjectQWidget(
            viewer,
            smlm_data=smlm_data_1,
            filter_specifications=filter_specifications_1,
            region_specifications=region_specifications_1,
            roi_specifications=roi_specifications_1,
        )

        new_widget._load_button_on_click()

        assert (
            my_widget.smlm_data._locdatas[0].meta
            == new_widget.smlm_data._locdatas[0].meta
        )
        assert my_widget.smlm_data._locdata_names == new_widget.smlm_data._locdata_names
        assert my_widget.smlm_data._index == new_widget.smlm_data._index
        assert new_widget.smlm_data == smlm_data_1

        assert repr(my_widget.filter_specifications._datasets) == repr(
            new_widget.filter_specifications._datasets
        )
        assert (
            my_widget.filter_specifications._names
            == new_widget.filter_specifications._names
        )
        assert (
            my_widget.filter_specifications._index
            == new_widget.filter_specifications._index
        )
        assert new_widget.filter_specifications == filter_specifications_1

        assert repr(my_widget.region_specifications._datasets[0]) == repr(
            new_widget.region_specifications._datasets[0]
        )
        assert (
            my_widget.region_specifications._names
            == new_widget.region_specifications._names
        )
        assert (
            my_widget.region_specifications._index
            == new_widget.region_specifications._index
        )
        assert new_widget.region_specifications == region_specifications_1

        assert repr(my_widget.roi_specifications._datasets[0]) == repr(
            new_widget.roi_specifications._datasets[0]
        )
        assert (
            my_widget.roi_specifications._names == new_widget.roi_specifications._names
        )
        assert (
            my_widget.roi_specifications._index == new_widget.roi_specifications._index
        )
        assert new_widget.roi_specifications == roi_specifications_1


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
