from napari_locan import MetadataQWidget
from napari_locan.data_model._locdata import SmlmData


class TestMetadataQWidget:
    def test_MetadataQWidget(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = MetadataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._metadata_text_edit.toPlainText() == ""

        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = MetadataQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._metadata_text_edit.toPlainText() != ""
