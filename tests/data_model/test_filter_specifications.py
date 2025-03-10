import locan as lc

from napari_locan.data_model.data_model_base import DataModel
from napari_locan.data_model.filter_specifications import FilterSpecifications


class TestFilterSpecifications:
    def test_init(self):
        filter_specifications = FilterSpecifications()
        assert isinstance(filter_specifications, DataModel)
        assert filter_specifications.datasets == []
        assert filter_specifications.names == []
        assert filter_specifications.index == -1
        assert filter_specifications.dataset is None
        assert filter_specifications.name == ""
        assert filter_specifications.filter_condition == ""

        selectors = {
            "position_x": lc.Selector(
                loc_property="position_x", activate=True, lower_bound=0, upper_bound=1
            ),
            "position_y": lc.Selector(
                loc_property="position_y", activate=True, lower_bound=0, upper_bound=1
            ),
        }
        filter_specifications = FilterSpecifications(
            datasets=[selectors, selectors], names=["1", "2"]
        )
        assert len(filter_specifications.datasets) == 2
        assert len(filter_specifications.names) == 2
        assert filter_specifications.index == 1
        assert isinstance(filter_specifications.dataset, dict)
        assert isinstance(filter_specifications.name, str)
        assert filter_specifications.name == "2"

        assert (
            filter_specifications.filter_condition
            == "0 < position_x < 1 and 0 < position_y < 1"
        )
