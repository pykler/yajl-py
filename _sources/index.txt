Welcome to Yajl-Py's documentation!
===================================

`yajl-py <http://github.com/pykler/yajl-py>`_ is a pure python wrapper
to the `yajl <http://lloyd.github.com/yajl/>`_ C Library.

Description
-----------

A library that allows sax-like parsing of JSON. It is a thin wrapper
around the yajl C library that aims to enable all yajl's features. It
uses ctypes to interface with yajl's routines, and thus allows for using
any yajl routine even if it isn't explicitly wrapped in yajl-py. yajl-py
aims to be as pythonic as possible and still be consistent with the
general style of yajl itself. This can be seen by comparing
:ref:`yajl-py examples <yajl-py-examples>` with the
`examples of yajl <http://lloyd.github.com/yajl/>`_ itself.

Installation
------------

To install the latest version of yajl-py, run::

    easy_install yajl-py

For the development version you may visit
`yajl-py at github <http://github.com/pykler/yajl-py>`_.

Alternatives
------------

Another python library that wraps yajl for python is 
`py-yajl <http://github.com/rtyler/py-yajl/>`_. py-yajl creates an
alternative to the built in json.loads and json.dumps using yajl. On the
other hand, yajl-py wraps only yajl's functionality giving the user the
flexibility of defining their callbacks and thus benifiting from yajl's
stream parsing.

.. _yajl-py-examples:

Versioning
----------

To maintain compatibility, yajl-py version numbering follows yajl's version
numbers, where releases of yajl-py are fully compatible with the same numbered
releases of yajl. This document reflects yajl-py version |release|.

Examples
--------

`Examples of how to use yajl-py
<http://github.com/pykler/yajl-py/tree/master/examples/>`_ quickly show
how much slimmer the python versions are than their C counterparts. Each
of the examples in that directory perform the same actions as the C
versions. The code is layed out in a similar fashion to the C code such
that one can follow the logic.

Quick Example
.............

.. write some quick example here

Documentaion
------------

yajl-py internally is divided in a similar way as yajl's C api. However,
for flexibility all the classes, methods and structures implemented in
each of the submodules is directly available under the main yajl module.
Therefore using ``yajl.yajl_parse.YajlParser`` is the same as using
``yajl.YajlParser`` and similarly ``yajl.yajl_gen.YajlGen`` is the same as
using ``yajl.YajlGen``. The shared object (dll in windows, and dylib for
bsd/MacOSX) is accessible as ``yajl.yajl_common.yajl`` or simply
``yajl.yajl``. Generally, you will not need to interact with the shared
object directly, if this is the case then it is a short-comming of
yajl-py.

The following links lead to documentation generated from the yajl-py
docstrings:

.. toctree::

    yajl/index
 
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

