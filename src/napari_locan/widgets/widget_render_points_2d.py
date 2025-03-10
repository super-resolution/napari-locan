"""
Render 2d point cloud.

A QWidget plugin to render SMLM data in 2d.
"""

from __future__ import annotations

import logging
from typing import Any

import locan as lc
import numpy.typing as npt
from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class RenderPoints2dQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_loc_properties_selection()
        self._add_other_properties_selection()
        self._add_points_buttons()
        self._set_layout()

    def _add_loc_properties_selection(self) -> None:
        self._loc_properties_x_label = QLabel("x:")
        self._loc_properties_x_combobox = QComboBox()
        self._loc_properties_x_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as x coordinate."
        )
        self.smlm_data.index_changed_signal.connect(
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
        self._loc_properties_y_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as y coordinate."
        )
        self.smlm_data.index_changed_signal.connect(
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

    def _add_other_properties_selection(self) -> None:
        self._loc_properties_other_label = QLabel("other:")
        self._loc_properties_other_combobox = QComboBox()
        self._loc_properties_other_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as pixel value."
        )
        self.smlm_data.index_changed_signal.connect(
            self._loc_properties_other_combobox_slot_for_smlm_data_index
        )
        if self.smlm_data.index != -1 and bool(self.smlm_data.locdata):
            self._loc_properties_other_combobox.addItem("")
            self._loc_properties_other_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
        key_index = 0
        self._loc_properties_other_combobox.setCurrentIndex(key_index)

        self._other_properties_layout = QHBoxLayout()
        self._other_properties_layout.addWidget(self._loc_properties_other_label)
        self._other_properties_layout.addWidget(self._loc_properties_other_combobox)

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

    def _loc_properties_other_combobox_slot_for_smlm_data_index(
        self, index: int
    ) -> None:
        key_index = self._loc_properties_other_combobox.currentIndex()
        self._loc_properties_other_combobox.clear()
        self._loc_properties_other_combobox.addItem("")
        if index != -1:
            self._loc_properties_other_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            if key_index == -1:
                self._loc_properties_other_combobox.setCurrentIndex(0)
            else:
                self._loc_properties_other_combobox.setCurrentIndex(key_index)

    def _add_points_buttons(self) -> None:
        self._points_button = QPushButton("Render points")
        self._points_button.setToolTip(
            "Show point representation of SMLM data in new points layer."
        )
        self._points_button.clicked.connect(self._points_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._other_properties_layout)
        layout.addWidget(self._points_button)
        self.setLayout(layout)

    def _points_button_on_click(self) -> None:
        locdata = self.smlm_data.locdata
        if locdata is None:
            raise ValueError("There is no SMLM data available.")
        if bool(locdata) is False:
            raise ValueError("Locdata is empty.")
        if self._get_message_feedback() is False:
            return

        loc_properties = [
            self._loc_properties_x_combobox.currentText(),
            self._loc_properties_y_combobox.currentText(),
        ]
        other_property: str | None = self._loc_properties_other_combobox.currentText()
        other_property = other_property if other_property != "" else None
        data = locdata.data[loc_properties].to_numpy()

        if other_property is None:
            point_properties: dict[str, npt.NDArray[Any]] = {}
            add_kwargs = {"name": self.smlm_data.locdata_name}
        else:
            other_property_data = locdata.data[other_property].to_numpy()
            other_property_data = lc.adjust_contrast(
                other_property_data, rescale=lc.Trafo.STANDARDIZE
            )
            point_properties = {"other_property": other_property_data}
            add_kwargs = {
                "name": self.smlm_data.locdata_name,
                "edge_color": "",
                "face_color": "other_property",
                "face_colormap": "viridis",
            }

        with progress() as progress_bar:
            progress_bar.set_description("Rendering:")
            self.viewer.add_points(data=data, properties=point_properties, **add_kwargs)

    def _get_message_feedback(self) -> bool:
        n_localizations = len(self.smlm_data.locdata)  # type: ignore
        if n_localizations < 10_000:
            run_computation = True
        else:
            msgBox = QMessageBox()
            msgBox.setText(
                f"There are {n_localizations} localizations. "
                f"Rendering will take some time."
            )
            msgBox.setInformativeText("Do you want to continue?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
            msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
            return_value = msgBox.exec()
            run_computation = bool(return_value == QMessageBox.Ok)  # type: ignore[attr-defined]
        return run_computation
