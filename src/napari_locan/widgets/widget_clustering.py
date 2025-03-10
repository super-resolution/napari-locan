"""
Compute localization clusters.

QWidget plugin for clustering SMLM data.
More advanced clustering routines are available through locan-based scripts.
"""

import logging
from typing import Any

import locan as lc
from napari.qt.threading import thread_worker
from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class ClusteringQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_cluster_method_combobox()
        self._add_loc_properties_selection()
        self._add_parameter_definitions()
        self._add_buttons()
        self._set_layout()

    def _add_cluster_method_combobox(self) -> None:
        self._cluster_method_combobox = QComboBox()
        self._cluster_method_combobox.setToolTip("Choose clustering procedure.")
        self._cluster_method_combobox.addItem("DBSCAN")

        self._cluster_method_layout = QHBoxLayout()
        self._cluster_method_layout.addWidget(self._cluster_method_combobox)

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

    def _add_parameter_definitions(self) -> None:
        self._eps_label = QLabel("epsilon:")
        self._eps_spin_box = QSpinBox()
        self._eps_spin_box.setToolTip("Parameter for clustering procedure.")
        self._eps_spin_box.setValue(20)

        self._min_points_label = QLabel("min_points:")
        self._min_points_spin_box = QSpinBox()
        self._min_points_spin_box.setToolTip("Parameter for clustering procedure.")
        self._min_points_spin_box.setValue(3)

        self._parameter_definitions_layout = QHBoxLayout()
        self._parameter_definitions_layout.addWidget(self._eps_label)
        self._parameter_definitions_layout.addWidget(self._eps_spin_box)
        self._parameter_definitions_layout.addWidget(self._min_points_label)
        self._parameter_definitions_layout.addWidget(self._min_points_spin_box)

    def _add_buttons(self) -> None:
        self._compute_button = QPushButton("Compute")
        self._compute_button.setToolTip("Run the clustering procedure.")
        self._compute_button.clicked.connect(self._compute_button_on_click)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._compute_button)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._cluster_method_layout)
        layout.addLayout(self._loc_properties_layout)
        layout.addLayout(self._parameter_definitions_layout)
        layout.addLayout(self._buttons_layout)
        self.setLayout(layout)

    def _compute_button_on_click_main_thread(self) -> None:
        if self.smlm_data.index == -1:
            raise ValueError("There is no smlm data available.")
        if self._get_message_feedback() is False:
            return

        eps_ = self._eps_spin_box.value()
        min_samples_ = self._min_points_spin_box.value()

        with progress() as progress_bar:
            progress_bar.set_description("Running cluster_dbscan")
            noise, clust = lc.cluster_dbscan(
                locdata=self.smlm_data.locdata, eps=eps_, min_samples=min_samples_  # type: ignore[arg-type]
            )
            self.smlm_data.append_item(
                locdata=noise, locdata_name=noise.meta.identifier + "-noise"
            )
            self.smlm_data.append_item(
                locdata=clust, locdata_name=clust.meta.identifier + "-cluster"
            )

    def _compute_button_on_click_thread_worker(self) -> None:
        if self.smlm_data.index == -1:
            raise ValueError("There is no smlm data available.")
        if self._get_message_feedback() is False:
            return

        eps_ = self._eps_spin_box.value()
        min_samples_ = self._min_points_spin_box.value()

        def worker_return(return_value: tuple[lc.LocData, lc.LocData]) -> None:
            noise, clust = return_value
            self.smlm_data.append_item(
                locdata=noise, locdata_name=noise.meta.identifier + "-noise"
            )
            self.smlm_data.append_item(
                locdata=clust, locdata_name=clust.meta.identifier + "-cluster"
            )

        worker = _cluster_dbscan_worker(
            locdata=self.smlm_data.locdata, eps=eps_, min_samples=min_samples_
        )
        worker.returned.connect(worker_return)
        worker.start()

    def _compute_button_on_click(self) -> None:
        self._compute_button_on_click_main_thread()
        # the thread worker seems to take >3x longer:
        # self._compute_button_on_click_thread_worker()

    def _get_message_feedback(self) -> bool:
        n_localizations = len(self.smlm_data.locdata)  # type: ignore
        if n_localizations < 10_000:
            run_computation = True
        else:
            msgBox = QMessageBox()
            msgBox.setText(
                f"There are {n_localizations} localizations. "
                f"The computation will take some time."
            )
            msgBox.setInformativeText("Do you want to run the computation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # type: ignore[attr-defined]
            msgBox.setDefaultButton(QMessageBox.Cancel)  # type: ignore[attr-defined]
            return_value = msgBox.exec()
            run_computation = bool(return_value == QMessageBox.Ok)  # type: ignore[attr-defined]
        return run_computation


@thread_worker(progress={"desc": "Running cluster_dbscan"})  # type: ignore[misc]
def _cluster_dbscan_worker(**kwargs: Any) -> tuple[lc.LocData, lc.LocData]:
    return_value = lc.cluster_dbscan(**kwargs)
    return return_value  # type: ignore[no-any-return]
