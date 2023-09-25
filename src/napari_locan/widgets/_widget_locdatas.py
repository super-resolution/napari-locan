"""
QWidget plugin to list locdatas
"""
import logging

from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model._locdata import SmlmData

logger = logging.getLogger(__name__)


class LocdatasQWidget(QWidget):  # type: ignore
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
        self.smlm_data.locdata_names_signal.connect(
            self._synchronize_smlm_data_to_combobox
        )
        self.smlm_data.index_signal.connect(self._locdatas_combobox.setCurrentIndex)
        self._locdatas_combobox.currentIndexChanged.connect(
            self.smlm_data.set_index_slot
        )
        self.smlm_data.change_event()

    def _synchronize_smlm_data_to_combobox(self, locdata_names: list[str]) -> None:
        self._locdatas_combobox.clear()
        self._locdatas_combobox.addItems(locdata_names)

    def _add_buttons(self) -> None:
        self._delete_button = QPushButton("Delete")
        self._delete_button.setToolTip("Delete SMLM dataset.")
        self._delete_button.clicked.connect(self._delete_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._delete_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._buttons_layout)
        layout.addLayout(self._locdatas_layout)
        self.setLayout(layout)

    def _delete_button_on_click(self) -> None:
        current_index = self._locdatas_combobox.currentIndex()
        if current_index == -1:
            raise KeyError("No item available to be deleted.")
        else:
            self.smlm_data.locdatas.pop(current_index)
            self.smlm_data.locdatas = (
                self.smlm_data.locdatas
            )  # needed to activate setter

            self.smlm_data.change_event()
