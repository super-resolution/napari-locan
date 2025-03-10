"""
Select localizations from SMLM dataset.

A QWidget plugin to select localizations in current SMLM dataset based on a
filter specification.
A new SMLM dataset will be created.
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
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import filter_specifications, smlm_data
from napari_locan.data_model.filter_specifications import FilterSpecifications
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class SelectQWidget(QWidget):  # type: ignore[misc]
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
        if self.filter_specifications.dataset is None:
            self.filter_specifications.append_item(dataset={})

        self._add_loc_property_selector()
        self._add_selection_tools()
        self._add_condition_text()
        self._add_buttons()

        self._connect_loc_property_selector()
        self._connect_selection_tools()
        self._connect_condition_text()
        self._connect_buttons()

        self._init_widget_values()

        self._set_layout()

    def _add_loc_property_selector(self) -> None:
        self._loc_property_label = QLabel("Localization property:")
        self._loc_property_combobox = QComboBox()
        self._loc_property_combobox.setToolTip(
            "Choose localization property for selected SMLM dataset and selected filter specifications."
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
        self.filter_specifications.index_changed_signal.connect(
            self._loc_property_combobox_slot_for_filter_specifications_index
        )
        self._loc_property_combobox.currentIndexChanged.connect(
            self._loc_property_combobox_on_changed
        )

    def _add_selection_tools(self) -> None:
        self._lower_bound_label = QLabel("Min:")
        self._lower_bound_spinbox = QDoubleSpinBox()
        self._upper_bound_label = QLabel("Max:")
        self._upper_bound_spinbox = QDoubleSpinBox()
        self._apply_checkbox = QCheckBox("Apply")
        self._apply_checkbox.setToolTip("Set selection to current settings.")

        self._selection_tools_layout = QHBoxLayout()
        self._selection_tools_layout.addWidget(self._lower_bound_label)
        self._selection_tools_layout.addWidget(self._lower_bound_spinbox)
        self._selection_tools_layout.addWidget(self._upper_bound_label)
        self._selection_tools_layout.addWidget(self._upper_bound_spinbox)
        self._selection_tools_layout.addWidget(self._apply_checkbox)

    def _connect_selection_tools(self) -> None:
        self._lower_bound_spinbox.valueChanged.connect(
            self._lower_bound_spinbox_on_changed
        )
        self._upper_bound_spinbox.valueChanged.connect(
            self._upper_bound_spinbox_on_changed
        )
        self._apply_checkbox.stateChanged.connect(self._apply_checkbox_on_changed)

    def _add_condition_text(self) -> None:
        self._condition_text_label = QLabel("Condition:")
        self._condition_text_edit = QPlainTextEdit()
        self._condition_text_edit.setReadOnly(True)

        self._condition_text_layout = QVBoxLayout()
        self._condition_text_layout.addWidget(self._condition_text_label)
        self._condition_text_layout.addWidget(self._condition_text_edit)

    def _connect_condition_text(self) -> None:
        self.filter_specifications.index_changed_signal.connect(
            self._filter_specifications_index_on_changed
        )

    def _add_buttons(self) -> None:
        self._select_button = QPushButton("Select")
        self._select_button.setToolTip(
            "Filter the selected SMLM data according to the condition and keep "
            "selection as new SMLM dataset."
        )

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._select_button)

    def _connect_buttons(self) -> None:
        self._select_button.clicked.connect(self._select_button_on_click)

    def _init_widget_values(self) -> None:
        try:
            self._loc_property_combobox.setCurrentIndex(0)
        except IndexError:
            self._loc_property_combobox.setCurrentIndex(-1)
        self._loc_property_combobox_on_changed()
        self._update_condition_text()

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._loc_property_selector_layout)
        layout.addLayout(self._selection_tools_layout)
        layout.addLayout(self._condition_text_layout)
        layout.addLayout(self._buttons_layout)
        self.setLayout(layout)

    def _loc_property_combobox_slot_for_smlm_data_index(self, index: int) -> None:
        key_index = self._loc_property_combobox.currentIndex()
        self._loc_property_combobox.clear()
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
        if self.filter_specifications.dataset is not None:
            self._loc_property_combobox.addItems(
                self.filter_specifications.dataset.keys()
            )

    def _loc_property_combobox_slot_for_filter_specifications_index(self) -> None:
        if self.filter_specifications.index == -1:
            self._loc_property_combobox.clear()
        else:
            self._loc_property_combobox_slot_for_smlm_data_index(
                index=self.smlm_data.index
            )

    def _loc_property_combobox_on_changed(self) -> None:
        if self._loc_property_combobox.currentIndex() == -1:
            self._lower_bound_spinbox.setHidden(True)
            self._upper_bound_spinbox.setHidden(True)
            self._apply_checkbox.setHidden(True)
        else:
            self._lower_bound_spinbox.setHidden(False)
            self._upper_bound_spinbox.setHidden(False)
            self._apply_checkbox.setHidden(False)

            loc_property = self._loc_property_combobox.currentText()
            min_, max_ = self._get_spinbox_boundaries()
            self._lower_bound_spinbox.setRange(min_, max_)
            self._upper_bound_spinbox.setRange(min_, max_)

            if loc_property in self.filter_specifications.dataset:  # type: ignore[operator]
                self._lower_bound_spinbox.setValue(
                    self.filter_specifications.dataset[loc_property].lower_bound  # type: ignore[index]
                )
                self._upper_bound_spinbox.setValue(
                    self.filter_specifications.dataset[loc_property].upper_bound  # type: ignore[index]
                )
                self._apply_checkbox.setChecked(
                    self.filter_specifications.dataset[loc_property].activate  # type: ignore[index]
                )
            else:
                self._lower_bound_spinbox.setValue(
                    self.smlm_data.locdata.data[loc_property].min()  # type: ignore[union-attr]
                )
                self._upper_bound_spinbox.setValue(
                    self.smlm_data.locdata.data[loc_property].max()  # type: ignore[union-attr]
                )
                self._apply_checkbox.setChecked(False)

    def _get_spinbox_boundaries(self) -> tuple[float, float]:
        loc_property = self._loc_property_combobox.currentText()
        if self.smlm_data.locdata is None:
            min_, max_ = 0, 0
        else:
            min_value = self.smlm_data.locdata.data[loc_property].min()
            max_value = self.smlm_data.locdata.data[loc_property].max()
            min_ = min_value * 10 if min_value < 0 else 0
            max_ = max_value * 10
        return min_, max_

    def _filter_specifications_index_on_changed(self) -> None:
        if self.filter_specifications.index == -1:
            self._loc_property_combobox.setCurrentIndex(-1)
        else:
            if (
                self._loc_property_combobox.currentText()
                not in self.filter_specifications.dataset  # type: ignore[operator]
            ):
                self._loc_property_combobox.setCurrentIndex(0)
            else:
                loc_property = self._loc_property_combobox.currentText()
                self._lower_bound_spinbox.setValue(
                    self.filter_specifications.dataset[loc_property].lower_bound  # type: ignore[index]
                )
                self._upper_bound_spinbox.setValue(
                    self.filter_specifications.dataset[loc_property].upper_bound  # type: ignore[index]
                )
                self._apply_checkbox.setChecked(
                    self.filter_specifications.dataset[loc_property].activate  # type: ignore[index]
                )

        self._update_condition_text()

    def _apply_checkbox_on_changed(self) -> None:
        loc_property = self._loc_property_combobox.currentText()
        if self._loc_property_combobox.currentIndex() != -1:
            try:
                self.filter_specifications.dataset[  # type: ignore[index]
                    loc_property
                ].activate = self._apply_checkbox.isChecked()
            except KeyError:
                selector = lc.Selector(
                    loc_property=loc_property,
                    activate=self._apply_checkbox.isChecked(),
                    lower_bound=self._lower_bound_spinbox.value(),
                    upper_bound=self._upper_bound_spinbox.value(),
                )
                self.filter_specifications.dataset[loc_property] = selector  # type: ignore[index]
            self._update_condition_text()

    def _lower_bound_spinbox_on_changed(self) -> None:
        loc_property = self._loc_property_combobox.currentText()
        if self._loc_property_combobox.currentIndex() != -1:
            try:
                self.filter_specifications.dataset[  # type: ignore[index]
                    loc_property
                ].lower_bound = self._lower_bound_spinbox.value()
            except KeyError:
                selector = lc.Selector(
                    loc_property=loc_property,
                    activate=self._apply_checkbox.isChecked(),
                    lower_bound=self._lower_bound_spinbox.value(),
                    upper_bound=self._upper_bound_spinbox.value(),
                )
                self.filter_specifications.dataset[loc_property] = selector  # type: ignore[index]
            self._update_condition_text()

    def _upper_bound_spinbox_on_changed(self) -> None:
        loc_property = self._loc_property_combobox.currentText()
        if self._loc_property_combobox.currentIndex() != -1:
            try:
                self.filter_specifications.dataset[  # type: ignore[index]
                    loc_property
                ].upper_bound = self._upper_bound_spinbox.value()
            except KeyError:
                selector = lc.Selector(
                    loc_property=loc_property,
                    activate=self._apply_checkbox.isChecked(),
                    lower_bound=self._lower_bound_spinbox.value(),
                    upper_bound=self._upper_bound_spinbox.value(),
                )
                self.filter_specifications.dataset[loc_property] = selector  # type: ignore[index]
            self._update_condition_text()

    def _update_condition_text(self) -> None:
        if self.filter_specifications.index != -1:
            text = self.filter_specifications.filter_condition
            self._condition_text_edit.setPlainText(text)
        else:
            self._condition_text_edit.setPlainText("")

    def _select_button_on_click(self) -> None:
        locdata = self.smlm_data.locdata
        if locdata is None:
            raise ValueError("There is no SMLM data available.")
        elif bool(locdata) is False:
            raise ValueError("Locdata is empty.")

        if not self.filter_specifications.filter_condition:
            raise ValueError("Filter condition cannot be an empty string.")

        with progress() as progress_bar:
            progress_bar.set_description("Selecting:")
            new_locdata = lc.select_by_condition(
                locdata=locdata, condition=self.filter_specifications.filter_condition
            )
            self.smlm_data.append_item(
                locdata=new_locdata,
                locdata_name=new_locdata.meta.identifier + "-selection",
            )
