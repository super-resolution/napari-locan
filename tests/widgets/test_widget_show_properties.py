from napari_locan import ShowPropertiesQWidget
from napari_locan.data_model.smlm_data import SmlmData


class TestShowPropertiesQWidget:
    def test_ShowPropertiesQWidget(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = ShowPropertiesQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._properties_text_edit.toPlainText() == ""

        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = ShowPropertiesQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._properties_text_edit.toPlainText().startswith(
            "{'frame': 1,"
        ) or my_widget._properties_text_edit.toPlainText().startswith(
            "{'frame': np.int64(1)"
        )
