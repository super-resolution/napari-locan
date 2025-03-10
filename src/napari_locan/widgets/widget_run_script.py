"""
Run python script.

A QWidget plugin with a simple interface to handle python scripts for
localization analysis.
"""

from pathlib import Path

from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import napari_locan._scripts as nl_scripts
import napari_locan.scripts


class RunScriptQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.path_for_scripts = Path(napari_locan.scripts.__file__).resolve().parent

        self._add_script()
        self._add_buttons()
        self._set_layout()

    def _add_script(self) -> None:
        self._script_combobox = QComboBox()
        self._script_combobox.setToolTip("Choose a predefined python script.")
        scripts = list(nl_scripts.LocanScripts.__members__.keys())
        self._script_combobox.addItems(scripts)
        self._script_combobox.setCurrentText("HELLO")
        self._script_combobox.currentIndexChanged.connect(
            self._script_combobox_on_change
        )

        self._script_load_button = QPushButton("Load")
        self._script_load_button.setToolTip("Load a python script.")
        self._script_load_button.clicked.connect(self._script_load_button_on_click)

        self._script_save_button = QPushButton("Save")
        self._script_save_button.setToolTip("Save a python script.")
        self._script_save_button.clicked.connect(self._script_save_button_on_click)

        self._script_file_name_edit = QLineEdit()

        self._script_text_edit = QPlainTextEdit()

        self._script_combobox_on_change()

        self._script_buttons_layout = QHBoxLayout()
        self._script_buttons_layout.addWidget(self._script_combobox)
        self._script_buttons_layout.addWidget(self._script_load_button)
        self._script_buttons_layout.addWidget(self._script_save_button)

        self._script_layout = QVBoxLayout()
        self._script_layout.addLayout(self._script_buttons_layout)
        self._script_layout.addWidget(self._script_file_name_edit)
        self._script_layout.addWidget(self._script_text_edit)

    def _script_load_button_on_click(self) -> None:
        file_path = self._script_file_name_edit.text()
        if not file_path:
            file_path = "../scripts"

        file_dialog = QFileDialog()

        file_name_ = file_dialog.getOpenFileName(
            None,
            "Load python script",
            file_path,
            filter="Python files (*.py);; All files (*)",
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )

        if file_dialog.fileSelected:
            self._script_combobox.setCurrentText("NONE")

            file_name = (
                file_name_[0] if isinstance(file_name_, tuple) else str(file_name_)
            )
            self._script_file_name_edit.setText(file_name)

            if file_name:
                with open(file_name) as file:
                    script = file.read()
                self._script_text_edit.setPlainText(script)

    def _script_save_button_on_click(self) -> None:
        file_path = self._script_file_name_edit.text()
        if not file_path:
            file_path = ".."

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)  # type: ignore[attr-defined]

        file_name_ = file_dialog.getSaveFileName(
            None,
            "Save python script",
            file_path,
            filter="Python files (*.py);; All files (*)",
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )
        file_name = file_name_[0] if isinstance(file_name_, tuple) else str(file_name_)

        if file_name:
            self._script_combobox.blockSignals(True)
            self._script_combobox.setCurrentText("NONE")
            self._script_combobox.blockSignals(False)

            self._script_file_name_edit.setText(file_name)

            with open(file_name, mode="w") as file:
                text = self._script_text_edit.toPlainText()
                file.write(text)

    def _add_buttons(self) -> None:
        self._run_button = QPushButton("Run")
        self._run_button.setToolTip("Run the displayed python script.")
        self._run_button.clicked.connect(self._run_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._script_layout)
        layout.addWidget(self._run_button)
        self.setLayout(layout)

    def _script_combobox_on_change(self) -> None:
        if self._script_combobox.currentText() == "NONE":
            self._script_file_name_edit.setText("")
            self._script_text_edit.setPlainText("")
        else:
            script_name = (
                self.path_for_scripts
                / nl_scripts.LocanScripts[self._script_combobox.currentText()].value
            )
            with open(str(script_name)) as file:
                script = file.read()
            self._script_file_name_edit.setText(str(script_name))
            self._script_text_edit.setPlainText(script)

    def _run_button_on_click(self) -> None:
        script = self._script_text_edit.toPlainText()
        with progress() as progress_bar:
            progress_bar.set_description("Running:")
            exec(script)  # noqa: S102
