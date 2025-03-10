"""
Ready-to-go scripts for using locan within napari
"""

from enum import Enum, unique


@unique
class LocanScripts(Enum):
    NONE = ""
    HELLO = "script_hello.py"
    LOAD = "script_load.py"
