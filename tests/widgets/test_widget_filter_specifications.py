import locan as lc
import pytest

from napari_locan import FilterSpecificationsQWidget
from napari_locan.data_model.filter_specifications import FilterSpecifications
from napari_locan.data_model.smlm_data import SmlmData


class TestFilterSpecificationsQWidget:
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

    def test_FilterSpecificationsQWidget_changing_datasets(self, make_napari_viewer):
        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications = FilterSpecifications(datasets=[selectors, selectors])

        viewer = make_napari_viewer()
        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )

        assert my_widget._filter_specifications_combobox.currentIndex() == 1
        assert my_widget._filter_specifications_combobox.currentText() != ""

        my_widget._filter_specifications_combobox.setCurrentIndex(0)
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.index == 0

        filter_specifications.delete_all()
        assert len(filter_specifications.datasets) == 0
        assert my_widget._filter_specifications_combobox.currentIndex() == -1
        assert my_widget._filter_specifications_combobox.currentText() == ""
        assert filter_specifications.index == -1

        filter_specifications.append_item(dataset=selectors)
        assert len(filter_specifications.datasets) == 1
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.index == 0

        filter_specifications.append_item(dataset=selectors, set_index=False)
        assert len(filter_specifications.datasets) == 2
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.index == 0

        filter_specifications.append_item(dataset=selectors)
        assert len(filter_specifications.datasets) == 3
        assert my_widget._filter_specifications_combobox.currentIndex() == 2
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.index == 2

    def test_FilterSpecificationsQWidget_delete_button(self, make_napari_viewer):
        filter_specifications = FilterSpecifications()
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )

        with pytest.raises(IndexError):
            my_widget._delete_button_on_click()

        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications = FilterSpecifications(datasets=[selectors, selectors])
        viewer = make_napari_viewer()
        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )

        my_widget._delete_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() != ""
        assert filter_specifications.names == ["0"]

        my_widget._delete_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == -1
        assert my_widget._filter_specifications_combobox.currentText() == ""
        assert filter_specifications.datasets == []

    @pytest.mark.skip("Needs user interaction")
    def test_FilterSpecificationsQWidget_delete_all_button(self, make_napari_viewer):
        smlm_data = SmlmData(
            locdatas=[lc.LocData(), lc.LocData()], locdata_names=["1", "2"]
        )
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications = FilterSpecifications(datasets=[selectors, selectors])
        viewer = make_napari_viewer()
        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )

        my_widget._delete_all_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == -1
        assert my_widget._filter_specifications_combobox.currentText() == ""
        assert filter_specifications.datasets == []

    def test_FilterSpecificationsQWidget_new_button(self, make_napari_viewer):
        smlm_data = SmlmData()
        filter_specifications = FilterSpecifications()
        viewer = make_napari_viewer()
        my_widget = FilterSpecificationsQWidget(
            viewer, smlm_data=smlm_data, filter_specifications=filter_specifications
        )

        my_widget._new_button_on_click()
        assert my_widget._filter_specifications_combobox.currentIndex() == 0
        assert my_widget._filter_specifications_combobox.currentText() == "1"
        assert filter_specifications.datasets == [{}]
