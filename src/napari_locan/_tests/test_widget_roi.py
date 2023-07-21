from napari_locan import RoiQWidget
from napari_locan.data_model._locdata import SmlmData


class TestRoiQWidgetQWidget:
    def test_RoiQWidget_init(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(viewer, smlm_data=smlm_data)
        assert not my_widget._locdatas_combobox.isEditable()
        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._locdatas_combobox.currentText() == ""

        # todo:
        # make shapes layer
        # load file with path
        # check text for rois
        # save in temp directory

    def test_RoiQWidget_(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(viewer, smlm_data=smlm_data)
        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._locdatas_combobox.currentText() != ""
