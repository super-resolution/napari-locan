# -*- coding: utf-8 -*-

# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import asyncio
import os
import sys
from importlib.metadata import version

# change event loop in windows for python 3.8
if (
    sys.version_info.major == 3
    and sys.version_info.minor == 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

# General information about the project.
project = "napari-locan"
author = "napari-locan Developers"
copyright = "2022-2023, napari-locan Developers"

# Version number generated by setuptools_scm
release = version("napari-locan")
# take major/minor
# version = '.'.join(release.split('.')[:2])
version = release  # type: ignore


# -- General configuration ---------------------------------------------------

# Minimal Sphinx version needed for documentation
# needs_sphinx = '1.0'

# Sphinx extension modules
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "myst_nb",
    "sphinx_copybutton",
]

# autosummary settings
# Make _autosummary files and include them
autosummary_generate = True

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# myST-NB settings
nb_execution_mode = "off"  # "force" "cache"

# copybutton settings
copybutton_prompt_text = ">>> "

# The language for content autogenerated by Sphinx.
language = "en"

# The suffixes of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}

# The master/root toctree document.
master_doc = root_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "jupyter_execute",
    ".jupyter_cache",
    "**.ipynb_checkpoints",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.
# html_theme = "sphinx_rtd_theme"
html_theme = "furo"

# Theme options
# for furo
html_theme_options: dict[str, bool] = {
    # 'sidebar_hide_name': True,
}

html_title = f"{project}\n{release}"
# html_title = f'{release}'
html_short_title = f"{project}"

html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"

html_static_path = ["_static"]


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = f"{project}_docs"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    "papersize": "a4paper",
    # The font size ('10pt', '11pt' or '12pt').
    "pointsize": "11pt",
    # Additional stuff for the LaTeX preamble.
    "preamble": r"\setcounter{tocdepth}{2}",
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
    "classoptions": ",openany,oneside",
}

latex_logo = "_static/logo.png"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "napari-locan.tex", "Locan Documentation", author, "manual"),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "napari-locan", "napari-locan Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "napari-locan",
        "napari-locan Documentation",
        author,
        "napari-locan",
        "One line description of project.",
        "Miscellaneous",
    ),
]
