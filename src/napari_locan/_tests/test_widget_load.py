from pathlib import Path

import locan as lc

from napari_locan import LoadQWidget
from napari_locan.data_model._locdata import SmlmData


class TestLoadQWidget:
    def test_LoadQWidget(self, make_napari_viewer):
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = LoadQWidget(viewer, smlm_data=smlm_data)

        locan_test_data = (
            Path(lc.__file__).resolve().parent
            / "tests/test_data"
            / "rapidSTORM_dstorm_data.txt"
        )

        my_widget._file_path_edit.insert(str(locan_test_data))
        my_widget._file_type_combobox.setCurrentIndex(lc.FileType.RAPIDSTORM.value)

        # needs user interaction:
        # my_widget._file_path_select_button_on_click()

        my_widget._load_button_on_click()
        assert Path(smlm_data.locdata.meta.file.path) == locan_test_data
