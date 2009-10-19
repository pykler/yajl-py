=======
yajl-py
=======

`yajl-py` is a Pure Python wrapper (implemented using
ctypes) to the excellent Yajl (Yet Another JSON Library) C
library.

Dependencies
------------

    - python 2.5 (or compatible)
    - yajl: http://lloydforge.org/projects/yajl/

Install
-------

From within the current directory run::

    python setup.py install

        - OR Alternatively -

    easy_install .

Usage
-----

The examples directory contains a full featured JSON Parser
built using `yajl` and `yajl-py`. The code also prints some
output to stdout after parsing json from stdin. The printing
is more or less debug messages to show how the parser works.
See `examples/README.rst` for more info.
