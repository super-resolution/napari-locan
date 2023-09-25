"""
QWidget plugin to render a collection of SMLM data as series
"""
from __future__ import annotations

import logging

import locan as lc
import numpy as np
import numpy.typing as npt
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
from napari_locan.data_model._locdata import SmlmData

logger = logging.getLogger(__name__)


class CollectionSeriesQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_loc_properties_selection()
        self._add_other_properties_selection()
        self._add_translation_selection()
        self._add_points_buttons()
        self._set_layout()

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
        self.smlm_data.index_signal.connect(
            self._loc_properties_x_combobox_slot_for_smlm_data_index
        )
        # condition excludes smlm_data.locdata to be None in what comes:
        if (
            self.smlm_data.index != -1
            and bool(self.smlm_data.locdata)
            and isinstance(self.smlm_data.locdata.references, list)  # type: ignore
        ):
            self._loc_properties_x_combobox.addItems(
                self.smlm_data.locdata.references[0].data.columns  # type: ignore
            )
            try:
                key_index = list(
                    self.smlm_data.locdata.references[0].data.columns  # type: ignore
                ).index(
                    self.smlm_data.locdata.references[0].coordinate_keys[0]  # type: ignore
                )
                self._loc_properties_x_combobox.setCurrentIndex(key_index)
            except IndexError:
                self._loc_properties_x_combobox.setCurrentIndex(-1)

        self._loc_properties_y_label = QLabel("y:")
        self._loc_properties_y_combobox = QComboBox()
        self._loc_properties_y_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as y coordinate."
        )
        self.smlm_data.index_signal.connect(
            self._loc_properties_y_combobox_slot_for_smlm_data_index
        )
        if (
            self.smlm_data.index != -1
            and bool(self.smlm_data.locdata)
            and isinstance(self.smlm_data.locdata.references, list)  # type: ignore
        ):
            self._loc_properties_y_combobox.addItems(
                self.smlm_data.locdata.references[0].data.columns  # type: ignore
            )
            try:
                key_index = list(
                    self.smlm_data.locdata.references[0].data.columns  # type: ignore
                ).index(
                    self.smlm_data.locdata.references[0].coordinate_keys[1]  # type: ignore
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
        self.smlm_data.index_signal.connect(
            self._loc_properties_other_combobox_slot_for_smlm_data_index
        )
        if (
            self.smlm_data.index != -1
            and bool(self.smlm_data.locdata)
            and isinstance(self.smlm_data.locdata.references, list)  # type: ignore
        ):
            self._loc_properties_other_combobox.addItem("")
            self._loc_properties_other_combobox.addItems(
                self.smlm_data.locdata.references[0].data.columns  # type: ignore
            )
        key_index = 0
        self._loc_properties_other_combobox.setCurrentIndex(key_index)

        self._other_properties_layout = QHBoxLayout()
        self._other_properties_layout.addWidget(self._loc_properties_other_label)
        self._other_properties_layout.addWidget(self._loc_properties_other_combobox)

    def _loc_properties_x_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_properties_x_combobox.currentIndex()
        self._loc_properties_x_combobox.clear()
        if self.smlm_data.locdata.references is None:  # type: ignore
            raise TypeError("SMLM data must be a LocData collection.")
        if index != -1:
            self._loc_properties_x_combobox.addItems(
                self.smlm_data.locdata.references[0].data.columns  # type: ignore
            )
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(
                        self.smlm_data.locdata.references[0].data.columns  # type: ignore
                    ).index(
                        self.smlm_data.locdata.references[0].coordinate_keys[0]  # type: ignore
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
                self.smlm_data.locdata.references[0].data.columns  # type: ignore
            )
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(
                        self.smlm_data.locdata.references[0].data.columns  # type: ignore
                    ).index(
                        self.smlm_data.locdata.references[0].coordinate_keys[1]  # type: ignore
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
                self.smlm_data.locdata.references[0].data.columns  # type: ignore
            )
            if key_index == -1:
                self._loc_properties_other_combobox.setCurrentIndex(0)
            else:
                self._loc_properties_other_combobox.setCurrentIndex(key_index)

    def _add_points_buttons(self) -> None:
        self._points_button = QPushButton("Show points")
        self._points_button.setToolTip(
            "Show point representation of SMLM data in new layer."
        )
        self._points_button.clicked.connect(self._points_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._other_properties_layout)
        layout.addLayout(self._translation_selection_layout)
        layout.addWidget(self._points_button)
        self.setLayout(layout)

    def _points_button_on_click(self) -> None:
        locdata: lc.LocData = self.smlm_data.locdata
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
        other_property = self._loc_properties_other_combobox.currentText()
        other_property = other_property if other_property != "" else None

        # translation to centroid.
        if self._translation_check_box.isChecked():
            if any(
                loc_property_ not in locdata.coordinate_keys
                for loc_property_ in loc_properties
            ):
                raise ValueError(
                    "Overlay is only implemented for loc_properties beeing coordinate labels."
                )
            else:
                locdata = lc.overlay(
                    locdatas=locdata.references,
                    centers="centroid",
                    orientations=None,
                )

        reference_data = [
            reference.data[loc_properties].to_numpy()
            for reference in locdata.references
        ]

        img_stack = [
            np.insert(reference_, 0, i, axis=1)
            for i, reference_ in enumerate(reference_data)
        ]
        data = np.concatenate(img_stack, axis=0)

        if other_property is None:
            point_properties: dict[str, npt.NDArray] = {}
            add_kwargs = {"name": self.smlm_data.locdata_name}
        else:
            other_property_stack = [
                reference.data[other_property].to_numpy()
                for reference in locdata.references
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
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            return_value = msgBox.exec()
            run_computation = bool(return_value == QMessageBox.Ok)
        return run_computation
