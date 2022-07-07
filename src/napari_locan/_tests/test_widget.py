from pathlib import Path

import locan as lc

from napari_locan import LoadDataQWidget, RunScriptQWidget


def test_LoadDataQWidget(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    my_widget = LoadDataQWidget(viewer)

    locan_test_data = Path(lc.__file__).resolve().parent / \
                "tests/test_data" / \
                "rapidSTORM_dstorm_data.txt"

    my_widget._file_path_edit.insert(str(locan_test_data))
    my_widget._file_type_combobox.setCurrentIndex(lc.FileType.RAPIDSTORM.value)

    # needs user interaction:
    #my_widget._file_path_select_button_on_click()

    my_widget._load_button_on_click()
    assert len(viewer.layers) == 1

    captured = capsys.readouterr()
    assert captured.out == ""


def test_RunScriptQWidget(make_napari_viewer, capsys):
    import src.napari_locan._scripts as nl_scripts
    viewer = make_napari_viewer()
    my_widget = RunScriptQWidget(viewer)
    assert my_widget._script_combobox.currentText() == "HELLO"
    assert my_widget._script_text_edit.toPlainText() == nl_scripts.script_hello
    my_widget._run_button_on_click()

    captured = capsys.readouterr()
    assert captured.out == "Hello world!\n"

    my_widget._script_combobox.setCurrentText("LOAD")
    assert my_widget._script_text_edit.toPlainText() == nl_scripts.script_load
    my_widget._run_button_on_click()
    assert len(viewer.layers) == 1
