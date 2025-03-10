"""
Save and load the current state of napari-locan.

QWidget plugin to save and load the napari-locan state,
which currently includes the following data models

1) filter_specifications
2) region_specifications
3) roi_specifications
4) smlm_data

The data is serialized by the pickle module using protocol 5.
"""

import logging
import pickle
from pathlib import Path
from typing import Any

from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from napari_locan import (
    filter_specifications,
    region_specifications,
    roi_specifications,
    smlm_data,
)
from napari_locan.data_model.filter_specifications import FilterSpecifications
from napari_locan.data_model.region_specifications import RegionSpecifications
from napari_locan.data_model.roi_specifications import RoiSpecifications
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class NapariLocanProjectQWidget(QWidget):  # type: ignore
    def __init__(
        self,
        napari_viewer: Viewer,
        filter_specifications: FilterSpecifications = filter_specifications,
        region_specifications: RegionSpecifications = region_specifications,
        roi_specifications: RoiSpecifications = roi_specifications,
        smlm_data: SmlmData = smlm_data,
    ) -> None:
        super().__init__()
        self.viewer = napari_viewer
        self.filter_specifications = filter_specifications
        self.region_specifications = region_specifications
        self.roi_specifications = roi_specifications
        self.smlm_data = smlm_data

        self._add_buttons()
        self._set_layout()

    def _add_buttons(self) -> None:
        self._new_button = QPushButton("New")
        self._new_button.setToolTip("Clear all and start new napari-locan project.")
        self._new_button.clicked.connect(self._new_button_on_click)

        self._load_button = QPushButton("Load")
        self._load_button.setToolTip("Load napari-locan project from file.")
        self._load_button.clicked.connect(self._load_button_on_click)

        self._save_button = QPushButton("Save")
        self._save_button.setToolTip("Save current napari-locan project to file.")
        self._save_button.clicked.connect(self._save_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._new_button)
        self._buttons_layout.addWidget(self._load_button)
        self._buttons_layout.addWidget(self._save_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._buttons_layout)
        self.setLayout(layout)

    def _new_button_on_click(self) -> None:
        self.filter_specifications.delete_all()
        self.region_specifications.delete_all()
        self.roi_specifications.delete_all()
        self.smlm_data.delete_all()

    def _load_button_on_click(self) -> None:
        fname_ = QFileDialog.getOpenFileName(
            None,
            "Load napari_locan project from pickle file",
            "",
            filter="Pickle file (*.pickle)",
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )
        file_path = fname_[0] if isinstance(fname_, tuple) else str(fname_)
        with progress() as progress_bar:
            progress_bar.set_description("Loading data")
            with open(file_path, "rb") as file:
                napari_locan_state = pickle.load(file)  # noqa S301
        self._unpack_napari_locan_state(napari_locan_state=napari_locan_state)

    def _save_button_on_click(self) -> None:
        napari_locan_state = self._pack_napari_locan_state()

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)  # type: ignore[attr-defined]
        file_path_return = file_dialog.getSaveFileName(
            caption="Provide file name and path to save current project.",
            filter="Pickle file (*.pickle)",
        )
        file_path = Path(file_path_return[0])
        if file_path:
            with progress() as progress_bar:
                progress_bar.set_description("Saving data")
                with open(file_path, "wb") as file:
                    pickle.dump(napari_locan_state, file, protocol=5)

    def _pack_napari_locan_state(self) -> dict[str, Any]:
        napari_locan_state: dict[str, Any] = {}
        napari_locan_state["filter_specifications"] = self.filter_specifications
        napari_locan_state["region_specifications"] = self.region_specifications
        napari_locan_state["roi_specifications"] = self.roi_specifications
        napari_locan_state["smlm_data"] = self.smlm_data
        return napari_locan_state

    def _unpack_napari_locan_state(self, napari_locan_state: dict[str, Any]) -> None:
        # unpack filter_specifications
        self.filter_specifications._datasets = napari_locan_state[
            "filter_specifications"
        ]._datasets
        self.filter_specifications._names = napari_locan_state[
            "filter_specifications"
        ]._names
        self.filter_specifications._index = napari_locan_state[
            "filter_specifications"
        ]._index
        self.filter_specifications.names_changed_signal.emit(
            self.filter_specifications._names
        )
        self.filter_specifications.index_changed_signal.emit(
            self.filter_specifications._index
        )

        # unpack region_specifications
        self.region_specifications._datasets = napari_locan_state[
            "region_specifications"
        ]._datasets
        self.region_specifications._names = napari_locan_state[
            "region_specifications"
        ]._names
        self.region_specifications._index = napari_locan_state[
            "region_specifications"
        ]._index
        self.region_specifications.names_changed_signal.emit(
            self.region_specifications._names
        )
        self.region_specifications.index_changed_signal.emit(
            self.region_specifications._index
        )

        # unpack roi_specifications
        self.roi_specifications._datasets = napari_locan_state[
            "roi_specifications"
        ]._datasets
        self.roi_specifications._names = napari_locan_state["roi_specifications"]._names
        self.roi_specifications._index = napari_locan_state["roi_specifications"]._index
        self.roi_specifications.names_changed_signal.emit(
            self.roi_specifications._names
        )
        self.roi_specifications.index_changed_signal.emit(
            self.roi_specifications._index
        )

        # unpack smlm_data
        self.smlm_data._locdatas = napari_locan_state["smlm_data"]._locdatas
        self.smlm_data._locdata_names = napari_locan_state["smlm_data"]._locdata_names
        self.smlm_data._index = napari_locan_state["smlm_data"]._index
        self.smlm_data.locdata_names_changed_signal.emit(self.smlm_data._locdata_names)
        self.smlm_data.index_changed_signal.emit(self.smlm_data._index)
