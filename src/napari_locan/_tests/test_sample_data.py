from napari_locan import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
)


def test_make_image_npc():
    images = make_image_npc()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2


def test_make_image_tubulin():
    images = make_image_tubulin()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2


def test_make_points_npc():
    images = make_points_npc()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2


def test_make_points_tubulin():
    images = make_points_tubulin()
    assert isinstance(images[0], tuple)
    assert images[0][0].ndim == 2
