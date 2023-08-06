# mypythontools

[![Python versions](https://img.shields.io/pypi/pyversions/mypythontools.svg)](https://pypi.python.org/pypi/mypythontools/) [![PyPI version](https://badge.fury.io/py/mypythontools.svg)](https://badge.fury.io/py/mypythontools) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Malachov/mypythontools.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Malachov/mypythontools/context:python) [![Documentation Status](https://readthedocs.org/projects/mypythontools/badge/?version=latest)](https://mypythontools.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/Malachov/mypythontools/branch/master/graph/badge.svg)](https://codecov.io/gh/Malachov/mypythontools)

Some tools/functions/snippets used across projects.

Official documentation - [readthedocs](https://mypythontools.readthedocs.io/)
Official repo - [github](https://github.com/Malachov/mypythontools)

Usually used from IDE. Used paths are infered and things like sphinx rst docs generation, building
application with pyinstaller or deploying to Pypi is matter of calling one function,
or clicking one button (e.g. Vs code task).

Many projects - one codebase.

If you are not sure whether structure of app that will work with this code, there is python starter repo
on [github](https://github.com/Malachov/my-python-starter)

Paths are infered, but if you have atypical structure or have more projects in cwd, use `mypythontools.misc.set_paths()`.

Modules:

- build
- deploy
- misc
- pyvueeel (for applications build with eel and vue)
- utils (various functions callable from one `push_pipeline` function)

Check modules help with examples.

## Installation

Python >=3.6 (Python 2 is not supported).

Install just with

```console
pip install mypythontools
```
