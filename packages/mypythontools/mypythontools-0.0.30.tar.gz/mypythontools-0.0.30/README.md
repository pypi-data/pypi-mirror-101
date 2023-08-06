# mypythontools

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
