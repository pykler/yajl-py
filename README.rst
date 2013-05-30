=======
yajl-py
=======

`yajl-py` is a Pure Python wrapper (implemented using
ctypes) to the excellent Yajl (Yet Another JSON Library) C
library.

`yajl` and `yajl-py`, allow for fast stream parsing of JSON
files, which enables the parsing of large files, that would
not fit in memory.

Dependencies
------------

    - python 2.6 (or compatible)
    - yajl (from http://lloyd.github.com/yajl/)

To run the tests you also require:

    - make (to run `make test`)
    - nose (debian package == `python-nose`)
    - MiniMockTest (`pip install minimocktest`)

Install
-------

From within the current directory run::

    python setup.py install

        - OR Alternatively -

    pip install .

To install from pypi::

    pip install yajl-py

Usage
-----

The examples directory contains full featured JSON Parsers built using
`yajl` and `yajl-py`. See `examples/README.rst` for more info.
