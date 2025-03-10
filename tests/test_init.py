import napari_locan


def test_version():
    try:
        assert isinstance(napari_locan._version.version, str)
        assert isinstance(napari_locan._version.version_tuple, tuple)
    except AttributeError:
        pass
    assert napari_locan.__version__
    assert napari_locan.__all__
    assert all(
        item in napari_locan.__all__
        for item in dir(napari_locan)
        if not item.startswith("_") and "Widget" in item
    )
    # print(dir(napari_locan))
    # print(napari_locan.__version__)
    # print(napari_locan.__all__)
