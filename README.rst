=======
yajl-py
=======


.. image:: https://travis-ci.org/pykler/yajl-py.png?branch=master
   :target: https://travis-ci.org/pykler/yajl-py

.. image:: https://coveralls.io/repos/pykler/yajl-py/badge.png
   :target: https://coveralls.io/r/pykler/yajl-py

.. image:: https://pypip.in/v/yajl-py/badge.png
   :target: https://crate.io/packages/yajl-py/#info

.. image:: https://pypip.in/d/yajl-py/badge.png
   :target: https://crate.io/packages/yajl-py/#info

.. image:: https://requires.io/github/pykler/yajl-py/requirements.png?branch=master
   :target: https://requires.io/github/pykler/yajl-py/requirements/?branch=master

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
