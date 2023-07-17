"""
QWidget plugin to load SMLM data
"""
import logging

import locan as lc
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
from napari_locan._locdata import SmlmData

logger = logging.getLogger(__name__)


class LoadQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_file_type()
        self._add_file_path()
        self._add_buttons()
        self._set_layout()

    def _add_file_type(self) -> None:
        self._file_type_label = QLabel("File type:")
        self._file_type_combobox = QComboBox()
        file_types = list(lc.FileType.__members__.keys())
        self._file_type_combobox.addItems(file_types)
        self._file_type_combobox.setCurrentIndex(lc.FileType.RAPIDSTORM.value)

        self._file_type_layout = QHBoxLayout()
        self._file_type_layout.addWidget(self._file_type_label)
        self._file_type_layout.addWidget(self._file_type_combobox)

    def _add_file_path(self) -> None:
        self._file_path_label = QLabel("File path:")
        self._file_path_edit = QLineEdit()
        self._file_path_select_button = QPushButton("Select")
        self._file_path_select_button.setStatusTip("Select a file path.")
        self._file_path_select_button.clicked.connect(
            self._file_path_select_button_on_click
        )

        self._file_path_layout = QHBoxLayout()
        self._file_path_layout.addWidget(self._file_path_label)
        self._file_path_layout.addWidget(self._file_path_edit)
        self._file_path_layout.addWidget(self._file_path_select_button)

    def _add_buttons(self) -> None:
        self._load_button = QPushButton("Load File")
        self._load_button.setStatusTip("Load the selected file as new SMLM dataset.")
        self._load_button.clicked.connect(self._load_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._file_type_layout)
        layout.addLayout(self._file_path_layout)
        layout.addWidget(self._load_button)
        self.setLayout(layout)

    def _file_path_select_button_on_click(self) -> None:
        fname_ = QFileDialog.getOpenFileName(
            None,
            "message",
            "",
            filter=""
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )
        fname = fname_[0] if isinstance(fname_, tuple) else str(fname_)
        self._file_path_edit.setText(fname)

    def _load_button_on_click(self) -> None:
        if not self._file_path_edit.text():
            self._file_path_select_button_on_click()

        file_path = self._file_path_edit.text()
        file_type = self._file_type_combobox.currentText()
        locdata = lc.load_locdata(path=file_path, file_type=file_type)
        self.smlm_data.locdatas.append(locdata)
        self.smlm_data.locdatas = self.smlm_data.locdatas  # needed to activate setter