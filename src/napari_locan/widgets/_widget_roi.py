"""
QWidget plugin for managing regions of interest
"""
import logging

import locan as lc
import napari
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model._locdata import SmlmData

logger = logging.getLogger(__name__)


class RoiQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_locdatas_combobox()
        self._add_loc_properties_selection()
        self._add_roi_text()
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

    def _add_loc_properties_selection(self) -> None:
        self._loc_properties_x_label = QLabel("x:")
        self._loc_properties_x_combobox = QComboBox()
        self.smlm_data.index_signal.connect(
            self._loc_properties_x_combobox_slot_for_smlm_data_index
        )
        # condition excludes smlm_data.locdata to be None in what comes:
        if self.smlm_data.index != -1 and bool(self.smlm_data.locdata):
            self._loc_properties_x_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            try:
                key_index = list(
                    self.smlm_data.locdata.data.columns  # type: ignore
                ).index(
                    self.smlm_data.locdata.coordinate_keys[0]  # type: ignore
                )
                self._loc_properties_x_combobox.setCurrentIndex(key_index)
            except IndexError:
                self._loc_properties_x_combobox.setCurrentIndex(-1)

        self._loc_properties_y_label = QLabel("y:")
        self._loc_properties_y_combobox = QComboBox()
        self.smlm_data.index_signal.connect(
            self._loc_properties_y_combobox_slot_for_smlm_data_index
        )
        if self.smlm_data.index != -1 and bool(self.smlm_data.locdata):
            self._loc_properties_y_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            try:
                key_index = list(
                    self.smlm_data.locdata.data.columns  # type: ignore
                ).index(
                    self.smlm_data.locdata.coordinate_keys[1]  # type: ignore
                )
                self._loc_properties_y_combobox.setCurrentIndex(key_index)
            except IndexError:
                self._loc_properties_y_combobox.setCurrentIndex(-1)

        self._loc_properties_layout = QHBoxLayout()
        self._loc_properties_layout.addWidget(self._loc_properties_x_label)
        self._loc_properties_layout.addWidget(self._loc_properties_x_combobox)
        self._loc_properties_layout.addWidget(self._loc_properties_y_label)
        self._loc_properties_layout.addWidget(self._loc_properties_y_combobox)

    def _loc_properties_x_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_properties_x_combobox.currentIndex()
        self._loc_properties_x_combobox.clear()
        if index != -1:
            self._loc_properties_x_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(
                        self.smlm_data.locdata.data.columns  # type: ignore
                    ).index(
                        self.smlm_data.locdata.coordinate_keys[0]  # type: ignore
                    )
                    self._loc_properties_x_combobox.setCurrentIndex(new_key_index)
                else:
                    self._loc_properties_x_combobox.setCurrentIndex(-1)
            else:
                self._loc_properties_x_combobox.setCurrentIndex(key_index)

    def _loc_properties_y_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_properties_y_combobox.currentIndex()
        self._loc_properties_y_combobox.clear()
        if index != -1:
            self._loc_properties_y_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(
                        self.smlm_data.locdata.data.columns  # type: ignore
                    ).index(
                        self.smlm_data.locdata.coordinate_keys[1]  # type: ignore
                    )
                    self._loc_properties_y_combobox.setCurrentIndex(new_key_index)
                else:
                    self._loc_properties_y_combobox.setCurrentIndex(-1)
            else:
                self._loc_properties_y_combobox.setCurrentIndex(key_index)

    def _add_roi_text(self) -> None:
        self._roi_text_edit = QPlainTextEdit()

        self._roi_text_layout = QHBoxLayout()
        self._roi_text_layout.addWidget(self._roi_text_edit)

    def _add_buttons(self) -> None:
        self._save_button = QPushButton("Save")
        self._save_button.setStatusTip("Save region of interest in yaml file.")
        self._save_button.clicked.connect(self._save_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._save_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._locdatas_layout)
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._roi_text_layout)
        layout.addLayout(self._buttons_layout)
        self.setLayout(layout)

    def _save_button_on_click(self) -> None:
        # todo: currently updates the text field
        layer = self._get_current_shapes_layer()
        if smlm_data.index != -1 and layer is not None:
            reference = smlm_data.locdata.meta  # type: ignore
            loc_properties = [
                self._loc_properties_x_combobox.currentText(),
                self._loc_properties_y_combobox.currentText(),
            ]

            rois = lc.get_rois(
                shapes_layer=layer, reference=reference, loc_properties=loc_properties
            )

            text = str(rois)

            self._roi_text_edit.setPlainText(text)

            # lc.save_rois(rois=rois, file_path=None, roi_file_indicator="_roi")

    def _get_current_shapes_layer(self) -> napari.layers.Layer:
        layer_selection = self.viewer.layers.selection
        if len(layer_selection) > 1:
            raise ValueError("You need to select a single shapes layer.")
        else:
            layer = layer_selection.pop()
        return layer
