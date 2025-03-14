"""
Save SMLM data files.

A QWidget plugin to save data from the SMLM data model.
"""

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


class SaveSmlmDataQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_file_type()
        self._add_file_path()
        # self._add_kwargs_edit()
        self._add_buttons()
        self._set_layout()

    def _add_file_type(self) -> None:
        self._file_type_label = QLabel("File type:")
        self._file_type_combobox = QComboBox()
        file_types = [
            type_.name
            for type_ in lc.FileType
            if type_.name in ["ASDF", "parquet", "SMAP", "SMLM", "THUNDERSTORM"]
        ]
        self._file_type_combobox.addItems(file_types)
        self._file_type_combobox.setCurrentText(lc.FileType.ASDF.name)

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

    # def _add_kwargs_edit(self) -> None:
    #     self._kwargs_edit_label = QLabel("**kwargs:")
    #     self._kwargs_edit = QLineEdit()
    #     self._kwargs_edit.setToolTip("Add kwargs for save function.")
    #
    #     self._kwargs_edit_layout = QHBoxLayout()
    #     self._kwargs_edit_layout.addWidget(self._kwargs_edit_label)
    #     self._kwargs_edit_layout.addWidget(self._kwargs_edit)

    def _add_buttons(self) -> None:
        self._save_button = QPushButton("Save SMLM data")
        self._save_button.setToolTip("Save the selected SMLM dataset.")
        self._save_button.clicked.connect(self._save_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._file_type_layout)
        layout.addLayout(self._file_path_layout)
        # layout.addLayout(self._kwargs_edit_layout)
        layout.addWidget(self._save_button)
        self.setLayout(layout)

    def _file_path_select_button_on_click(self) -> None:
        fname_ = QFileDialog.getSaveFileName(
            None,
            "Save as...",
            "",
            filter="ASDF (*.asdf);;CSV files (*.csv);;Parquet files (*.parquet);;SMAP (*.csv);;SMLM (*.zip);;THUNDERSTORM (*.csv)",
            selectedFilter="ASDF (*.asdf)",
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )
        fname = fname_[0] if isinstance(fname_, tuple) else str(fname_)
        self._file_path_edit.setText(fname)

    def _file_path_delete_button_on_click(self) -> None:
        self._file_path_edit.clear()

    def _save_button_on_click(self) -> None:
        if not self._file_path_edit.text():
            self._file_path_select_button_on_click()

        file_path = Path(self._file_path_edit.text())
        file_type = self._file_type_combobox.currentText()

        # text = self._kwargs_edit.text()
        # expr = ast.parse(f"dict({text}\n)", mode="eval")
        # kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in expr.body.keywords}  # type: ignore

        with progress() as progress_bar:
            progress_bar.set_description("Saving data")
            if file_type == lc.FileType.ASDF.name and file_path.suffix == ".asdf":
                lc.save_asdf(locdata=self.smlm_data.locdata, path=file_path)  # type: ignore[arg-type]
            elif file_type == lc.FileType.SMAP.name and file_path.suffix == ".csv":
                lc.save_SMAP_csv(locdata=self.smlm_data.locdata, path=file_path)  # type: ignore[arg-type]
            elif file_type == lc.FileType.SMLM.name and file_path.suffix == ".zip":
                lc.save_SMLM(locdata=self.smlm_data.locdata, path=file_path)  # type: ignore[arg-type]
            elif (
                file_type == lc.FileType.THUNDERSTORM.name
                and file_path.suffix == ".csv"
            ):
                lc.save_thunderstorm_csv(locdata=self.smlm_data.locdata, path=file_path)  # type: ignore[arg-type]
            else:
                raise TypeError(
                    "Selected file type cannot be saved. Check that file suffix is correct."
                )
