=======
yajl-py
=======


.. image:: https://img.shields.io/travis/pykler/yajl-py.svg
    :target: https://travis-ci.org/pykler/yajl-py

.. image:: https://img.shields.io/coveralls/pykler/yajl-py.svg
    :target: https://coveralls.io/r/pykler/yajl-py

.. image:: https://img.shields.io/pypi/v/yajl-py.svg
    :target: https://pypi.python.org/pypi/yajl-py

.. image:: https://img.shields.io/github/issues/pykler/yajl-py.svg?maxAge=86400
    :target: https://github.com/pykler/yajl-py/issues

.. image:: https://img.shields.io/github/forks/pykler/yajl-py.svg?style=social
    :target: https://github.com/pykler/yajl-py

.. image:: https://img.shields.io/github/stars/pykler/yajl-py.svg?style=social
    :target: https://github.com/pykler/yajl-py

.. image:: https://img.shields.io/github/watchers/pykler/yajl-py.svg?style=social
   :target: https://github.com/pykler/yajl-py/subscription

``yajl-py`` is a Pure Python wrapper (implemented using
ctypes) to the excellent Yajl (Yet Another JSON Library) C
library.

``yajl`` and ``yajl-py``, allow for fast stream parsing of JSON
files, which enables the parsing of large files, that would
not fit in memory.

Dependencies
------------

    - python 2.6 (or compatible)
    - `yajl <http://lloyd.github.com/yajl/>`_

To run the tests you also require:

    - make (to run ``make test``)
    - nose (debian package == ``python-nose``)
    - MiniMockTest (``pip install minimocktest``)

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
``yajl`` and ``yajl-py``. See `examples/README.rst <examples/>`_ for more info.

Contributions
-------------

The following people provided valuable contributions to this library:

 * `Peter Dobcsanyi`
 * `Charles Gordon <https://github.com/cgordon>`_
 * `Christopher Reighley <https://github.com/reighley-christopher>`_
