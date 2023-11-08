import locan as lc
import napari
import pytest

from napari_locan import SelectQWidget
from napari_locan.data_model.filter_specifications import FilterSpecifications
from napari_locan.data_model.smlm_data import SmlmData


class TestSelectQWidget:
    def test_SelectQWidget_init(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        filter_specifications = FilterSpecifications()
        viewer = make_napari_viewer()
        my_widget = SelectQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget._loc_property_combobox.currentIndex() == -1
        assert my_widget._lower_bound_spinbox.isHidden()
        assert my_widget._upper_bound_spinbox.isHidden()
        assert my_widget._apply_checkbox.isHidden()
        assert my_widget._condition_text_edit.toPlainText() == ""
        viewer.close()

        smlm_data = SmlmData(locdatas=[locdata_2d])
        filter_specifications = FilterSpecifications()
        viewer = make_napari_viewer()
        my_widget = SelectQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget._loc_property_combobox.currentIndex() == 0
        assert my_widget._lower_bound_spinbox.value() == 1.0
        assert my_widget._upper_bound_spinbox.value() == 5.0
        assert my_widget._apply_checkbox.isChecked() is False
        assert my_widget._condition_text_edit.toPlainText() == ""
        viewer.close()

        smlm_data = SmlmData(locdatas=[locdata_2d])
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=10, upper_bound=20
            ),
            "position_y": lc.Selector(
                loc_property="position_y",
                activate=False,
                lower_bound=10,
                upper_bound=20,
            ),
        }
        filter_specifications = FilterSpecifications([selectors])
        viewer = make_napari_viewer()
        my_widget = SelectQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget._loc_property_combobox.currentIndex() == 0
        assert my_widget._lower_bound_spinbox.value() == 10
        assert my_widget._upper_bound_spinbox.value() == 20
        assert my_widget._apply_checkbox.isChecked() is True
        assert (
            my_widget._condition_text_edit.toPlainText() == "10.0 < position_x < 20.0"
        )
        viewer.close()

        smlm_data = SmlmData(locdatas=[locdata_2d])
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=10, upper_bound=20
            ),
            "something": lc.Selector(
                loc_property="something", activate=True, lower_bound=10, upper_bound=20
            ),
        }
        filter_specifications = FilterSpecifications([selectors])
        viewer = make_napari_viewer()
        my_widget = SelectQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget._loc_property_combobox.currentIndex() == 0
        assert my_widget._lower_bound_spinbox.value() == 10
        assert my_widget._upper_bound_spinbox.value() == 20
        assert my_widget._apply_checkbox.isChecked() is True
        assert (
            my_widget._condition_text_edit.toPlainText()
            == "10.0 < position_x < 20.0 and 10 < something < 20"
        )
        viewer.close()

    def test_SelectQWidget_changes(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData(locdatas=[locdata_2d])
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=10, upper_bound=20
            ),
            "something": lc.Selector(
                loc_property="something", activate=False, lower_bound=10, upper_bound=20
            ),
        }
        filter_specifications = FilterSpecifications([selectors])
        viewer = make_napari_viewer()
        my_widget = SelectQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget._loc_property_combobox.currentIndex() == 0
        assert my_widget._lower_bound_spinbox.value() == 10
        assert my_widget._upper_bound_spinbox.value() == 20
        assert my_widget._apply_checkbox.isChecked() is True
        assert (
            my_widget._condition_text_edit.toPlainText() == "10.0 < position_x < 20.0"
        )

        my_widget._loc_property_combobox.setCurrentIndex(0)
        my_widget._lower_bound_spinbox.setValue(9)
        my_widget._upper_bound_spinbox.setValue(19)
        my_widget._apply_checkbox.setChecked(False)
        assert my_widget._loc_property_combobox.currentIndex() == 0
        assert my_widget._lower_bound_spinbox.value() == 9
        assert my_widget._upper_bound_spinbox.value() == 19
        assert my_widget._apply_checkbox.isChecked() is False
        assert my_widget._condition_text_edit.toPlainText() == ""

        smlm_data.index = 0
        with pytest.raises(ValueError):
            my_widget._select_button_on_click()

        my_widget._apply_checkbox.setChecked(True)
        assert my_widget._loc_property_combobox.currentIndex() == 0
        assert my_widget._lower_bound_spinbox.value() == 9
        assert my_widget._upper_bound_spinbox.value() == 19
        assert my_widget._apply_checkbox.isChecked() is True
        assert my_widget._condition_text_edit.toPlainText() == "9.0 < position_x < 19.0"

        my_widget._loc_property_combobox.setCurrentIndex(3)
        assert my_widget._loc_property_combobox.currentIndex() == 3
        assert my_widget._lower_bound_spinbox.value() == 80
        assert my_widget._upper_bound_spinbox.value() == 150
        assert my_widget._apply_checkbox.isChecked() is False
        assert my_widget._condition_text_edit.toPlainText() == "9.0 < position_x < 19.0"

        my_widget._select_button_on_click()
        assert len(smlm_data.locdatas) == 2
        assert smlm_data.index == 1

        my_widget.filter_specifications.set_datasets_and_names(datasets=[])
        assert my_widget._loc_property_combobox.currentIndex() == -1
        assert my_widget._lower_bound_spinbox.isHidden()
        assert my_widget._upper_bound_spinbox.isHidden()
        assert my_widget._apply_checkbox.isHidden()

        my_widget._loc_property_combobox.setCurrentIndex(1)


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_image")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Filter specifications"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Select"
    )
    napari.run()
