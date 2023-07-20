![logo](./docs/_static/logo.png) napari-locan
==================================================

[![License](https://img.shields.io/pypi/l/napari-locan.svg?color=green)](https://github.com/super-resolution/napari-locan/blob/main/LICENSE.md)
[![PyPI](https://img.shields.io/pypi/v/napari-locan.svg?color=green)](https://pypi.org/project/napari-locan)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-locan.svg?color=green)](https://python.org)
[![tests](https://github.com/super-resolution/napari-locan/workflows/tests/badge.svg)](https://github.com/super-resolution/napari-locan/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/super-resolution/napari-locan/branch/main/graph/badge.svg)](https://codecov.io/gh/super-resolution/napari-locan)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-locan)](https://napari-hub.org/plugins/napari-locan)

Use locan methods in napari.

This plugin allows loading, visualizing and analyzing
single-molecule localization (SMLM) data.
napari-locan is well suited for exploratory data analysis.

It implements a subset of methods from [locan], a python-based library with
code for analyzing SMLM data.
Locan provides extended functionality that is better suited for script- or
notebook-based analysis procedures.

For details on usage and development of napari-locan please read the [documentation].

----------------------------------

## Installation

You can install `napari-locan` via [pip]:

    pip install napari-locan



To install latest development version :

    pip install git+https://github.com/super-resolution/napari-locan.git@main


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-locan" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/super-resolution/napari-locan/issues
[documentation]: https://napari-locan.readthedocs.io

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
[locan]: https://locan.readthedocs.io/en/latest/
