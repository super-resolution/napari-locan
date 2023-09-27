from napari_locan import ShowDataQWidget
from napari_locan.data_model._locdata import SmlmData


class TestShowPropertiesQWidget:
    def test_ShowDataQWidget(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = ShowDataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._data_text_edit.toPlainText() == ""

        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = ShowDataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._data_text_edit.toPlainText().startswith("   position_x")
