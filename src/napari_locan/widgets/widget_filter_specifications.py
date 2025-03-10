"""
The data model for filter specifications.

A QWidget plugin to list filter specifications that can be applied to select
localizations from a SMLM dataset.
"""

import logging

from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import filter_specifications, smlm_data
from napari_locan.data_model.filter_specifications import FilterSpecifications
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class FilterSpecificationsQWidget(QWidget):  # type: ignore
    def __init__(
        self,
        napari_viewer: Viewer,
        smlm_data: SmlmData = smlm_data,
        filter_specifications: FilterSpecifications = filter_specifications,
    ):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data
        self.filter_specifications = filter_specifications

        self._add_filter_specifications_combobox()
        self._add_buttons()
        self._set_layout()

    def _add_filter_specifications_combobox(self) -> None:
        self._filter_specifications_combobox = QComboBox()
        self._connect_filter_specifications_combobox_and_filter_specifications()

        self._filter_specifications_layout = QHBoxLayout()
        self._filter_specifications_layout.addWidget(
            self._filter_specifications_combobox
        )

    def _connect_filter_specifications_combobox_and_filter_specifications(self) -> None:
        self.filter_specifications.names_changed_signal.connect(
            self._synchronize_filter_specifications_to_combobox
        )
        self.filter_specifications.names_changed_signal.emit(
            self.filter_specifications.names
        )

        self.filter_specifications.index_changed_signal.connect(
            self._filter_specifications_combobox.setCurrentIndex
        )
        self.filter_specifications.index_changed_signal.emit(
            self.filter_specifications.index
        )

        self._filter_specifications_combobox.currentIndexChanged.connect(
            self.filter_specifications.set_index_slot
        )

    def _synchronize_filter_specifications_to_combobox(self, names: list[str]) -> None:
        current_index = self.filter_specifications.index
        self._filter_specifications_combobox.clear()
        self._filter_specifications_combobox.addItems(names)
        self._filter_specifications_combobox.setCurrentIndex(current_index)

    def _add_buttons(self) -> None:
        self._delete_all_button = QPushButton("Delete all")
        self._delete_all_button.setToolTip("Delete all filter specifications.")
        self._delete_all_button.clicked.connect(self._delete_all_button_on_click)

        self._delete_button = QPushButton("Delete")
        self._delete_button.setToolTip("Delete filter specifications dataset.")
        self._delete_button.clicked.connect(self._delete_button_on_click)

        self._new_button = QPushButton("New")
        self._new_button.setToolTip("Create new filter specifications dataset.")
        self._new_button.clicked.connect(self._new_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._delete_all_button)
        self._buttons_layout.addWidget(self._delete_button)
        self._buttons_layout.addWidget(self._new_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._buttons_layout)
        layout.addLayout(self._filter_specifications_layout)
        self.setLayout(layout)

    def _delete_all_button_on_click(self) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Do you really want to delete ALL filter specifications?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
        msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:  # type: ignore[attr-defined]
            self.filter_specifications.delete_all()
        else:
            return

    def _delete_button_on_click(self) -> None:
        self.filter_specifications.delete_item()

    def _new_button_on_click(self) -> None:
        self.filter_specifications.append_item(dataset={})
