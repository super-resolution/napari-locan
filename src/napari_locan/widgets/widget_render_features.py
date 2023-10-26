"""
Render selected features of a SMLM dataset.

A QWidget plugin to represent locdata features including centroid,
bounding box, oriented bounding box, convex hull and alpha shape.
"""
import logging

from napari.utils import progress
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QCheckBox,
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


class RenderFeaturesQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_size_buttons()
        self._add_centroid_check_box()
        self._add_bounding_box_check_box()
        self._add_oriented_bounding_box_check_box()
        self._add_convex_hull_check_box()
        self._add_alpha_shape_check_box()
        self._add_render_button()

        self._set_layout()

    def _add_size_buttons(self) -> None:
        self._size_spin_box_label = QLabel("size:")

        self._size_spin_box = QSpinBox()
        self._size_spin_box.setToolTip("Size of rendered shapes.")
        self._size_spin_box.setRange(1, 2147483647)
        self._size_spin_box.setValue(100)

        self._edge_width_spin_box_label = QLabel("width:")

        self._edge_width_spin_box = QSpinBox()
        self._edge_width_spin_box.setToolTip("Edge width of rendered shapes.")
        self._edge_width_spin_box.setRange(1, 2147483647)
        self._edge_width_spin_box.setValue(100)

        self._size_buttons_layout = QHBoxLayout()
        self._size_buttons_layout.addWidget(self._size_spin_box_label)
        self._size_buttons_layout.addWidget(self._size_spin_box)
        self._size_buttons_layout.addWidget(self._edge_width_spin_box_label)
        self._size_buttons_layout.addWidget(self._edge_width_spin_box)

    def _add_centroid_check_box(self) -> None:
        self._centroid_label = QLabel("Centroid:")

        self._centroid_check_box = QCheckBox()
        self._centroid_check_box.setToolTip("Show centroid of all localizations.")
        self._centroid_check_box.setChecked(False)

        self._centroid_layout = QHBoxLayout()
        self._centroid_layout.addWidget(self._centroid_label)
        self._centroid_layout.addWidget(self._centroid_check_box)

    def _add_bounding_box_check_box(self) -> None:
        self._bounding_box_label = QLabel("Bounding box:")

        self._bounding_box_check_box = QCheckBox()
        self._bounding_box_check_box.setToolTip(
            "Show bounding box of all localizations."
        )
        self._bounding_box_check_box.setChecked(False)

        self._bounding_box_layout = QHBoxLayout()
        self._bounding_box_layout.addWidget(self._bounding_box_label)
        self._bounding_box_layout.addWidget(self._bounding_box_check_box)

    def _add_oriented_bounding_box_check_box(self) -> None:
        self._oriented_bounding_box_label = QLabel("Oriented bounding box:")

        self._oriented_bounding_box_check_box = QCheckBox()
        self._oriented_bounding_box_check_box.setToolTip(
            "Show oriented bounding box of all localizations."
        )
        self._oriented_bounding_box_check_box.setChecked(False)

        self._oriented_bounding_box_layout = QHBoxLayout()
        self._oriented_bounding_box_layout.addWidget(self._oriented_bounding_box_label)
        self._oriented_bounding_box_layout.addWidget(
            self._oriented_bounding_box_check_box
        )

    def _add_convex_hull_check_box(self) -> None:
        self._convex_hull_label = QLabel("Convex hull:")

        self._convex_hull_check_box = QCheckBox()
        self._convex_hull_check_box.setToolTip("Show convex hull of all localizations.")
        self._convex_hull_check_box.setChecked(False)

        self._convex_hull_layout = QHBoxLayout()
        self._convex_hull_layout.addWidget(self._convex_hull_label)
        self._convex_hull_layout.addWidget(self._convex_hull_check_box)

    def _add_alpha_shape_check_box(self) -> None:
        self._alpha_shape_label = QLabel("Alpha shape:")

        self._alpha_shape_check_box = QCheckBox()
        self._alpha_shape_check_box.setToolTip("Show alpha shape of all localizations.")
        self._alpha_shape_check_box.setChecked(False)

        self._alpha_shape_spin_box_label = QLabel("alpha:")

        self._alpha_shape_spin_box = QSpinBox()
        self._alpha_shape_spin_box.setToolTip(
            "Alpha value to compute specific alpha shape."
        )
        self._alpha_shape_spin_box.setRange(1, 2147483647)
        self._alpha_shape_spin_box.setValue(100)

        self._alpha_shape_layout = QHBoxLayout()
        self._alpha_shape_layout.addWidget(self._alpha_shape_label)
        self._alpha_shape_layout.addWidget(self._alpha_shape_check_box)
        self._alpha_shape_layout.addWidget(self._alpha_shape_spin_box_label)
        self._alpha_shape_layout.addWidget(self._alpha_shape_spin_box)

    def _add_render_button(self) -> None:
        self._render_button = QPushButton("Render all")
        self._render_button.setToolTip(
            "Show the selected SMLM data features in new layers."
        )
        self._render_button.clicked.connect(self._render_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._size_buttons_layout)
        layout.addLayout(self._centroid_layout)
        layout.addLayout(self._bounding_box_layout)
        layout.addLayout(self._oriented_bounding_box_layout)
        layout.addLayout(self._convex_hull_layout)
        layout.addLayout(self._alpha_shape_layout)
        layout.addWidget(self._render_button)
        self.setLayout(layout)

    def _render_button_on_click(self) -> None:
        locdata = self.smlm_data.locdata
        if locdata is None:
            raise ValueError("There is no SMLM data available.")

        if self._centroid_check_box.isChecked():
            self.viewer.add_points(
                data=locdata.centroid,
                name="centroid",
                symbol="x",
                size=self._size_spin_box.value(),
            )

        if (
            self._bounding_box_check_box.isChecked()
            and locdata.bounding_box is not None
        ):
            try:
                shapes = [locdata.bounding_box.region.points]
                self.viewer.add_shapes(
                    shapes,
                    shape_type="polygon",
                    name="bounding_box",
                    edge_width=self._edge_width_spin_box.value(),
                    edge_color="gray",
                    face_color="",
                )
            except NotImplementedError as exception:
                raise NotImplementedError(
                    "Region not available for plotting."
                ) from exception

        if (
            self._oriented_bounding_box_check_box.isChecked()
            and locdata.oriented_bounding_box is not None
        ):
            try:
                shapes = [locdata.oriented_bounding_box.region.points]
                self.viewer.add_shapes(
                    shapes,
                    shape_type="polygon",
                    name="oriented_bounding_box",
                    edge_width=self._edge_width_spin_box.value(),
                    edge_color="yellow",
                    face_color="",
                )
            except NotImplementedError as exception:
                raise NotImplementedError(
                    "Region not available for plotting."
                ) from exception

        if self._convex_hull_check_box.isChecked() and locdata.convex_hull is not None:
            try:
                shapes = [locdata.convex_hull.region.points]
                self.viewer.add_shapes(
                    shapes,
                    shape_type="polygon",
                    name="convex_hull",
                    edge_width=self._edge_width_spin_box.value(),
                    edge_color="white",
                    face_color="",
                )
            except NotImplementedError as exception:
                raise NotImplementedError(
                    "Region not available for plotting."
                ) from exception

        if (
            self._alpha_shape_check_box.isChecked()
            and self._get_message_feedback() is True
        ):
            with progress() as progress_bar:
                progress_bar.set_description("Processing alpha shape")
                alpha = self._alpha_shape_spin_box.value()
                locdata.update_alpha_shape(alpha)

            if locdata.alpha_shape is not None:
                try:
                    shapes = locdata.alpha_shape.region.points  # type: ignore[assignment]
                    self.viewer.add_shapes(
                        shapes,
                        shape_type="polygon",
                        name="alpha_shape",
                        edge_width=self._edge_width_spin_box.value(),
                        edge_color="blue",
                        face_color="",
                    )
                except NotImplementedError as exception:
                    raise NotImplementedError(
                        "Region not available for plotting."
                    ) from exception

    def _get_message_feedback(self) -> bool:
        n_localizations = len(self.smlm_data.locdata)  # type: ignore
        if n_localizations < 10_000:
            run_computation = True
        else:
            msgBox = QMessageBox()
            msgBox.setText(
                f"There are {n_localizations} localizations. "
                f"The alpha shape computation will take some time."
            )
            msgBox.setInformativeText("Do you want to run the computation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            return_value = msgBox.exec()
            run_computation = bool(return_value == QMessageBox.Ok)
        return run_computation
