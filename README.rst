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

    - python 2.7+, python 3.3+
    - `yajl <http://lloyd.github.io/yajl/>`_

To run the tests you also require:

    - make (to run ``make test``)
    - nose (debian package == ``python-nose``)
    - mock (``pip install mock``)

Install
-------

From within the current directory run::

    pip install .

To install from pypi::

    pip install yajl-py

Usage
-----

The examples directory contains full featured JSON Parsers built using
``yajl`` and ``yajl-py``. See `examples/README.rst <examples/>`_ for more info.

Notes around strings, python 3, and yajl-py
-------------------------------------------

TLDR; if using python3, yajl-py expects bytes and not strings

Python 3 fixed a whole string of issues with strings. Due to these fixes
somethings taken for granted in python 2 are now explicit in python 3. The
major change that affects yajl-py is related to a decision made within ctypes.

Strings going and coming from the ctypes interface to c-code are now bytes.
Although we can make an explicit decision to decode and encode strings
transparently to latin-1 or utf-8, this is an arbitrary choice. Even
though it can be coded in such a way to make the encoding configurable, the
decision has been made to keep with the decision made by ctypes and hence put
the onus on the developer to decode/encode the input/output as necessary.

Contributions
-------------

The following people provided valuable contributions to this library:

 * `Peter Dobcsanyi`
 * `Charles Gordon <https://github.com/cgordon>`_
 * `Christopher Reighley <https://github.com/reighley-christopher>`_
