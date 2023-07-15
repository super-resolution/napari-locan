from pathlib import Path

import locan as lc

from napari_locan import RenderQWidget


def test_RenderQWidget(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    my_widget = RenderQWidget(viewer)

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
    assert len(viewer.layers) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
