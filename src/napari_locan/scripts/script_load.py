"""
Load SMLM data
"""

from pathlib import Path

import locan as lc
import napari

bin_size = 30

viewer = napari.current_viewer()

file_path = Path(__file__).resolve().parents[1] / "scripts/npc_gp210.asdf"
file_type = lc.FileType.ASDF

locdata = lc.load_locdata(path=file_path, file_type=file_type)

print(locdata.meta)

# optional kwargs for the corresponding viewer.add_* method
add_kwargs = {"name": Path(file_path).stem, "scale": (bin_size, bin_size)}

# render data
lc.render_2d_napari(
    locdata=locdata,
    viewer=viewer,
    n_bins=None,
    bin_size=bin_size,
    bin_range=None,
    bin_edges=None,
    rescale=lc.Trafo.EQUALIZE,
    cmap=lc.COLORMAP_DEFAULTS["CONTINUOUS"],
    **add_kwargs,
)
