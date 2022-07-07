"""
Read-to-go scripts for using locan within napari
"""
from enum import Enum, unique


@unique
class LocanScripts(Enum):
    HELLO = "script_hello"
    LOAD = "script_load"


script_hello = """
print("Hello world!")
"""

script_load = '''"""
Load SMLM data
"""
from pathlib import Path
import napari
import locan as lc


viewer = viewer = napari.current_viewer()

file_path = Path(lc.__file__).resolve().parent / \
                "tests/test_data" / \
                "rapidSTORM_dstorm_data.txt"
file_type = lc.FileType.RAPIDSTORM

locdata = lc.load_locdata(path=file_path, file_type=file_type)

print(locdata.meta)

# optional kwargs for the corresponding viewer.add_* method
add_kwargs = {"name": Path(file_path).stem}

# render data
lc.render_2d_napari(
    locdata=locdata,
    viewer=viewer,
    n_bins=None, 
    bin_size=10, 
    bin_range=None, 
    bin_edges=None,
    rescale=lc.Trafo.EQUALIZE,
    cmap=lc.COLORMAP_CONTINUOUS,
    **add_kwargs,
        )
'''