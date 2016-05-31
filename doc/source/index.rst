Yajl-Py documentation
=====================

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

`yajl-py <http://github.com/pykler/yajl-py>`_ is a pure python wrapper
to the `yajl <http://lloyd.github.com/yajl/>`_ C Library.

`yajl` and `yajl-py`, allow for fast stream parsing of JSON
files. This enables the parsing of large files, that would
otherwise be un-parsable as they would not fit in memory.

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

    pip install yajl-py

For the development version you may visit
`yajl-py at github <http://github.com/pykler/yajl-py>`_::

    pip install git+https://github.com/pykler/yajl-py.git

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

Parsing
+++++++
.. code-block:: python

    import sys
    from yajl import *

    # Sample callbacks, which output some debug info
    # these are examples to show off the yajl parser
    class ContentHandler(YajlContentHandler):
        def __init__(self):
            self.out = sys.stdout
        def yajl_null(self, ctx):
            self.out.write("null\n" )
        def yajl_boolean(self, ctx, boolVal):
            self.out.write("bool: %s\n" %('true' if boolVal else 'false'))
        def yajl_integer(self, ctx, integerVal):
            self.out.write("integer: %s\n" %integerVal)
        def yajl_double(self, ctx, doubleVal):
            self.out.write("double: %s\n" %doubleVal)
        def yajl_number(self, ctx, stringNum):
            ''' Since this is defined both integer and double callbacks are useless '''
            num = float(stringNum) if '.' in stringNum else int(stringNum)
            self.out.write("number: %s\n" %num)
        def yajl_string(self, ctx, stringVal):
            self.out.write("string: '%s'\n" %stringVal)
        def yajl_start_map(self, ctx):
            self.out.write("map open '{'\n")
        def yajl_map_key(self, ctx, stringVal):
            self.out.write("key: '%s'\n" %stringVal)
        def yajl_end_map(self, ctx):
            self.out.write("map close '}'\n")
        def yajl_start_array(self, ctx):
            self.out.write("array open '['\n")
        def yajl_end_array(self, ctx):
            self.out.write("array close ']'\n")

    # Create the parser
    parser = YajlParser(ContentHandler())
    # Parse JSON from stdin
    parser.parse()

Generating
++++++++++
.. code-block:: python

    from yajl import *

    g = YajlGen(beautify=False)
    g.yajl_gen_map_open()
    g.yajl_gen_string("a")
    g.yajl_gen_array_open()
    g.yajl_gen_null()
    g.yajl_gen_bool(True)
    g.yajl_gen_integer(1)
    g.yajl_gen_double(2.0)
    g.yajl_gen_number(str(3))

    g.yajl_gen_get_buf()
    # [Out]: '{"a":[null,true,1,2,3'

    g.yajl_gen_string("b")
    g.yajl_gen_array_close()
    g.yajl_gen_map_close()

    g.yajl_gen_get_buf()
    # [Out]: ',"b"]}'

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
