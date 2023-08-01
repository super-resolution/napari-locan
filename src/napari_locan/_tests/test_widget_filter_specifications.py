import locan as lc
import pytest

from napari_locan import FilterSpecificationsQWidget
from napari_locan.data_model._filter import FilterSpecifications
from napari_locan.data_model._locdata import SmlmData


class TestLocdatasQWidget:
    def test_FilterSpecificationsQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        filter_specifications = FilterSpecifications()
        viewer = make_napari_viewer()
        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert not my_widget._filter_specifications_combobox.isEditable()
        assert my_widget._filter_specifications_combobox.currentIndex() == -1
        assert my_widget._filter_specifications_combobox.currentText() == ""

    def test_FilterSpecificationsQWidget_changing_locdatas(self, make_napari_viewer):
        smlm_data = SmlmData()
        filter_specifications = FilterSpecifications()
        locdata_0, locdata_1 = lc.LocData(), lc.LocData()
        smlm_data.locdatas = [locdata_0, locdata_1]
        viewer = make_napari_viewer()

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications.filters = [selectors, selectors]

        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""

        my_widget._filter_specifications_combobox.setCurrentIndex(1)
        assert my_widget._filter_specifications_combobox.currentIndex() == 1
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.index == 1

        filter_specifications.filters = []
        assert my_widget._filter_specifications_combobox.currentIndex() == -1
        assert my_widget._filter_specifications_combobox.currentText() == ""

    def test_FilterSpecificationsQWidget_buttons(self, make_napari_viewer):
        smlm_data = SmlmData()
        filter_specifications = FilterSpecifications()
        viewer = make_napari_viewer()

        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )

        with pytest.raises(KeyError):
            my_widget._delete_button_on_click()

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications.filters = [selectors, selectors]

        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.filters == [selectors, selectors]

        my_widget._delete_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.filters == [selectors]

        my_widget._delete_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == -1
        assert my_widget._filter_specifications_combobox.currentText() == ""
        assert filter_specifications.filters == []

        my_widget._new_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() == "0"
        assert filter_specifications.filters == [{}]
