from copy import copy
from pathlib import Path

import locan as lc
import napari
import numpy as np
import pytest

from napari_locan import RoiQWidget
from napari_locan.data_model.region_specifications import RegionSpecifications
from napari_locan.data_model.roi_specifications import RoiSpecifications
from napari_locan.data_model.smlm_data import SmlmData


class TestRoiQWidgetQWidget:
    def test_RoiQWidget_init(self, make_napari_viewer, locdata_2d):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        assert len(my_widget.region_specifications.datasets) == 0
        assert len(my_widget.roi_specifications.datasets) == 0

        assert my_widget._regions_combobox.count() == 0
        assert my_widget._regions_combobox.currentIndex() == -1
        assert my_widget._regions_text_edit.toPlainText() == ""

        assert my_widget._reference_combobox.count() == 4
        assert my_widget._reference_combobox.currentIndex() == 0

        assert my_widget._locdatas_combobox.currentIndex() == -1
        assert my_widget._loc_properties_x_combobox.currentIndex() == -1
        assert my_widget._loc_properties_y_combobox.currentIndex() == -1

        assert not my_widget._rois_combobox.isEditable()
        assert my_widget._rois_combobox.currentIndex() == -1
        assert my_widget._rois_combobox.currentText() == ""
        assert my_widget._roi_text_edit.toPlainText() == ""

        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        assert len(my_widget.region_specifications.datasets) == 0
        assert len(my_widget.roi_specifications.datasets) == 0

        assert my_widget._regions_combobox.count() == 0
        assert my_widget._regions_combobox.currentIndex() == -1
        assert my_widget._regions_text_edit.toPlainText() == ""

        assert my_widget._reference_combobox.count() == 4
        assert my_widget._reference_combobox.currentIndex() == 0

        assert my_widget._locdatas_combobox.currentIndex() == 0
        assert my_widget._loc_properties_x_combobox.currentIndex() == 0
        assert my_widget._loc_properties_y_combobox.currentIndex() == 1

        assert not my_widget._rois_combobox.isEditable()
        assert my_widget._rois_combobox.currentIndex() == -1
        assert my_widget._rois_combobox.currentText() == ""
        assert my_widget._roi_text_edit.toPlainText() == ""

    def test_RoiQWidget_regions_from_shapes(self, make_napari_viewer, locdata_2d):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        shape_data = [
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "rectangle"),
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "ellipse"),
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "polygon"),
        ]
        viewer.add_shapes(shape_data)

        my_widget._scale_layer_button_on_click()

        my_widget._get_regions_from_shapes_button_on_click()
        assert len(my_widget.region_specifications.datasets) == 3
        assert my_widget._regions_combobox.count() == 3
        assert my_widget._regions_combobox.currentIndex() == 2
        assert my_widget._regions_combobox.currentText() == "3-Polygon"
        assert (
            my_widget._regions_text_edit.toPlainText()
            != "Rectangle((0.0, 0.0), 3.1, 2.5, 0)"
        )

        my_widget._delete_regions_button_on_click()
        assert len(my_widget.region_specifications.datasets) == 2
        assert my_widget._regions_combobox.count() == 2
        assert my_widget._regions_combobox.currentIndex() == 1
        assert my_widget._regions_text_edit.toPlainText() != ""

    @pytest.mark.skip("requires user interaction")
    def test_RoiQWidget_regions_from_locdata(self, make_napari_viewer, locdata_2d):
        locdata = copy(locdata_2d)
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        my_widget._get_regions_from_smlm_data_button_on_click()

        print(my_widget.region_specifications.datasets)
        assert len(my_widget.region_specifications.datasets) == 1
        assert my_widget._regions_combobox.count() == 1
        assert my_widget._regions_combobox.currentIndex() == 0
        assert my_widget._regions_combobox.currentText() == "1-Rectangle"

    @pytest.mark.skip("requires user interaction")
    def test_RoiQWidget_regions_delete_all(self, make_napari_viewer, locdata_2d):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        shape_data = [
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "rectangle"),
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "ellipse"),
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "polygon"),
        ]
        viewer.add_shapes(shape_data)

        my_widget._get_regions_from_shapes_button_on_click()
        assert len(my_widget.region_specifications.datasets) == 3
        assert my_widget._regions_combobox.count() == 3
        assert my_widget._regions_combobox.currentIndex() == 2

        # requires user interaction
        my_widget._delete_all_regions_button_on_click()
        assert len(my_widget.region_specifications.datasets) == 0
        assert my_widget._regions_combobox.count() == 0
        assert my_widget._regions_combobox.currentIndex() == -1

    def test_RoiQWidget_rois(self, make_napari_viewer, locdata_2d):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        smlm_data.locdata.meta.file.path = "locdata_2d.txt"
        smlm_data.locdata.meta.file.type = lc.FileType.RAPIDSTORM.value

        shape_data = [
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "rectangle"),
        ]
        viewer.add_shapes(shape_data)

        my_widget._get_regions_from_shapes_button_on_click()
        assert len(my_widget.region_specifications.datasets) == 1

        my_widget._reference_combobox.setCurrentIndex(0)
        assert my_widget._reference_combobox.currentText() == "None"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 1
        assert my_widget._rois_combobox.count() == 1
        assert my_widget._rois_combobox.currentIndex() == 0
        assert my_widget.roi_specifications.datasets[0].reference is None
        assert (
            my_widget.roi_specifications.datasets[0].region
            == my_widget.region_specifications.datasets[0]
        )
        assert my_widget.roi_specifications.datasets[0].loc_properties == [
            "position_x",
            "position_y",
        ]
        assert my_widget._roi_text_edit.toPlainText() != ""

        my_widget._reference_combobox.setCurrentIndex(1)
        assert my_widget._reference_combobox.currentText() == "SmlmData"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 2
        assert my_widget._rois_combobox.count() == 2
        assert my_widget._rois_combobox.currentIndex() == 1
        assert (
            my_widget.roi_specifications.datasets[1].reference
            is my_widget.smlm_data.locdata
        )
        assert (
            my_widget.roi_specifications.datasets[1].region
            == my_widget.region_specifications.datasets[0]
        )
        assert my_widget.roi_specifications.datasets[1].loc_properties == [
            "position_x",
            "position_y",
        ]
        assert my_widget._roi_text_edit.toPlainText() != ""

        my_widget._reference_combobox.setCurrentIndex(2)
        assert my_widget._reference_combobox.currentText() == "File reference"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 3
        assert my_widget._rois_combobox.count() == 3
        assert my_widget._rois_combobox.currentIndex() == 2
        assert isinstance(
            my_widget.roi_specifications.datasets[2].reference,
            lc.data.metadata_pb2.Metadata,
        )
        assert (
            my_widget.roi_specifications.datasets[2].reference.file.path
            == smlm_data.locdata.meta.file.path
        )
        assert (
            my_widget.roi_specifications.datasets[2].reference.file.type
            == smlm_data.locdata.meta.file.type
        )
        assert (
            my_widget.roi_specifications.datasets[2].region
            == my_widget.region_specifications.datasets[0]
        )
        assert my_widget.roi_specifications.datasets[2].loc_properties == [
            "position_x",
            "position_y",
        ]
        assert my_widget._roi_text_edit.toPlainText() != ""

        my_widget._reference_combobox.setCurrentIndex(0)
        assert my_widget._reference_combobox.currentText() == "None"
        my_widget._create_roi_button_on_click()
        with pytest.raises(AttributeError):
            my_widget._apply_roi_button_on_click()
        assert len(my_widget.smlm_data.locdatas) == 1

        my_widget._delete_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 3
        assert my_widget._rois_combobox.currentIndex() == 2

        my_widget._reference_combobox.setCurrentIndex(1)
        assert my_widget._reference_combobox.currentText() == "SmlmData"
        my_widget._create_roi_button_on_click()
        my_widget._apply_roi_button_on_click()
        assert len(my_widget.smlm_data.locdatas) == 2

    @pytest.mark.skip("requires user interactions")
    def test_RoiQWidget_reference_file_dialog_and_delete_all(
        self, make_napari_viewer, locdata_2d
    ):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        shape_data = [
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "rectangle"),
        ]
        viewer.add_shapes(shape_data)

        my_widget._get_regions_from_shapes_button_on_click()
        assert len(my_widget.region_specifications.datasets) == 1

        my_widget._reference_combobox.setCurrentIndex(3)
        assert my_widget._reference_combobox.currentText() == "File dialog"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 1
        assert my_widget._rois_combobox.count() == 1
        assert my_widget._rois_combobox.currentIndex() == 0
        print(my_widget.roi_specifications.datasets[0].reference)
        assert my_widget.roi_specifications.datasets[0].reference.file.path != ""
        assert my_widget.roi_specifications.datasets[0].reference.file.type != ""

        # requires user interaction
        my_widget._delete_all_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 0
        assert my_widget._rois_combobox.count() == 0
        assert my_widget._rois_combobox.currentIndex() == -1

    @pytest.mark.skip("need user interaction")
    def test_RoiQWidget_save_rois(self, make_napari_viewer, locdata_2d, tmp_path):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData(locdatas=[locdata_2d])
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        smlm_data.locdata.meta.file.path = str(tmp_path / "locdata_2d.txt")
        smlm_data.locdata.meta.file.type = "RAPIDSTORM"

        shape_data = [
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "rectangle"),
        ]
        viewer.add_shapes(shape_data)

        my_widget._get_regions_from_shapes_button_on_click()
        my_widget._reference_combobox.setCurrentIndex(1)
        assert my_widget._reference_combobox.currentText() == "SmlmData"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 1
        assert my_widget._rois_combobox.currentIndex() == 0
        with pytest.raises(AttributeError):
            my_widget._save_roi_button_on_click()

        my_widget._reference_combobox.setCurrentIndex(2)
        assert my_widget._reference_combobox.currentText() == "File reference"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 2
        assert my_widget._rois_combobox.currentIndex() == 1

        my_widget._save_roi_button_on_click()
        roi_file = (
            tmp_path / f"locdata_2d_{my_widget._rois_combobox.currentText()}.yaml"
        )
        assert roi_file.exists()

        my_widget._load_roi_button_on_click(file_path=roi_file)
        assert len(my_widget.roi_specifications.datasets) == 3
        assert my_widget._rois_combobox.currentIndex() == 2

    @pytest.mark.skip("need user interaction")
    def test_RoiQWidget_save_and_load_rois_gui(
        self, make_napari_viewer, locdata_2d, tmp_path
    ):
        region_specifications = RegionSpecifications()
        roi_specifications = RoiSpecifications()
        smlm_data = SmlmData()
        viewer = make_napari_viewer()
        my_widget = RoiQWidget(
            viewer,
            region_specifications=region_specifications,
            roi_specifications=roi_specifications,
            smlm_data=smlm_data,
        )

        shape_data = [
            (np.array([[0, 0], [0, 2.5], [3.1, 2.5], [3.1, 0]]), "rectangle"),
        ]
        viewer.add_shapes(shape_data)

        my_widget._get_regions_from_shapes_button_on_click()
        my_widget._reference_combobox.setCurrentIndex(3)
        assert my_widget._reference_combobox.currentText() == "File dialog"
        my_widget._create_roi_button_on_click()
        assert len(my_widget.roi_specifications.datasets) == 1
        assert my_widget._rois_combobox.currentIndex() == 0

        my_widget._save_roi_button_on_click()

        roi_file = Path(my_widget.roi_specifications.datasets[0].reference.file.path)
        roi_file = roi_file.with_name(roi_file.stem + "_roi_0.yaml")
        my_widget._load_roi_button_on_click(file_path=roi_file)
        assert len(my_widget.roi_specifications.datasets) == 2
        assert my_widget._rois_combobox.currentIndex() == 1


@pytest.mark.napari
def test_run_napari():
    viewer = napari.Viewer()
    viewer.open_sample("napari-locan", "tubulin_image")
    viewer.add_shapes(data=None, text="ROI shapes")
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="SMLM data"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Show metadata"
    )
    viewer.window.add_plugin_dock_widget(
        plugin_name="napari-locan", widget_name="Region of interest"
    )
    napari.run()
