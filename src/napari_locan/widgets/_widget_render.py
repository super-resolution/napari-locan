"""
QWidget plugin to render SMLM data
"""
from pathlib import Path

import locan as lc
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class RenderQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer):
        super().__init__()
        self.viewer = napari_viewer

        self._add_file_type()
        self._add_file_path()
        self._add_bin_size()
        self._add_bin_range()
        self._add_rescale()
        self._add_buttons()
        self._set_layout()

    def _add_file_type(self) -> None:
        self._file_type_label = QLabel("File type:")
        self._file_type_combobox = QComboBox()
        file_types = list(lc.FileType.__members__.keys())
        self._file_type_combobox.addItems(file_types)
        self._file_type_combobox.setCurrentIndex(lc.FileType.RAPIDSTORM.value)

        self._file_type_layout = QHBoxLayout()
        self._file_type_layout.addWidget(self._file_type_label)
        self._file_type_layout.addWidget(self._file_type_combobox)

    def _add_file_path(self) -> None:
        self._file_path_label = QLabel("File path:")
        self._file_path_edit = QLineEdit()
        self._file_path_select_button = QPushButton("Select")
        self._file_path_select_button.setStatusTip("Select a file path.")
        self._file_path_select_button.clicked.connect(
            self._file_path_select_button_on_click
        )

        self._file_path_layout = QHBoxLayout()
        self._file_path_layout.addWidget(self._file_path_label)
        self._file_path_layout.addWidget(self._file_path_edit)
        self._file_path_layout.addWidget(self._file_path_select_button)

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
        # rescale = {"label": "Rescale intensity"},
        self._rescale_label = QLabel("Rescale intensity:")
        self._rescale_combobox = QComboBox()
        trafos = list(lc.Trafo.__members__.keys())
        self._rescale_combobox.addItems(trafos)
        self._rescale_combobox.setCurrentIndex(lc.Trafo.EQUALIZE.value)

        self._rescale_layout = QHBoxLayout()
        self._rescale_layout.addWidget(self._rescale_label)
        self._rescale_layout.addWidget(self._rescale_combobox)

    def _add_buttons(self) -> None:
        self._load_button = QPushButton("Load File")
        self._load_button.setStatusTip(
            "Load and display the selected file in new layer."
        )
        self._load_button.clicked.connect(self._load_button_on_click)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._file_type_layout)
        layout.addLayout(self._file_path_layout)
        layout.addLayout(self._bin_size_layout)
        layout.addLayout(self._bin_range_layout)
        layout.addLayout(self._rescale_layout)
        layout.addWidget(self._load_button)
        self.setLayout(layout)

    def _file_path_select_button_on_click(self) -> None:
        fname_ = QFileDialog.getOpenFileName(
            None,
            "message",
            "",
            filter=""
            # kwargs: parent, message, directory, filter
            # but kw_names are different for different qt_bindings
        )
        fname = fname_[0] if isinstance(fname_, tuple) else str(fname_)
        self._file_path_edit.setText(fname)

    def _load_button_on_click(self) -> None:
        if not self._file_path_edit.text():
            self._file_path_select_button_on_click()

        file_path = self._file_path_edit.text()
        file_type = self._file_type_combobox.currentText()
        locdata = lc.load_locdata(path=file_path, file_type=file_type)

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
        add_kwargs = {"name": Path(file_path).stem}

        # render data
        lc.render_2d_napari(
            locdata=locdata,
            viewer=self.viewer,
            bin_size=int(self._bin_size_spin_box.value()),
            bin_range=bin_range,
            rescale=self._rescale_combobox.currentText(),
            cmap=lc.COLORMAP_CONTINUOUS,
            **add_kwargs,
        )
