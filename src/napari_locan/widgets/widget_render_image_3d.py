"""
Render 3d image.

A QWidget plugin to render SMLM data as image by binning localization
properties into 3d pixels.
"""

from __future__ import annotations

import logging

import locan as lc
from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class RenderImage3dQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_loc_properties_selection()
        self._add_other_properties_selection()
        self._add_bin_size()
        self._add_bin_range()
        self._add_rescale()
        self._add_render_buttons()
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
            key_index = list(self.smlm_data.locdata.data.columns).index(  # type: ignore
                self.smlm_data.locdata.coordinate_keys[0]  # type: ignore
            )
            self._loc_properties_x_combobox.setCurrentIndex(key_index)

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
            key_index = list(self.smlm_data.locdata.data.columns).index(  # type: ignore
                self.smlm_data.locdata.coordinate_keys[1]  # type: ignore
            )
            self._loc_properties_y_combobox.setCurrentIndex(key_index)

        self._loc_properties_z_label = QLabel("z:")
        self._loc_properties_z_combobox = QComboBox()
        self._loc_properties_z_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset as z coordinate."
        )
        self.smlm_data.index_changed_signal.connect(
            self._loc_properties_z_combobox_slot_for_smlm_data_index
        )
        if self.smlm_data.index != -1 and bool(self.smlm_data.locdata):
            self._loc_properties_z_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            key_index = list(self.smlm_data.locdata.data.columns).index(  # type: ignore
                self.smlm_data.locdata.coordinate_keys[2]  # type: ignore
            )
            self._loc_properties_z_combobox.setCurrentIndex(key_index)

        self._loc_properties_layout = QHBoxLayout()
        self._loc_properties_layout.addWidget(self._loc_properties_x_label)
        self._loc_properties_layout.addWidget(self._loc_properties_x_combobox)
        self._loc_properties_layout.addWidget(self._loc_properties_y_label)
        self._loc_properties_layout.addWidget(self._loc_properties_y_combobox)
        self._loc_properties_layout.addWidget(self._loc_properties_z_label)
        self._loc_properties_layout.addWidget(self._loc_properties_z_combobox)

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
                    new_key_index = list(self.smlm_data.locdata.data.columns).index(  # type: ignore  # noqa: E501
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
                    new_key_index = list(self.smlm_data.locdata.data.columns).index(  # type: ignore  # noqa: E501
                        self.smlm_data.locdata.coordinate_keys[1]  # type: ignore
                    )
                    self._loc_properties_y_combobox.setCurrentIndex(new_key_index)
                else:
                    self._loc_properties_y_combobox.setCurrentIndex(-1)
            else:
                self._loc_properties_y_combobox.setCurrentIndex(key_index)

    def _loc_properties_z_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_properties_z_combobox.currentIndex()
        self._loc_properties_z_combobox.clear()
        if index != -1:
            self._loc_properties_z_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    new_key_index = list(self.smlm_data.locdata.data.columns).index(  # type: ignore  # noqa: E501
                        self.smlm_data.locdata.coordinate_keys[2]  # type: ignore
                    )
                    self._loc_properties_z_combobox.setCurrentIndex(new_key_index)
                else:
                    self._loc_properties_z_combobox.setCurrentIndex(-1)
            else:
                self._loc_properties_z_combobox.setCurrentIndex(key_index)

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

    def _add_bin_size(self) -> None:
        self._bin_size_label = QLabel("Bin size:")
        self._bin_size_spin_box = QSpinBox()
        self._bin_size_spin_box.setRange(1, 2147483647)
        self._bin_size_spin_box.setValue(10)

        self._bin_size_layout = QHBoxLayout()
        self._bin_size_layout.addWidget(self._bin_size_label)
        self._bin_size_layout.addWidget(self._bin_size_spin_box)

    def _add_bin_range(self) -> None:
        self._bin_range_check_box = QCheckBox()
        self._bin_range_check_box.setChecked(False)
        self._bin_range_check_box.stateChanged.connect(
            self._bin_range_check_box_on_changed
        )

        self._bin_range_label = QLabel("Bin range:")

        self._bin_range_min_label = QLabel("min:")
        self._bin_range_min_spin_box = QDoubleSpinBox()
        self._bin_range_min_spin_box.setRange(-1e10, 1e10)
        self._bin_range_min_spin_box.setValue(0)

        self._bin_range_max_label = QLabel("max:")
        self._bin_range_max_spin_box = QDoubleSpinBox()
        self._bin_range_max_spin_box.setRange(-1e10, 1e10)
        self._bin_range_max_spin_box.setValue(1e10)

        self._bin_range_layout = QHBoxLayout()
        self._bin_range_layout.addWidget(self._bin_range_label)
        self._bin_range_layout.addWidget(self._bin_range_min_label)
        self._bin_range_layout.addWidget(self._bin_range_min_spin_box)
        self._bin_range_layout.addWidget(self._bin_range_max_label)
        self._bin_range_layout.addWidget(self._bin_range_max_spin_box)
        self._bin_range_layout.addStretch()
        self._bin_range_layout.addWidget(self._bin_range_check_box)

        self._bin_range_check_box_on_changed()

    def _bin_range_check_box_on_changed(self) -> None:
        self._bin_range_min_label.setVisible(self._bin_range_check_box.isChecked())
        self._bin_range_min_spin_box.setVisible(self._bin_range_check_box.isChecked())
        self._bin_range_max_label.setVisible(self._bin_range_check_box.isChecked())
        self._bin_range_max_spin_box.setVisible(self._bin_range_check_box.isChecked())

    def _add_rescale(self) -> None:
        self._rescale_label = QLabel("Rescale intensity:")
        self._rescale_combobox = QComboBox()
        trafos = list(lc.Trafo.__members__.keys())
        self._rescale_combobox.addItems(trafos)
        self._rescale_combobox.setCurrentIndex(lc.Trafo.EQUALIZE.value)

        self._rescale_layout = QHBoxLayout()
        self._rescale_layout.addWidget(self._rescale_label)
        self._rescale_layout.addWidget(self._rescale_combobox)

    def _add_render_buttons(self) -> None:
        self._render_button = QPushButton("Render image")
        self._render_button.setToolTip("Render selected SMLM data in new image layer.")
        self._render_button.clicked.connect(self._render_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._other_properties_layout)
        layout.addLayout(self._bin_size_layout)
        layout.addLayout(self._bin_range_layout)
        layout.addLayout(self._rescale_layout)
        layout.addWidget(self._render_button)
        self.setLayout(layout)

    def _render_button_on_click(self) -> None:
        locdata = self.smlm_data.locdata
        if locdata is None:
            raise ValueError("There is no SMLM data available.")
        elif bool(locdata) is False:
            raise ValueError("Locdata is empty.")

        loc_properties = [
            self._loc_properties_x_combobox.currentText(),
            self._loc_properties_y_combobox.currentText(),
            self._loc_properties_z_combobox.currentText(),
        ]
        other_property: str | None = self._loc_properties_other_combobox.currentText()
        other_property = other_property if other_property != "" else None

        # set bins
        if self._bin_range_check_box.isChecked():
            bin_range_ = (
                self._bin_range_min_spin_box.value(),
                self._bin_range_max_spin_box.value(),
            )
            bin_range = [bin_range_] * locdata.dimension
        else:
            bin_range = None

        # optional kwargs for the corresponding viewer.add_* method
        add_kwargs = {"name": self.smlm_data.locdata_name}

        # render data
        with progress() as progress_bar:
            progress_bar.set_description("Rendering:")
            lc.render_3d_napari(
                locdata=locdata,
                loc_properties=loc_properties,
                other_property=other_property,
                viewer=self.viewer,
                bin_size=int(self._bin_size_spin_box.value()),
                bin_range=bin_range,
                rescale=self._rescale_combobox.currentText(),
                cmap=lc.COLORMAP_DEFAULTS["CONTINUOUS"],
                **add_kwargs,  # type: ignore[arg-type]
            )
