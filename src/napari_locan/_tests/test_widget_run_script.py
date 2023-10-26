from pathlib import Path

from napari_locan import RunScriptQWidget


class TestRunScriptQWidget:
    def test_RunScriptQWidget(self, make_napari_viewer, capsys):
        viewer = make_napari_viewer()
        my_widget = RunScriptQWidget(viewer)
        assert my_widget._script_combobox.currentText() == "HELLO"
        assert Path(my_widget._script_file_name_edit.text()).name == "script_hello.py"
        assert my_widget._script_text_edit.toPlainText().startswith(
            '"""\nSay hello!\n"""'
        )
        my_widget._run_button_on_click()
        captured = capsys.readouterr()
        assert captured.out == "Hello world!\n"

        my_widget._script_combobox.setCurrentText("NONE")
        assert my_widget._script_combobox.currentText() == "NONE"
        assert my_widget._script_file_name_edit.text() == ""
        assert my_widget._script_text_edit.toPlainText().startswith("")
        my_widget._run_button_on_click()
        captured = capsys.readouterr()
        assert captured.out == ""

        my_widget._script_combobox.setCurrentText("LOAD")
        assert my_widget._script_combobox.currentText() == "LOAD"
        assert Path(my_widget._script_file_name_edit.text()).name == "script_load.py"
        assert my_widget._script_text_edit.toPlainText().startswith(
            '"""\nLoad SMLM data\n"""'
        )
        my_widget._run_button_on_click()
        captured = capsys.readouterr()
        assert "identifier" in captured.out
        assert len(viewer.layers) == 1

        # needs user interaction:
        # my_widget._script_load_button_on_click()
        # assert Path(my_widget._script_file_name_edit.text()).name == "script_hello.py"
