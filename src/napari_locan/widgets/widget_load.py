"""
Load SMLM data files.

A QWidget plugin to load SMLM data files into the SMLM data model.
A new SMLM dataset will be created.
"""

import ast
import logging
from pathlib import Path

import locan as lc
from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class LoadQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_file_type()
        self._add_file_path()
        self._add_kwargs_edit()
        self._add_buttons()
        self._set_layout()

    def _add_file_type(self) -> None:
        self._file_type_label = QLabel("File type:")
        self._file_type_combobox = QComboBox()
        file_types = [
            type_.name
            for type_ in lc.FileType
            if type_.name != lc.FileType.UNKNOWN_FILE_TYPE.name
        ]
        self._file_type_combobox.addItems(file_types)
        self._file_type_combobox.setCurrentText(lc.FileType.RAPIDSTORM.name)

        self._file_type_layout = QHBoxLayout()
        self._file_type_layout.addWidget(self._file_type_label)
        self._file_type_layout.addWidget(self._file_type_combobox)

    def _add_file_path(self) -> None:
        self._file_path_label = QLabel("File path:")
        self._file_path_edit = QLineEdit()
        self._file_path_select_button = QPushButton("Select")
        self._file_path_select_button.setToolTip("Select a file path.")
        self._file_path_select_button.clicked.connect(
            self._file_path_select_button_on_click
        )
        self._file_path_delete_button = QPushButton("Delete")
        self._file_path_delete_button.setToolTip("Clear the file path.")
        self._file_path_delete_button.clicked.connect(
            self._file_path_delete_button_on_click
        )

        self._file_path_layout = QHBoxLayout()
        self._file_path_layout.addWidget(self._file_path_label)
        self._file_path_layout.addWidget(self._file_path_edit)
        self._file_path_layout.addWidget(self._file_path_select_button)
        self._file_path_layout.addWidget(self._file_path_delete_button)

    def _add_kwargs_edit(self) -> None:
        self._kwargs_edit_label = QLabel("**kwargs:")
        self._kwargs_edit = QLineEdit()
        self._kwargs_edit.setToolTip("Add kwargs for load function like 'nrows=10'.")

        self._kwargs_edit_layout = QHBoxLayout()
        self._kwargs_edit_layout.addWidget(self._kwargs_edit_label)
        self._kwargs_edit_layout.addWidget(self._kwargs_edit)

    def _add_buttons(self) -> None:
        self._load_button = QPushButton("Load File")
        self._load_button.setToolTip("Load the selected file as new SMLM dataset.")
        self._load_button.clicked.connect(self._load_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._file_type_layout)
        layout.addLayout(self._file_path_layout)
        layout.addLayout(self._kwargs_edit_layout)
        layout.addWidget(self._load_button)
        self.setLayout(layout)

    def _file_path_select_button_on_click(self) -> None:
        fname_ = QFileDialog.getOpenFileName(
            None,
            "message",
            "",
            filter="",
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )
        fname = fname_[0] if isinstance(fname_, tuple) else str(fname_)
        self._file_path_edit.setText(fname)

    def _file_path_delete_button_on_click(self) -> None:
        self._file_path_edit.clear()

    def _load_button_on_click(self) -> None:
        if not self._file_path_edit.text():
            self._file_path_select_button_on_click()
        else:
            fname_ = QFileDialog.getOpenFileName(
                None,
                "message",
                self._file_path_edit.text(),
                filter="",
                # kwargs: parent, message, directory, filter
                # but kw_names are different for different qt_bindings
            )
            fname = fname_[0] if isinstance(fname_, tuple) else str(fname_)
            self._file_path_edit.setText(fname)

        file_path = self._file_path_edit.text()
        file_type = self._file_type_combobox.currentText()

        text = self._kwargs_edit.text()
        expr = ast.parse(f"dict({text}\n)", mode="eval")
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in expr.body.keywords}  # type: ignore

        with progress() as progress_bar:
            progress_bar.set_description("Loading data")
            locdata = lc.load_locdata(path=file_path, file_type=file_type, **kwargs)
            locdata_name = locdata.meta.identifier + "-" + str(Path(file_path).name)
            self.smlm_data.append_item(locdata=locdata, locdata_name=locdata_name)
