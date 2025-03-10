import locan as lc

from napari_locan.data_model.data_model_base import DataModel
from napari_locan.data_model.region_specifications import RegionSpecifications


class TestRegionSpecifications:
    def test_init(self):
        region_specs = RegionSpecifications()
        assert isinstance(region_specs, DataModel)
        assert region_specs.datasets == []
        assert region_specs.names == []
        assert region_specs.index == -1
        assert region_specs.dataset is None
        assert region_specs.name == ""

        region_specs = RegionSpecifications(
            datasets=[lc.Rectangle(), lc.EmptyRegion()], names=["rectange", "empty"]
        )
        assert len(region_specs.datasets) == 2
        assert len(region_specs.names) == 2
        assert region_specs.index == 1
        assert isinstance(region_specs.dataset, lc.Region)
        assert isinstance(region_specs.name, str)
        assert region_specs.name == "empty"
