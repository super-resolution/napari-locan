"""
Show localization property distribution.

A QWidget plugin to show localization property distributions
"""

from __future__ import annotations

import logging
from typing import Any

import locan as lc
from napari.utils import progress
from napari.viewer import Viewer
from napari_matplotlib.base import BaseNapariMPLWidget
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class PropertyDistributionQWidget(QWidget):  # type: ignore[misc]
    def __init__(
        self,
        napari_viewer: Viewer,
        smlm_data: SmlmData = smlm_data,
        parent: Any | None = None,
    ) -> None:
        super().__init__(parent=parent)
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_loc_property_selector()
        self._add_plot_widget()
        self._add_buttons()

        self._connect_loc_property_selector()
        self._init_widget_values()

        self._set_layout()

    def _add_loc_property_selector(self) -> None:
        self._loc_property_label = QLabel("Localization property:")
        self._loc_property_combobox = QComboBox()
        self._loc_property_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset."
        )
        # condition excludes smlm_data.locdata to be None in what comes:
        if self.smlm_data.index != -1 and bool(self.smlm_data.locdata):
            self._loc_property_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )

        self._loc_property_selector_layout = QHBoxLayout()
        self._loc_property_selector_layout.addWidget(self._loc_property_label)
        self._loc_property_selector_layout.addWidget(self._loc_property_combobox)

    def _connect_loc_property_selector(self) -> None:
        self.smlm_data.index_changed_signal.connect(
            self._loc_property_combobox_slot_for_smlm_data_index
        )
        self._loc_property_combobox.currentIndexChanged.connect(
            self._loc_property_combobox_on_changed
        )

    def _add_plot_widget(self) -> None:
        self._plot_widget = BaseNapariMPLWidget(self.viewer, parent=self)
        self._plot_widget.add_single_axes()

        self._plot_widget_layout = QVBoxLayout()
        self._plot_widget_layout.addWidget(self._plot_widget)

    def _add_buttons(self) -> None:
        self._select_button = QPushButton("Update plot")
        self._select_button.setToolTip(
            "Plot the distribution of the selected localization property."
        )
        self._select_button.clicked.connect(self._select_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._select_button)

    def _init_widget_values(self) -> None:
        try:
            self._loc_property_combobox.setCurrentIndex(0)
        except IndexError:
            self._loc_property_combobox.setCurrentIndex(-1)
        self._loc_property_combobox_on_changed()

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._loc_property_selector_layout)
        layout.addLayout(self._plot_widget_layout)
        layout.addLayout(self._buttons_layout)
        self.setLayout(layout)

    def _loc_property_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_property_combobox.currentIndex()
        self._loc_property_combobox.clear()
        self._plot_widget.axes.clear()
        self._plot_widget.canvas.draw()
        if index != -1:
            self._loc_property_combobox.addItems(
                self.smlm_data.locdata.data.columns  # type: ignore
            )
            if key_index == -1:
                if bool(self.smlm_data.locdata):
                    self._loc_property_combobox.setCurrentIndex(0)
                else:
                    self._loc_property_combobox.setCurrentIndex(-1)
            else:
                self._loc_property_combobox.setCurrentIndex(key_index)
        self._loc_property_combobox_on_changed()

    def _loc_property_combobox_on_changed(self) -> None:
        self._plot_widget.axes.clear()
        self._plot_widget.canvas.draw()

    def _select_button_on_click(self) -> None:
        locdata = self.smlm_data.locdata
        if locdata is None:
            raise ValueError("There is no SMLM data available.")
        elif bool(locdata) is False:
            raise ValueError("Locdata is empty.")

        self._plot_widget.axes.clear()

        with progress() as progress_bar:
            progress_bar.set_description("Running LocalizationProperty")
            lp = lc.LocalizationProperty(
                loc_property=self._loc_property_combobox.currentText()
            ).compute(locdata)
            lp.hist(ax=self._plot_widget.axes, fit=False)

        self._plot_widget.canvas.draw()
