"""
Load SMLM data
"""
from pathlib import Path
import napari
import locan as lc


bin_size = 30

viewer = napari.current_viewer()

file_path = Path(lc.__file__).resolve().parent / \
                "tests/test_data" / \
                "rapidSTORM_dstorm_data.txt"
file_type = lc.FileType.RAPIDSTORM

locdata = lc.load_locdata(path=file_path, file_type=file_type)

print(locdata.meta)

# optional kwargs for the corresponding viewer.add_* method
add_kwargs = {
    "name": Path(file_path).stem,
    "scale": (bin_size, bin_size)
}

# render data
lc.render_2d_napari(
    locdata=locdata,
    viewer=viewer,
    n_bins=None,
    bin_size=bin_size,
    bin_range=None,
    bin_edges=None,
    rescale=lc.Trafo.EQUALIZE,
    cmap=lc.COLORMAP_CONTINUOUS,
    **add_kwargs,
)
