"""
The data model for localization-based SMLM data.

QWidget plugin to access SMLM datasets from which images are rendered
and localization-based analysis procedures are computed.
Each dataset is kept as locdata, i.e. a locan.LocData object with metadata,
aggregated properties, and localization properties for all localizations.
"""

import logging
from pathlib import Path

import locan as lc
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class SmlmDataQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_locdatas_combobox()
        self._add_buttons()
        self._set_layout()

    def _add_locdatas_combobox(self) -> None:
        self._locdatas_combobox = QComboBox()
        self._connect_locdatas_combobox_and_smlm_data()

        self._locdatas_layout = QHBoxLayout()
        self._locdatas_layout.addWidget(self._locdatas_combobox)

    def _connect_locdatas_combobox_and_smlm_data(self) -> None:
        self.smlm_data.locdata_names_changed_signal.connect(
            self._synchronize_smlm_data_to_combobox
        )
        self.smlm_data.locdata_names_changed_signal.emit(self.smlm_data.locdata_names)

        self.smlm_data.index_changed_signal.connect(
            self._locdatas_combobox.setCurrentIndex
        )
        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)

        self._locdatas_combobox.currentIndexChanged.connect(
            self.smlm_data.set_index_slot
        )

    def _synchronize_smlm_data_to_combobox(self, locdata_names: list[str]) -> None:
        current_index = self.smlm_data.index
        self._locdatas_combobox.clear()
        self._locdatas_combobox.addItems(locdata_names)
        self._locdatas_combobox.setCurrentIndex(current_index)

    def _add_buttons(self) -> None:
        self._save_button = QPushButton("Save")
        self._save_button.setToolTip("Save SMLM dataset as ASDF file.")
        self._save_button.clicked.connect(self._save_button_on_click)

        self._delete_all_button = QPushButton("Delete all")
        self._delete_all_button.setToolTip("Delete all SMLM data.")
        self._delete_all_button.clicked.connect(self._delete_all_button_on_click)

        self._delete_button = QPushButton("Delete")
        self._delete_button.setToolTip("Delete SMLM dataset.")
        self._delete_button.clicked.connect(self._delete_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._delete_all_button)
        self._buttons_layout.addWidget(self._delete_button)
        self._buttons_layout.addWidget(self._save_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._buttons_layout)
        layout.addLayout(self._locdatas_layout)
        self.setLayout(layout)

    def _delete_button_on_click(self) -> None:
        self.smlm_data.delete_item()

    def _delete_all_button_on_click(self) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Do you really want to delete ALL datasets?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
        msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:  # type: ignore[attr-defined]
            self.smlm_data.delete_all()
        else:
            return

    def _save_button_on_click(self) -> None:
        current_index = self._locdatas_combobox.currentIndex()
        if current_index == -1:
            raise KeyError("No item available to be saved.")
        else:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.AnyFile)  # type: ignore[attr-defined]
            file_path_return = file_dialog.getSaveFileName(
                caption="Provide file name and path to save data",
                filter="ASDF file (*.asdf)",
            )
            file_path = Path(file_path_return[0])
            print("Save SmlmDdata at:", file_path)
            if file_path:
                lc.save_asdf(locdata=self.smlm_data.locdata, path=file_path)  # type: ignore[arg-type]
