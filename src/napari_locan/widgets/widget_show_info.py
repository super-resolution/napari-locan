"""
Show information for a SMLM dataset.

QWidget plugin for showing additional information
for a single SMLM dataset.
"""

import logging
from collections.abc import Iterable

import locan as lc
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class ShowInfoQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_information_meta()
        self._add_information_collection()
        self._add_information_selection()
        self._add_information_coordinate_dimension()
        self._add_information_localization_count()
        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)
        self._set_layout()

    def _add_information_meta(self) -> None:
        self._information_meta_checkbox = QCheckBox("has metadata.")
        self._information_meta_checkbox.setDisabled(True)
        self._information_meta_checkbox.setToolTip(
            "If checked the Locdata instance has a meta attribute that is not none."
        )

        self.smlm_data.index_changed_signal.connect(self._update_information_meta)

        self._information_meta_layout = QHBoxLayout()
        self._information_meta_layout.addWidget(self._information_meta_checkbox)

    def _add_information_collection(self) -> None:
        self._information_collection_checkbox = QCheckBox("is a collection.")
        self._information_collection_checkbox.setDisabled(True)
        self._information_collection_checkbox.setToolTip(
            "If checked the LocData instance has a reference attribute with a collection of other LocData instances."
        )

        self.smlm_data.index_changed_signal.connect(self._update_information_collection)

        self._information_collection_layout = QHBoxLayout()
        self._information_collection_layout.addWidget(
            self._information_collection_checkbox
        )

    def _add_information_selection(self) -> None:
        self._information_selection_checkbox = QCheckBox("is a selection.")
        self._information_selection_checkbox.setDisabled(True)
        self._information_selection_checkbox.setToolTip(
            "If checked the LocData instance has a reference attribute with a selection for other LocData instances."
        )

        self.smlm_data.index_changed_signal.connect(self._update_information_selection)

        self._information_selection_layout = QHBoxLayout()
        self._information_selection_layout.addWidget(
            self._information_selection_checkbox
        )

    def _add_information_coordinate_dimension(self) -> None:
        self._information_coordinate_dimension_text_edit = QLabel()
        self._information_coordinate_dimension_label = QLabel(
            "Coordinate dimension is:"
        )
        self._information_coordinate_dimension_label.setToolTip(
            "Number of coordinates available for each localization (i.e. size of coordinate_keys)."
        )

        self.smlm_data.index_changed_signal.connect(
            self._update_information_coordinate_dimension
        )

        self._information_coordinate_dimension_layout = QHBoxLayout()
        self._information_coordinate_dimension_layout.addWidget(
            self._information_coordinate_dimension_label
        )
        self._information_coordinate_dimension_layout.addWidget(
            self._information_coordinate_dimension_text_edit
        )

    def _add_information_localization_count(self) -> None:
        self._information_localization_count_text_edit = QLabel()
        self._information_localization_count_label = QLabel("Number of localizations:")
        self._information_localization_count_label.setToolTip(
            "Total number of localizations in SMLM dataset."
        )

        self.smlm_data.index_changed_signal.connect(
            self._update_localization_count_dimension
        )

        self._information_localization_count_layout = QHBoxLayout()
        self._information_localization_count_layout.addWidget(
            self._information_localization_count_label
        )
        self._information_localization_count_layout.addWidget(
            self._information_localization_count_text_edit
        )

    def _update_information_meta(self) -> None:
        if (
            self.smlm_data.index != -1
            and self.smlm_data.locdata is not None
            and self.smlm_data.locdata.meta is not None
        ):
            self._information_meta_checkbox.setChecked(True)
        else:
            self._information_meta_checkbox.setChecked(False)

    def _update_information_collection(self) -> None:
        if (
            self.smlm_data.index != -1
            and self.smlm_data.locdata is not None
            and self.smlm_data.locdata.references is not None
            and isinstance(self.smlm_data.locdata.references, Iterable)
        ):
            self._information_collection_checkbox.setChecked(True)
        else:
            self._information_collection_checkbox.setChecked(False)

    def _update_information_selection(self) -> None:
        if (
            self.smlm_data.index != -1
            and self.smlm_data.locdata is not None
            and self.smlm_data.locdata.references is not None
            and isinstance(self.smlm_data.locdata.references, lc.LocData)
        ):
            self._information_selection_checkbox.setChecked(True)
        else:
            self._information_selection_checkbox.setChecked(False)

    def _update_information_coordinate_dimension(self) -> None:
        if self.smlm_data.index != -1 and self.smlm_data.locdata is not None:
            self._information_coordinate_dimension_text_edit.setNum(
                self.smlm_data.locdata.dimension
            )
        else:
            self._information_coordinate_dimension_text_edit.clear()

    def _update_localization_count_dimension(self) -> None:
        if self.smlm_data.index != -1 and self.smlm_data.locdata is not None:
            self._information_localization_count_text_edit.setNum(
                self.smlm_data.locdata.properties["localization_count"]
            )
        else:
            self._information_localization_count_text_edit.clear()

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._information_meta_layout)
        layout.addLayout(self._information_collection_layout)
        layout.addLayout(self._information_selection_layout)
        layout.addLayout(self._information_coordinate_dimension_layout)
        layout.addLayout(self._information_localization_count_layout)
        self.setLayout(layout)
