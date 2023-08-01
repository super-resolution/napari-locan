import warnings

import locan as lc
import pytest

from napari_locan.data_model._filter import FilterSpecifications


class TestFilterSpecifications:
    def test_init(self):
        filter_specifications = FilterSpecifications()
        assert filter_specifications.filters == []
        assert filter_specifications.filter_names == []
        assert filter_specifications.index == -1
        assert filter_specifications.filter is None
        assert filter_specifications.filter_name == ""
        assert filter_specifications.filter_condition == ""

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }

        filter_specifications.filters = [selectors, selectors]
        assert len(filter_specifications.filters) == 2
        assert len(filter_specifications.filter_names) == 2
        assert filter_specifications.index == 0
        assert isinstance(filter_specifications.filter, dict)
        assert isinstance(filter_specifications.filter_name, str)
        assert isinstance(filter_specifications.filter_condition, str)

        filter_specifications = FilterSpecifications(filters=[selectors, selectors])
        assert len(filter_specifications.filters) == 2
        assert len(filter_specifications.filter_names) == 2
        assert filter_specifications.index == 0
        assert isinstance(filter_specifications.filter, dict)
        assert isinstance(filter_specifications.filter_name, str)

    def test_index(self):
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }

        filter_specifications = FilterSpecifications()
        filter_specifications.filters = [selectors, selectors]
        assert filter_specifications.index == 0
        assert (
            filter_specifications.filter
            is filter_specifications.filters[filter_specifications.index]
        )

        filter_specifications.index = 1
        assert filter_specifications.index == 1
        assert (
            filter_specifications.filter
            is filter_specifications.filters[filter_specifications.index]
        )

        with pytest.raises(IndexError):
            filter_specifications.index = 3

        filter_specifications.index = -1
        assert filter_specifications.index == -1
        assert filter_specifications.filter is None

    def test_append_filter(self):
        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications = FilterSpecifications()
        filter_specifications.append_filter(filter=selectors)
        filter_specifications.append_filter(filter=selectors)
        assert len(filter_specifications.filters) == 2
        assert len(filter_specifications.filter_names) == 2
        assert filter_specifications.index == 1
        assert isinstance(filter_specifications.filter, dict)
        assert isinstance(filter_specifications.filter_name, str)

    def test_connect(self):
        def filters_slot(filters):
            if filters != []:
                warnings.warn("filter_specifications not empty.", stacklevel=1)

        def index_slot(index):
            if index != -1:
                warnings.warn("index not -1.", stacklevel=1)

        filter_specifications = FilterSpecifications()
        filter_specifications.filters_signal.connect(filters_slot)
        filter_specifications.index_signal.connect(index_slot)

        filter_specifications.filters = []
        assert filter_specifications.filters == []
        assert filter_specifications.filter_names == []
        assert filter_specifications.index == -1
        assert filter_specifications.filter is None
        assert filter_specifications.filter_name == ""

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        with pytest.warns():
            filter_specifications.filters = [selectors, selectors]
        assert len(filter_specifications.filters) == 2
        assert len(filter_specifications.filter_names) == 2
        assert filter_specifications.index == 0
        assert isinstance(filter_specifications.filter, dict)
        assert isinstance(filter_specifications.filter_name, str)

    def test_change(self):
        filter_specifications = FilterSpecifications()
        assert filter_specifications.filters == []
        assert filter_specifications.filter_names == []
        assert filter_specifications.index == -1
        assert filter_specifications.filter is None
        assert filter_specifications.filter_name == ""

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications.filters = [selectors, selectors]
        assert len(filter_specifications.filters) == 2
        assert len(filter_specifications.filter_names) == 2
        assert filter_specifications.index == 0
        assert isinstance(filter_specifications.filter, dict)
        assert isinstance(filter_specifications.filter_name, str)

        filter_specifications.filters = filter_specifications.filters[:1]
        assert len(filter_specifications.filters) == 1
        assert len(filter_specifications.filter_names) == 1
        assert filter_specifications.index == 0
        assert isinstance(filter_specifications.filter, dict)
        assert isinstance(filter_specifications.filter_name, str)

        assert filter_specifications.filter["position_x"].activate is True
        filter_specifications.filter["position_x"].activate = False
        assert filter_specifications.filter["position_x"].activate is False
