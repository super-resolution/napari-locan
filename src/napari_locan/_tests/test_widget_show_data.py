from napari_locan import ShowDataQWidget
from napari_locan.data_model.smlm_data import SmlmData
from napari_locan.widgets.widget_show_data import TableModel


class TestTableModel:
    def test_TableModel(self, locdata_2d):
        df = locdata_2d.data
        model = TableModel(data=df)
        assert model.rowCount() == 6
        assert model.columnCount() == 4


class TestShowPropertiesQWidget:
    def test_ShowDataQWidget(self, make_napari_viewer, locdata_2d):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = ShowDataQWidget(viewer, smlm_data=smlm_data)

        assert my_widget._table_view.model() is None

        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = ShowDataQWidget(viewer, smlm_data=smlm_data)

        assert my_widget._table_view.model() is not None
