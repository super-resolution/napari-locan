from napari_locan import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
    smlm_data,
)


def test_make_image_npc():
    n_locdatas = len(smlm_data.locdatas)
    images = make_image_npc()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2
    assert len(smlm_data.locdatas) == n_locdatas + 1


def test_make_image_tubulin():
    n_locdatas = len(smlm_data.locdatas)
    images = make_image_tubulin()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2
    assert len(smlm_data.locdatas) == n_locdatas + 1


def test_make_points_npc():
    n_locdatas = len(smlm_data.locdatas)
    images = make_points_npc()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2
    assert len(smlm_data.locdatas) == n_locdatas + 1


def test_make_points_tubulin():
    n_locdatas = len(smlm_data.locdatas)
    images = make_points_tubulin()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2
    assert len(smlm_data.locdatas) == n_locdatas + 1
