"""
QWidget plugin to list fitler specifications
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

from napari_locan import filter_specifications, smlm_data
from napari_locan.data_model._filter import FilterSpecifications
from napari_locan.data_model._locdata import SmlmData

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
        self.filter_specifications.filter_names_signal.connect(
            self._synchronize_filter_specifications_to_combobox
        )
        self.filter_specifications.index_signal.connect(
            self._filter_specifications_combobox.setCurrentIndex
        )
        self._filter_specifications_combobox.currentIndexChanged.connect(
            self.filter_specifications.set_index_slot
        )
        self.filter_specifications.change_event()

    def _synchronize_filter_specifications_to_combobox(
        self, filter_names: list[str]
    ) -> None:
        self._filter_specifications_combobox.clear()
        self._filter_specifications_combobox.addItems(filter_names)

    def _add_buttons(self) -> None:
        self._delete_button = QPushButton("Delete")
        self._delete_button.setStatusTip("Delete filter specifications dataset.")
        self._delete_button.clicked.connect(self._delete_button_on_click)

        self._new_button = QPushButton("New")
        self._new_button.setStatusTip("Create new filter specifications dataset.")
        self._new_button.clicked.connect(self._new_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._delete_button)
        self._buttons_layout.addWidget(self._new_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._buttons_layout)
        layout.addLayout(self._filter_specifications_layout)
        self.setLayout(layout)

    def _delete_button_on_click(self) -> None:
        current_index = self._filter_specifications_combobox.currentIndex()
        if current_index == -1:
            raise KeyError("No item available to be deleted.")
        else:
            self.filter_specifications.filters.pop(current_index)
            self.filter_specifications.filters = (
                self.filter_specifications.filters
            )  # needed to activate setter

            self.filter_specifications.change_event()

    def _new_button_on_click(self) -> None:
        self.filter_specifications.append_filter(filter={})
