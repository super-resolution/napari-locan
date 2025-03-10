"""
Create regions of interest.

A QWidget plugin for managing regions of interest.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import locan as lc
import napari
from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import region_specifications, roi_specifications, smlm_data
from napari_locan.data_model.region_specifications import RegionSpecifications
from napari_locan.data_model.roi_specifications import RoiSpecifications
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class RoiQWidget(QWidget):  # type: ignore
    def __init__(
        self,
        napari_viewer: Viewer,
        region_specifications: RegionSpecifications = region_specifications,
        roi_specifications: RoiSpecifications = roi_specifications,
        smlm_data: SmlmData = smlm_data,
    ) -> None:
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data
        self.region_specifications = region_specifications
        self.roi_specifications = roi_specifications

        self._add_regions_widgets()
        self._add_regions_text()
        self._add_reference_widgets()
        self._add_locdatas_combobox()
        self._add_loc_properties_selection()
        self._add_rois_buttons()
        self._add_rois_combobox()
        self._add_roi_text()

        self._set_layout()

    def _add_regions_widgets(self) -> None:
        self._regions_label = QLabel()
        self._regions_label.setText("Regions:")
        self._regions_label.setToolTip(
            "Regions are created from shapes and are used to define ROIs."
        )
        self._delete_all_regions_button = QPushButton("Delete all")
        self._delete_all_regions_button.setToolTip("Delete all region specifications.")
        self._delete_all_regions_button.clicked.connect(
            self._delete_all_regions_button_on_click
        )

        self._delete_regions_button = QPushButton("Delete")
        self._delete_regions_button.setToolTip("Delete current region specifications.")
        self._delete_regions_button.clicked.connect(
            self._delete_regions_button_on_click
        )

        self._scale_layer_button = QPushButton("Reset scale")
        self._scale_layer_button.setToolTip(
            "Reset scale of the selected shapes layer. "
            "All shapes and point scales should typically have unit scale factors."
        )
        self._scale_layer_button.clicked.connect(self._scale_layer_button_on_click)

        self._get_regions_from_smlm_data_button = QPushButton("From SmlmData")
        self._get_regions_from_smlm_data_button.setToolTip(
            "Get region specifications from regions in the selected smlm dataset."
        )
        self._get_regions_from_smlm_data_button.clicked.connect(
            self._get_regions_from_smlm_data_button_on_click
        )

        self._get_regions_from_shapes_button = QPushButton("From shapes")
        self._get_regions_from_shapes_button.setToolTip(
            "Get region specifications from selected shapes layer."
        )
        self._get_regions_from_shapes_button.clicked.connect(
            self._get_regions_from_shapes_button_on_click
        )

        self._regions_combobox = QComboBox()
        self._regions_combobox.setToolTip("Region specifications.")
        self._connect_regions_combobox_and_region_specifications()

        self._regions_buttons_1_layout = QHBoxLayout()
        self._regions_buttons_1_layout.addWidget(self._delete_all_regions_button)
        self._regions_buttons_1_layout.addWidget(self._delete_regions_button)
        self._regions_buttons_1_layout.addWidget(self._scale_layer_button)

        self._regions_buttons_2_layout = QHBoxLayout()
        self._regions_buttons_2_layout.addWidget(
            self._get_regions_from_smlm_data_button
        )
        self._regions_buttons_2_layout.addWidget(self._get_regions_from_shapes_button)

        self._regions_widgets_layout = QVBoxLayout()
        self._regions_widgets_layout.addWidget(self._regions_label)
        self._regions_widgets_layout.addLayout(self._regions_buttons_1_layout)
        self._regions_widgets_layout.addLayout(self._regions_buttons_2_layout)
        self._regions_widgets_layout.addWidget(self._regions_combobox)

    def _connect_regions_combobox_and_region_specifications(self) -> None:
        self.region_specifications.names_changed_signal.connect(
            self._synchronize_region_specifications_to_combobox
        )
        self.region_specifications.names_changed_signal.emit(
            self.region_specifications.names
        )

        self.region_specifications.index_changed_signal.connect(
            self._regions_combobox.setCurrentIndex
        )
        self.region_specifications.index_changed_signal.emit(
            self.region_specifications.index
        )

        self._regions_combobox.currentIndexChanged.connect(
            self.region_specifications.set_index_slot
        )

    def _synchronize_region_specifications_to_combobox(self, names: list[str]) -> None:
        current_index = self.region_specifications.index
        self._regions_combobox.clear()
        self._regions_combobox.addItems(names)
        self._regions_combobox.setCurrentIndex(current_index)

    def _add_regions_text(self) -> None:
        self._regions_text_edit = QPlainTextEdit()
        self._regions_combobox.currentIndexChanged.connect(self._update_regions_text)

        self._regions_text_layout = QHBoxLayout()
        self._regions_text_layout.addWidget(self._regions_text_edit)

    def _update_regions_text(self) -> None:
        if self.region_specifications.index != -1:
            text = str(self.region_specifications.dataset)
            self._regions_text_edit.setPlainText(text)
        else:
            self._regions_text_edit.setPlainText("")

    def _add_reference_widgets(self) -> None:
        self._reference_label = QLabel()
        self._reference_label.setText("Reference:")
        self._reference_label.setToolTip(
            "The reference defines the dataset that a ROI refers to."
        )
        self._reference_combobox = QComboBox()
        self._reference_combobox.setToolTip("Choose as roi reference.")
        reference_items = ["None", "SmlmData", "File reference", "File dialog"]
        self._reference_combobox.addItems(reference_items)

        self._reference_widgets_layout = QVBoxLayout()
        self._reference_widgets_layout.addWidget(self._reference_label)
        self._reference_widgets_layout.addWidget(self._reference_combobox)

    def _add_loc_properties_selection(self) -> None:
        self._loc_properties_selection_label = QLabel()
        self._loc_properties_selection_label.setText("Localization properties:")
        self._loc_properties_selection_label.setToolTip(
            "Localization properties define the coordinates of a ROI."
        )
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

        self._loc_properties_comboboxes_layout = QHBoxLayout()
        self._loc_properties_comboboxes_layout.addWidget(self._loc_properties_x_label)
        self._loc_properties_comboboxes_layout.addWidget(
            self._loc_properties_x_combobox
        )
        self._loc_properties_comboboxes_layout.addWidget(self._loc_properties_y_label)
        self._loc_properties_comboboxes_layout.addWidget(
            self._loc_properties_y_combobox
        )

        self._loc_properties_layout = QVBoxLayout()
        self._loc_properties_layout.addWidget(self._loc_properties_selection_label)
        self._loc_properties_layout.addLayout(self._loc_properties_comboboxes_layout)

    def _add_locdatas_combobox(self) -> None:
        self._locdatas_label = QLabel()
        self._locdatas_label.setText("SMLM Data:")
        self._locdatas_label.setToolTip(
            "SmlmData that can be used as reference (linked to the SMLM Data widget)."
        )

        self._locdatas_combobox = QComboBox()
        self._locdatas_combobox.setToolTip("Choose SMLM dataset as roi reference.")
        self._connect_locdatas_combobox_and_smlm_data()

        self._locdatas_layout = QHBoxLayout()
        self._locdatas_layout.addWidget(self._locdatas_label)
        self._locdatas_layout.addWidget(self._locdatas_combobox)

    def _connect_locdatas_combobox_and_smlm_data(self) -> None:
        self.smlm_data.locdata_names_changed_signal.connect(
            self._synchronize_smlm_data_to_combobox
        )
        self.smlm_data.locdata_names_changed_signal.emit(self.smlm_data.locdata_names)

        self.smlm_data.index_changed_signal.connect(
            self._locdatas_combobox.setCurrentIndex
        )
        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)

        self._locdatas_combobox.currentIndexChanged.connect(
            self.smlm_data.set_index_slot
        )

    def _synchronize_smlm_data_to_combobox(self, locdata_names: list[str]) -> None:
        self._locdatas_combobox.clear()
        self._locdatas_combobox.addItems(locdata_names)

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

    def _add_rois_buttons(self) -> None:
        self._rois_label = QLabel()
        self._rois_label.setText("Regions of interest:")
        self._rois_label.setToolTip("Roi(reference, region, loc_properties).")

        self._delete_all_roi_button = QPushButton("Delete all")
        self._delete_all_roi_button.setToolTip("Delete all roi specifications.")
        self._delete_all_roi_button.clicked.connect(
            self._delete_all_roi_button_on_click
        )

        self._delete_roi_button = QPushButton("Delete")
        self._delete_roi_button.setToolTip("Delete roi specifications.")
        self._delete_roi_button.clicked.connect(self._delete_roi_button_on_click)

        self._load_roi_button = QPushButton("Load")
        self._load_roi_button.setToolTip("Load roi specifications from yaml file.")
        self._load_roi_button.clicked.connect(self._load_roi_button_on_click)

        self._save_roi_button = QPushButton("Save")
        self._save_roi_button.setToolTip("Save roi specifications to yaml file.")
        self._save_roi_button.clicked.connect(self._save_roi_button_on_click)

        self._apply_roi_button = QPushButton("Apply")
        self._apply_roi_button.setToolTip(
            "Create new SMLM dataset from roi specifications."
        )
        self._apply_roi_button.clicked.connect(self._apply_roi_button_on_click)

        self._create_roi_button = QPushButton("Create")
        self._create_roi_button.setToolTip(
            "Create roi specifications from current region."
        )
        self._create_roi_button.clicked.connect(self._create_roi_button_on_click)

        self._rois_buttons_layout_0 = QHBoxLayout()
        self._rois_buttons_layout_0.addWidget(self._delete_all_roi_button)
        self._rois_buttons_layout_0.addWidget(self._delete_roi_button)
        self._rois_buttons_layout_0.addWidget(self._load_roi_button)
        self._rois_buttons_layout_0.addWidget(self._save_roi_button)

        self._rois_buttons_layout_1 = QHBoxLayout()
        self._rois_buttons_layout_1.addWidget(self._create_roi_button)
        self._rois_buttons_layout_1.addWidget(self._apply_roi_button)

        self._rois_buttons_layout = QVBoxLayout()
        self._rois_buttons_layout.addWidget(self._rois_label)
        self._rois_buttons_layout.addLayout(self._rois_buttons_layout_0)
        self._rois_buttons_layout.addLayout(self._rois_buttons_layout_1)

    def _add_rois_combobox(self) -> None:
        self._rois_combobox = QComboBox()
        self._rois_combobox.setToolTip("Roi specifications.")
        self._connect_rois_combobox_and_roi_specifications()

        self._rois_combobox_layout = QHBoxLayout()
        self._rois_combobox_layout.addWidget(self._rois_combobox)

    def _connect_rois_combobox_and_roi_specifications(self) -> None:
        self.roi_specifications.names_changed_signal.connect(
            self._synchronize_roi_specifications_to_combobox
        )
        self.roi_specifications.names_changed_signal.emit(self.roi_specifications.names)

        self.roi_specifications.index_changed_signal.connect(
            self._rois_combobox.setCurrentIndex
        )
        self.roi_specifications.index_changed_signal.emit(self.roi_specifications.index)

        self._rois_combobox.currentIndexChanged.connect(
            self.roi_specifications.set_index_slot
        )

    def _synchronize_roi_specifications_to_combobox(self, names: list[str]) -> None:
        current_index = self.roi_specifications.index
        self._rois_combobox.clear()
        self._rois_combobox.addItems(names)
        self._rois_combobox.setCurrentIndex(current_index)

    def _add_roi_text(self) -> None:
        self._roi_text_edit = QPlainTextEdit()
        self._rois_combobox.currentIndexChanged.connect(self._update_roi_text)

        self._roi_text_layout = QHBoxLayout()
        self._roi_text_layout.addWidget(self._roi_text_edit)

    def _update_roi_text(self) -> None:
        if self.roi_specifications.dataset is not None:
            text = str(self.roi_specifications.dataset)  # type: ignore
            self._roi_text_edit.setPlainText(text)
        else:
            self._roi_text_edit.setPlainText("")

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._reference_widgets_layout)
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._locdatas_layout)
        layout.addLayout(self._regions_widgets_layout)
        layout.addLayout(self._regions_text_layout)
        layout.addLayout(self._rois_buttons_layout)
        layout.addLayout(self._rois_combobox_layout)
        layout.addLayout(self._roi_text_layout)
        self.setLayout(layout)

    def _delete_all_regions_button_on_click(self) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Do you really want to delete ALL regions?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
        msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:  # type: ignore[attr-defined]
            self.region_specifications.delete_all()
        else:
            return

    def _delete_regions_button_on_click(self) -> None:
        self.region_specifications.delete_item()

    def _scale_layer_button_on_click(self) -> None:
        """
        Reset scale to 1.
        The scale factor of a shapes layer is sometimes different from 1
        depending on the layer creation history.
        """
        shapes_layer = self._get_current_shapes_layer()
        shapes_layer.scale = tuple(1 for i in range(shapes_layer.ndim))

    def _get_regions_from_smlm_data_button_on_click(self) -> None:
        if self.smlm_data.locdata is None:
            raise ValueError("There is nto smlm dataset available.")

        # items = ["region", "bounding_box", "convex_hull", "alpha_shape"]
        items = ["region", "bounding_box", "convex_hull", "alpha_shape"]
        item, ok = QInputDialog().getItem(
            self,
            "Choose region or hull...",
            "LocData attribute:",
            items,
            0,
            False,
        )
        if not ok:
            return
        else:
            if item == "region":
                if self.smlm_data.locdata.region is None:
                    napari.utils.notifications.show_info(
                        "smlm_data.locdata.region is None."
                    )
                    new_region = None
                else:
                    new_region = self.smlm_data.locdata.region
            elif item == "bounding_box":
                if (
                    self.smlm_data.locdata.bounding_box is None
                    or isinstance(self.smlm_data.locdata.bounding_box, lc.EmptyRegion)
                    or self.smlm_data.locdata.convex_hull is None
                ):
                    napari.utils.notifications.show_info(
                        "self.smlm_data.locdata.bounding_box.region is not available."
                    )
                    new_region = None
                else:
                    new_region = self.smlm_data.locdata.bounding_box.region
            elif item == "convex_hull":
                if (
                    self.smlm_data.locdata.convex_hull is None
                    or self.smlm_data.locdata.convex_hull.region is None
                ):
                    napari.utils.notifications.show_info(
                        "smlm_data.locdata.convex_hull.region is not available."
                    )
                    new_region = None
                else:
                    new_region = self.smlm_data.locdata.convex_hull.region
            elif item == "alpha_shape":
                if (
                    self.smlm_data.locdata.alpha_shape is None
                    or self.smlm_data.locdata.alpha_shape.region is None
                ):
                    napari.utils.notifications.show_info(
                        "smlm_data.locdata.alpha_shape.region is not available."
                    )
                    new_region = None
                else:
                    new_region = self.smlm_data.locdata.alpha_shape.region
            else:
                raise AttributeError

        if new_region is not None:
            identifier_ = self.roi_specifications.count + 1
            repr_ = repr(new_region).split("(")[0]
            name_ = f"{identifier_}-{repr_}"
            self.region_specifications.append_item(dataset=new_region, name=name_)

    def _get_regions_from_shapes_button_on_click(self) -> None:
        shapes_layer = self._get_current_shapes_layer()
        shapes_data = shapes_layer.as_layer_data_tuple()

        new_regions = lc.visualize.render_napari.utilities._shapes_to_regions(
            shapes_data=shapes_data
        )
        repr_list = [repr(item_).split("(")[0] for item_ in new_regions]
        region_identifier = range(
            self.roi_specifications.count + 1,
            self.roi_specifications.count + 1 + len(new_regions),
        )
        names_list = [f"{i}-{repr_}" for i, repr_ in zip(region_identifier, repr_list)]
        for region_, name_ in zip(new_regions, names_list):
            self.region_specifications.append_item(dataset=region_, name=name_)

    def _delete_all_roi_button_on_click(self) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Do you really want to delete ALL roi specifications?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
        msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:  # type: ignore[attr-defined]
            self.roi_specifications.delete_all()
        else:
            return

    def _delete_roi_button_on_click(self) -> None:
        self.roi_specifications.delete_item()

    def _load_roi_button_on_click(
        self, value: bool = False, file_path: str | os.PathLike[Any] | None = None
    ) -> None:
        if file_path is None:
            fname = QFileDialog.getOpenFileName(
                None,
                "Open roi file...",
                "",
                filter="ROI file (*.yaml);; All files (*)",
                # kwargs: parent, message, directory, filter
                # but kw_names are different for different qt_bindings
            )
            new_file_path = Path(fname[0]) if isinstance(fname, tuple) else Path(fname)  # type: ignore[arg-type]
        else:
            new_file_path = Path(file_path)
        new_roi = lc.Roi.from_yaml(path=new_file_path)
        self.roi_specifications.append_item(
            dataset=new_roi, name=f"roi_{self.roi_specifications.count + 1}"
        )

    def _save_roi_button_on_click(self) -> None:
        if self.roi_specifications.dataset is None:
            raise KeyError("No item available to save.")
        else:
            roi = self.roi_specifications.dataset

            # choose file interactively
            file_path = None if roi.reference is None else "roi_reference"
            if file_path is None:
                fname = QFileDialog.getSaveFileName(
                    None,
                    "Set file path and base name...",
                    "",
                    filter="ROI file (*.yaml);; All files (*)",
                    # options=QFileDialog.DontConfirmOverwrite
                    # kwargs: parent, message, directory, filter
                    # but kw_names are different for different qt_bindings
                )
                if isinstance(fname, tuple):
                    new_file_path = Path(fname[0])
                else:
                    new_file_path = Path(fname)
            elif file_path == "roi_reference":
                new_file_path = None
            elif Path(file_path).is_dir():
                new_file_path = Path(file_path) / "my"  # just a simple name
            else:
                new_file_path = Path(file_path)

            # create roi file name and save roi
            if new_file_path is None:
                try:
                    new_file_path = Path(
                        roi.reference.file.path  # type: ignore[union-attr]
                    )
                except AttributeError:
                    raise
            roi_file = (
                new_file_path.stem + "_" + self._rois_combobox.currentText() + ".yaml"
            )
            roi_path = new_file_path.with_name(roi_file)

            fname_ = QFileDialog.getSaveFileName(
                None,
                "Save roi file as...",
                str(roi_path),
                filter="ROI file (*.yaml);; All files (*)",
                # kwargs: parent, message, directory, filter
                # but kw_names are different for different qt_bindings
            )
            fname = fname_[0] if isinstance(fname_, tuple) else str(fname_)  # type: ignore[assignment]
            roi_path = Path(fname)  # type: ignore[arg-type]

            roi.to_yaml(path=roi_path)

            napari.utils.notifications.show_info(f"Roi file was saved as: {roi_path}")

    def _apply_roi_button_on_click(self) -> None:
        if self.roi_specifications.dataset is None:
            raise KeyError("No item available to apply.")
        else:
            roi = self.roi_specifications.dataset
            with progress() as progress_bar:
                progress_bar.set_description("Selecting roi:")
                new_locdata = roi.locdata()
                self.smlm_data.append_item(
                    locdata=new_locdata,
                    locdata_name=new_locdata.meta.identifier
                    + "-"
                    + self._rois_combobox.currentText(),
                    set_index=False,
                )

    def _create_roi_button_on_click(self) -> None:
        if self.region_specifications.dataset is None:
            raise LookupError(
                "There is no region available. Please provide a valid region."
            )

        reference: (
            lc.LocData
            | dict[str, Any]
            | lc.data.metadata_pb2.Metadata
            | lc.data.metadata_pb2.File
            | None
        )
        if self._reference_combobox.currentText() == "None":
            reference = None
        elif self._reference_combobox.currentText() == "SmlmData":
            reference = self.smlm_data.locdata  # type: ignore
        elif self._reference_combobox.currentText() == "File reference":
            reference = self.smlm_data.locdata.meta.file  # type: ignore
        elif self._reference_combobox.currentText() == "File dialog":
            reference = {}
            fname = QFileDialog.getSaveFileName(
                None,
                "Select localization file as roi reference...",
                "",
                filter="",
                options=QFileDialog.DontConfirmOverwrite,  # type: ignore[attr-defined]
                # kwargs: parent, message, directory, filter
                # but kw_names are different for different qt_bindings
            )
            file_path = Path(fname[0]) if isinstance(fname, tuple) else Path(fname)  # type: ignore[arg-type]
            reference["file_path"] = file_path

            items = [member.name for member in lc.FileType]
            item, ok = QInputDialog().getItem(
                self,
                "Choose file type for roi reference...",
                "File type:",
                items,
                1,
                False,
            )
            if ok and item != lc.FileType.UNKNOWN_FILE_TYPE.name:
                reference["file_type"] = str(item)
            else:
                raise KeyError("A valid file type must be provided.")
        else:
            raise ValueError("Current choice of combobox is not supported.")

        loc_properties = [
            self._loc_properties_x_combobox.currentText(),
            self._loc_properties_y_combobox.currentText(),
        ]

        new_roi = lc.Roi(
            reference=reference,
            region=self.region_specifications.dataset,
            loc_properties=loc_properties,
        )
        self.roi_specifications.append_item(
            dataset=new_roi, name=f"roi_{self.roi_specifications.count + 1}"
        )

    def _get_current_shapes_layer(self) -> napari.layers.Layer:
        """return a selected shapes layer or raise exception"""
        layer_selection = self.viewer.layers.selection
        if len(layer_selection) > 1:
            raise ValueError("You need to select a single shapes layer.")
        else:
            try:
                layer = layer_selection.pop()
                layer_selection.add(layer)
                if layer.as_layer_data_tuple()[-1] != "shapes":
                    raise KeyError("Selected layer ist not of type shapes")
            except KeyError as exception:
                raise KeyError("Please select a valid shapes layer.") from exception
        return layer
