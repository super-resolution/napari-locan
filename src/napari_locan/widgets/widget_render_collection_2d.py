"""
Render collection of SMLM data as 2d point clouds.

A QWidget plugin to render a collection of SMLM data (e.g. a cluster collection)
as series of point clouds in 2d.
"""

from __future__ import annotations

import logging
from typing import Any

import locan as lc
import numpy as np
import numpy.typing as npt
from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QCheckBox,
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


class RenderCollection2dQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_loc_properties_selection()
        self._add_other_properties_selection()
        self._add_translation_selection()
        self._add_points_buttons()
        self._connect_signals()
        self._set_layout()

    def _connect_signals(self) -> None:
        self.smlm_data.index_changed_signal.connect(
            self._loc_properties_x_combobox_slot_for_smlm_data_index
        )
        self.smlm_data.index_changed_signal.connect(
            self._loc_properties_y_combobox_slot_for_smlm_data_index
        )
        self.smlm_data.index_changed_signal.connect(
            self._loc_properties_other_combobox_slot_for_smlm_data_index
        )

    def _add_translation_selection(self) -> None:
        self._translation_label = QLabel("Translate to common origin:")
        self._translation_check_box = QCheckBox()
        self._translation_check_box.setToolTip(
            "Translate each dataset to centroid = (0, 0)."
        )
        self._translation_selection_layout = QHBoxLayout()
        self._translation_selection_layout.addWidget(self._translation_label)
        self._translation_selection_layout.addWidget(self._translation_check_box)

    def _add_loc_properties_selection(self) -> None:
        self._loc_properties_x_label = QLabel("x:")
        self._loc_properties_x_combobox = QComboBox()
        self._loc_properties_x_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as x coordinate."
        )

        # condition excludes smlm_data.locdata to be None in what comes:
        if (
            self.smlm_data.locdata is not None  # self.smlm_data.index != -1
            and bool(self.smlm_data.locdata)
            and isinstance(self.smlm_data.locdata.references, list)
        ):
            columns_ = list(self.smlm_data.locdata.references)[0].data.columns
            self._loc_properties_x_combobox.addItems(columns_)
            try:
                key_index = list(columns_).index(
                    self.smlm_data.locdata.coordinate_keys[0]
                )
                self._loc_properties_x_combobox.setCurrentIndex(key_index)
            except IndexError:
                self._loc_properties_x_combobox.setCurrentIndex(-1)

        self._loc_properties_y_label = QLabel("y:")
        self._loc_properties_y_combobox = QComboBox()
        self._loc_properties_y_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as y coordinate."
        )

        if (
            self.smlm_data.locdata is not None  # self.smlm_data.index != -1
            and bool(self.smlm_data.locdata)
            and isinstance(self.smlm_data.locdata.references, list)
        ):
            columns_ = list(self.smlm_data.locdata.references)[0].data.columns
            self._loc_properties_y_combobox.addItems(columns_)
            try:
                key_index = list(columns_).index(
                    self.smlm_data.locdata.coordinate_keys[1]
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
        if (
            self.smlm_data.locdata is not None  # self.smlm_data.index != -1
            and bool(self.smlm_data.locdata)
            and isinstance(self.smlm_data.locdata.references, list)
        ):
            self._loc_properties_other_combobox.addItem("")
            self._loc_properties_other_combobox.addItems(
                self.smlm_data.locdata.references[0].data.columns
            )
        key_index = 0
        self._loc_properties_other_combobox.setCurrentIndex(key_index)

        self._other_properties_layout = QHBoxLayout()
        self._other_properties_layout.addWidget(self._loc_properties_other_label)
        self._other_properties_layout.addWidget(self._loc_properties_other_combobox)

    def _loc_properties_x_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_properties_x_combobox.currentIndex()
        self._loc_properties_x_combobox.clear()
        if self.smlm_data.locdata is None:
            return None
        elif self.smlm_data.locdata.references is None or isinstance(
            self.smlm_data.locdata.references, lc.LocData
        ):
            # raise TypeError("SMLM data must be a LocData collection.")
            return None
        else:
            columns_ = list(self.smlm_data.locdata.references)[0].data.columns
            self._loc_properties_x_combobox.addItems(columns_)  # type: ignore[arg-type]
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(columns_).index(
                        self.smlm_data.locdata.coordinate_keys[0]
                    )
                    self._loc_properties_x_combobox.setCurrentIndex(new_key_index)
                else:
                    self._loc_properties_x_combobox.setCurrentIndex(-1)
            else:
                self._loc_properties_x_combobox.setCurrentIndex(key_index)

    def _loc_properties_y_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_properties_y_combobox.currentIndex()
        self._loc_properties_y_combobox.clear()
        if self.smlm_data.locdata is None:
            return None
        elif self.smlm_data.locdata.references is None or isinstance(
            self.smlm_data.locdata.references, lc.LocData
        ):
            # raise TypeError("SMLM data must be a LocData collection.")
            return None
        else:
            columns_ = list(self.smlm_data.locdata.references)[0].data.columns
            self._loc_properties_y_combobox.addItems(columns_)  # type: ignore[arg-type]
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(columns_).index(
                        self.smlm_data.locdata.coordinate_keys[1]
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
        if self.smlm_data.locdata is None:
            return None
        elif self.smlm_data.locdata.references is None or isinstance(
            self.smlm_data.locdata.references, lc.LocData
        ):
            # raise TypeError("SMLM data must be a LocData collection.")
            return None
        else:
            columns_ = list(self.smlm_data.locdata.references)[0].data.columns
            self._loc_properties_other_combobox.addItems(columns_)  # type: ignore[arg-type]
            if key_index == -1:
                self._loc_properties_other_combobox.setCurrentIndex(0)
            else:
                self._loc_properties_other_combobox.setCurrentIndex(key_index)

    def _add_points_buttons(self) -> None:
        self._concatenate_button = QPushButton("Concatenate")
        self._concatenate_button.setToolTip(
            "Concatenate all collection elements in new  SMLM dataset."
        )
        self._concatenate_button.clicked.connect(self._concatenate_button_on_click)

        self._render_points_button = QPushButton("Render points")
        self._render_points_button.setToolTip(
            "Show point representation of all SMLM data collection elements in new points layer."
        )
        self._render_points_button.clicked.connect(self._render_points_button_on_click)

        self._render_points_as_series_button = QPushButton("Render points as series")
        self._render_points_as_series_button.setToolTip(
            "Show series of point representations for SMLM data collection elements in new points layer."
        )
        self._render_points_as_series_button.clicked.connect(
            self._render_points_as_series_button_on_click
        )

        self._points_buttons_layout = QVBoxLayout()
        self._points_buttons_layout.addWidget(self._concatenate_button)
        self._points_buttons_layout.addWidget(self._render_points_button)
        self._points_buttons_layout.addWidget(self._render_points_as_series_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._other_properties_layout)
        layout.addLayout(self._translation_selection_layout)
        layout.addLayout(self._points_buttons_layout)
        self.setLayout(layout)

    def _prepare_collection_for_rendering(
        self,
    ) -> tuple[list[str], str | None, lc.LocData] | None:
        if self.smlm_data.locdata is None:
            raise ValueError("There is no SMLM data available.")
        elif bool(self.smlm_data.locdata) is False:
            raise ValueError("Locdata is empty.")
        elif self._get_message_feedback() is False:
            return None
        else:
            locdata = self.smlm_data.locdata

        loc_properties = [
            self._loc_properties_x_combobox.currentText(),
            self._loc_properties_y_combobox.currentText(),
        ]
        other_property: str | None = self._loc_properties_other_combobox.currentText()
        other_property = other_property if other_property != "" else None

        # translation to centroid.
        if self._translation_check_box.isChecked():
            if any(
                loc_property_ not in self.smlm_data.locdata.coordinate_keys
                for loc_property_ in loc_properties
            ):
                raise ValueError(
                    "Overlay is only implemented for loc_properties being coordinate labels."
                )
            else:
                locdata = lc.overlay(
                    locdatas=self.smlm_data.locdata.references,  # type: ignore[arg-type]
                    centers="centroid",
                    orientations=None,
                )
        return loc_properties, other_property, locdata

    def _concatenate_button_on_click(self) -> None:
        returned = self._prepare_collection_for_rendering()
        if returned is None:
            return None
        else:
            loc_properties, other_property, locdata = returned
        locdata = lc.LocData.concat(locdatas=locdata.references)  # type: ignore
        self.smlm_data.append_item(locdata=locdata, set_index=False)

    def _render_points_button_on_click(self) -> None:
        with progress() as progress_bar:
            progress_bar.set_description("Rendering:")
            returned = self._prepare_collection_for_rendering()
            if returned is None:
                return None
            else:
                loc_properties, other_property, locdata = returned

            locdata = lc.LocData.concat(locdatas=locdata.references)  # type: ignore
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

            self.viewer.add_points(data=data, properties=point_properties, **add_kwargs)

    def _render_points_as_series_button_on_click(self) -> None:
        with progress() as progress_bar:
            progress_bar.set_description("Rendering:")
            returned = self._prepare_collection_for_rendering()
            if returned is None:
                return
            else:
                loc_properties, other_property, locdata = returned

            reference_data = [
                reference.data[loc_properties].to_numpy()
                for reference in locdata.references  # type: ignore
            ]

            img_stack = [
                np.insert(reference_, 0, i, axis=1)
                for i, reference_ in enumerate(reference_data)
            ]
            data = np.concatenate(img_stack, axis=0)

            if other_property is None:
                point_properties: dict[str, npt.NDArray[Any]] = {}
                add_kwargs = {"name": self.smlm_data.locdata_name}
            else:
                other_property_stack = [
                    reference.data[other_property].to_numpy()
                    for reference in locdata.references  # type: ignore
                ]
                other_data = np.concatenate(other_property_stack, axis=0)
                other_property_data = lc.adjust_contrast(
                    other_data, rescale=lc.Trafo.STANDARDIZE
                )
                point_properties = {"other_property": other_property_data}
                add_kwargs = {
                    "name": self.smlm_data.locdata_name,
                    "edge_color": "",
                    "face_color": "other_property",
                    "face_colormap": "viridis",
                }

            self.viewer.add_points(data=data, properties=point_properties, **add_kwargs)

    def _get_message_feedback(self) -> bool:
        n_localizations = len(self.smlm_data.locdata)  # type: ignore
        if n_localizations < 1_000:
            run_computation = True
        else:
            msgBox = QMessageBox()
            msgBox.setText(
                f"There are {n_localizations} datasets in the collection. "
                f"Rendering will take some time."
            )
            msgBox.setInformativeText("Do you want to continue?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
            msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
            return_value = msgBox.exec()
            run_computation = bool(return_value == QMessageBox.Ok)  # type: ignore[attr-defined]
        return run_computation
