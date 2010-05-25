=======
yajl-py
=======

`yajl-py` is a Pure Python wrapper (implemented using
ctypes) to the excellent Yajl (Yet Another JSON Library) C
library.

Dependencies
------------

    - python 2.6 (or compatible)
    - yajl (from http://lloydforge.org/projects/yajl/)

To run the tests you also require:

    - make (to run `make test`)
    - nose (debian package == `python-nose`)

Install
-------

From within the current directory run::

    python setup.py install

        - OR Alternatively -

    easy_install .

Usage
-----

The examples directory contains a full featured JSON Parsers built
using `yajl` and `yajl-py`. See `examples/README.rst` for more info.
