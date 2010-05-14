# (c) 2006-2009 Ian Bicking, Mike Beachy, and contributors
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
r"""
minimock is a simple library for doing Mock objects with doctest.
When using doctest, mock objects can be very simple.

Here's an example of something we might test, a simple email sender::

    >>> import smtplib
    >>> def send_email(from_addr, to_addr, subject, body):
    ...     conn = smtplib.SMTP('localhost')
    ...     msg = 'To: %s\nFrom: %s\nSubject: %s\n\n%s' % (
    ...         to_addr, from_addr, subject, body)
    ...     conn.sendmail(from_addr, [to_addr], msg)
    ...     conn.quit()

Now we want to make a mock ``smtplib.SMTP`` object.  We'll have to
inject our mock into the ``smtplib`` module::

    >>> smtplib.SMTP = Mock('smtplib.SMTP')
    >>> smtplib.SMTP.mock_returns = Mock('smtp_connection')

Now we do the test::

    >>> send_email('ianb@colorstudy.com', 'joe@example.com',
    ...            'Hi there!', 'How is it going?')
    Called smtplib.SMTP('localhost')
    Called smtp_connection.sendmail(
        'ianb@colorstudy.com',
        ['joe@example.com'],
        'To: joe@example.com\nFrom: ianb@colorstudy.com\nSubject: Hi there!\n\nHow is it going?')
    Called smtp_connection.quit()

Voila!  We've tested implicitly that no unexpected methods were called
on the object.  We've also tested the arguments that the mock object
got.  We've provided fake return calls (for the ``smtplib.SMTP()``
constructor).  These are all the core parts of a mock library.  The
implementation is simple because most of the work is done by doctest.
"""

__all__ = ["mock", "restore", "Mock", "TraceTracker", "assert_same_trace"]

import __builtin__
import sys
import inspect
import doctest
import re
import textwrap
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

# A list of mocked objects. Each item is a tuple of (original object,
# namespace dict, object name, and a list of object attributes).
#
mocked = []

def lookup_by_name(name, nsdicts):
    """
    Look up an object by name from a sequence of namespace dictionaries.
    Returns a tuple of (nsdict, object, attributes); nsdict is the
    dictionary the name was found in, object is the base object the name is
    bound to, and the attributes list is the chain of attributes of the
    object that complete the name.

        >>> import os
        >>> nsdict, name, attributes = lookup_by_name("os.path.isdir", 
        ...     (locals(),))
        >>> name, attributes
        ('os', ['path', 'isdir'])
        >>> nsdict, name, attributes = lookup_by_name("os.monkey", (locals(),))
        Traceback (most recent call last):
          ...
        NameError: name 'os.monkey' is not defined
            
    """
    for nsdict in nsdicts:
        attrs = name.split(".")
        names = []

        while attrs:
            names.append(attrs.pop(0))
            obj_name = ".".join(names)

            if obj_name in nsdict:
                attr_copy = attrs[:]
                tmp = nsdict[obj_name]
                try:
                    while attr_copy:
                        tmp = getattr(tmp, attr_copy.pop(0))
                except AttributeError:
                    pass
                else:
                    return nsdict, obj_name, attrs

    raise NameError("name '%s' is not defined" % name)

def mock(name, nsdicts=None, mock_obj=None, **kw):
    """
    Mock the named object, placing a Mock instance in the correct namespace
    dictionary. If no iterable of namespace dicts is provided, use
    introspection to get the locals and globals of the caller of this
    function, as well as __builtin__.__dict__ to allow mocking built-ins.

    All additional keyword args are passed on to the Mock object
    initializer.

    An example of how os.path.isfile is replaced:

        >>> import os
        >>> os.path.isfile
        <function isfile at ...>
        >>> isfile_id = id(os.path.isfile)
        >>> mock("os.path.isfile", returns=True)
        >>> os.path.isfile
        <Mock ... os.path.isfile>
        >>> os.path.isfile("/foo/bar/baz")
        Called os.path.isfile('/foo/bar/baz')
        True
        >>> mock_id = id(os.path.isfile)
        >>> mock_id != isfile_id
        True

    A second mock object will replace the first, but the original object
    will be the one replaced with the replace() function.

        >>> mock("os.path.isfile", returns=False)
        >>> mock_id != id(os.path.isfile)
        True
        >>> restore()
        >>> os.path.isfile
        <function isfile at ...>
        >>> isfile_id == id(os.path.isfile)
        True

    Test mocking a built-in function:
        >>> mock("raw_input", returns="okay")
        >>> raw_input()
        Called raw_input()
        'okay'

    """
    if nsdicts is None:
        stack = inspect.stack()
        try:
            # stack[1][0] is the frame object of the caller to this function
            globals_ = stack[1][0].f_globals
            locals_ = stack[1][0].f_locals
            nsdicts = (locals_, globals_, __builtin__.__dict__)
        finally:
            del(stack)

    if mock_obj is None:
        mock_obj = Mock(name, **kw)

    nsdict, obj_name, attrs = lookup_by_name(name, nsdicts)

    # Get the original object and replace it with the mock object.
    tmp = nsdict[obj_name]

    # if run from a doctest, nsdict may point to a *copy* of the
    # global namespace, so instead use tmp.func_globals if present.
    # we use isinstance(gettattr(...), dict) rather than hasattr
    # because if tmp is itself a mock object, tmp.func_globals will
    # return another mock object
    if isinstance(getattr(tmp, 'func_globals', None), dict):
        nsdict = tmp.func_globals
    if not attrs:
        original = tmp
        nsdict[obj_name] = mock_obj
    else:
        for attr in attrs[:-1]:
            tmp = getattr(tmp, attr)
        original = getattr(tmp, attrs[-1])
        setattr(tmp, attrs[-1], mock_obj)

    mocked.append((original, nsdict, obj_name, attrs))

def restore():
    """
    Restore all mocked objects.
    """
    global mocked

    # Restore the objects in the reverse order of their mocking to assure
    # the original state is retrieved.
    while mocked:
        original, nsdict, name, attrs = mocked.pop()
        if not attrs:
            nsdict[name] = original
        else:
            tmp = nsdict[name]
            for attr in attrs[:-1]:
                tmp = getattr(tmp, attr)
            setattr(tmp, attrs[-1], original)
    return

def assert_same_trace(tracker, want):
    r"""
    Check that the mock objects using ``tracker`` have been used as expected.
    
    :param tracker: a :class:`TraceTracker` instance
    :param want: the expected :class:`Printer` output
    :type want: string
    :raises: :exc:`AssertionError` if the expected and observed outputs don't
        match
    
    Example::
    
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> assert_same_trace(tt,
            ...     "Called mock_obj.some_meth('dummy argument')\n")
            >>> assert_same_trace(tt, "Non-matching trace")
            Traceback (most recent call last):
            ...
            AssertionError...
    """
    assert tracker.check(want), tracker.diff(want)
    
class AbstractTracker(object):
    def __init__(self, *args, **kw):
        raise NotImplementedError

    def call(self, *args, **kw):
        raise NotImplementedError

    def set(self, *args, **kw):
        raise NotImplementedError

class Printer(AbstractTracker):
    """Prints all calls to the file it's instantiated with.
    Can take any object that implements `write'.
    """
    def __init__(self, file):
        self.file = file

    def call(self, func_name, *args, **kw):
        parts = [repr(a) for a in args]
        parts.extend(
            '%s=%r' % (items) for items in sorted(kw.items()))
        msg = 'Called %s(%s)' % (func_name, ', '.join(parts))
        if len(msg) > 80:
            msg = 'Called %s(\n    %s)' % (
                func_name, ',\n    '.join(parts))
        print >> self.file, msg

    def set(self, obj_name, attr, value): 
        """
        >>> z = Mock('z', show_attrs=True)
        >>> z.a = 2
        Set z.a = 2
        """
        print >> self.file, 'Set %s.%s = %r' % (obj_name, attr, value)
        
class TraceTracker(Printer):
    """
    :class:`AbstractTracker` implementation for using MiniMock in non-
    :mod:`doctest` tests. Follows the pattern of recording minimocked
    object usage as strings, then using the facilities of :mod:`doctest`
    to assert the correctness of these usage strings.
    """
    def __init__(self, *args, **kw):
        self.out = StringIO()
        super(TraceTracker, self).__init__(self.out, *args, **kw)
        self.checker = MinimockOutputChecker()
        self.options =  doctest.ELLIPSIS
        self.options |= doctest.NORMALIZE_INDENTATION
        self.options |= doctest.NORMALIZE_FUNCTION_PARAMETERS
        self.options |= doctest.REPORT_UDIFF
        
    def check(self, want):
        r"""
        Compare observed MiniMock usage with that which we expected.
        
        :param want: the :class:`Printer` output that results from expected
            usage of mocked objects
        :type want: string
        :rtype: a ``True`` value if the check passed, ``False`` otherwise
        
        Example::
        
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('arg1')
            >>> tt.check("Called mock_obj.some_meth('arg1')")
            True
            >>> tt.clear()
            >>> m.some_meth('arg2')
            >>> tt.check("does not match")
            False
        """
        return self.checker.check_output(want, self.dump(),
            optionflags=self.options)
        
    def diff(self, want):
        r"""
        Analyse differences between observed MiniMock usage and that which
        we expected, if any.
        
        :param want: the :class:`Printer` output that results from expected
            usage of mocked objects
        :type want: string
        :rtype: a string summary of differences between the observed usage and
            the ``want`` parameter
        
        Example::
        
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> tt.diff("does not match")
            "Expected:\n    does not match\nGot:\n    Called mock_obj.some_meth('dummy argument')\n"
            >>> tt.diff("Called mock_obj.some_meth('dummy argument')")
            ''
        """
        if self.check(want):
            # doctest's output_difference always returns a diff, even if
            # there's no difference: short circuit that feature.
            return ''
        else:
            return self.checker.output_difference(doctest.Example("", want),
                self.dump(), optionflags=self.options)
        
    def dump(self):
        r"""
        Return the MiniMock object usage so far.
        
        Example::
        
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> tt.dump()
            "Called mock_obj.some_meth('dummy argument')\n"
        """
        return self.out.getvalue()

    def clear(self):
        """Clear the MiniMock object usage that has been tracked so far.
        """
        self.out.truncate(0)


def normalize_function_parameters(text):
    r"""
    Return a version of ``text`` with function parameters normalized.

        The normalisations performed are:

        * Remove any whitespace sequence between an opening
          parenthesis '(' and a subsequent non-whitespace character.

        * Remove any whitespace sequence between a non-whitespace
          character and a closing parenthesis ')'.

        * Ensure a comma ',' and a subsequent non-whitespace character
          are separated by a single space ' '.

    Example::
        
        >>> tt = TraceTracker()
        >>> foo = Mock("foo", tracker=tt)
        >>> expect_mock_output = '''\
        ...     Called foo.bar('baz')
        ...     '''
        >>> foo.bar('baz')
        >>> tt.check(expect_mock_output)
        True
        >>> tt.clear()
        >>> expect_mock_output = '''\
        ...     Called foo.bar(
        ...         'baz')
        ...     '''
        >>> foo.bar('baz')
        >>> tt.check(expect_mock_output)
        True
    """
    normalized_text = text
    normalize_map = {
        re.compile(r"\(\s+(\S)"): r"(\1",
        re.compile(r"(\S)\s+\)"): r"\1)",
        re.compile(r",\s*(\S)"): r", \1",
        }
    for search_pattern, replace_pattern in normalize_map.items():
        normalized_text = re.sub(
            search_pattern, replace_pattern, normalized_text)

    return normalized_text


doctest.NORMALIZE_INDENTATION = (
    doctest.register_optionflag('NORMALIZE_INDENTATION'))
doctest.NORMALIZE_FUNCTION_PARAMETERS = (
    doctest.register_optionflag('NORMALIZE_FUNCTION_PARAMETERS'))


class MinimockOutputChecker(doctest.OutputChecker, object):
    """Class for matching output of MiniMock objects against expectations.
    """

    def check_output(self, want, got, optionflags):
        if (optionflags & doctest.NORMALIZE_INDENTATION):
            want = textwrap.dedent(want).rstrip()
            got = textwrap.dedent(got).rstrip()
        if (optionflags & doctest.NORMALIZE_FUNCTION_PARAMETERS):
            want = normalize_function_parameters(want)
            got = normalize_function_parameters(got)
        output_match = super(MinimockOutputChecker, self).check_output(
            want, got, optionflags)
        return output_match
    check_output.__doc__ = doctest.OutputChecker.check_output.__doc__


class _DefaultTracker(object):
    def __repr__(self):
        return '(default tracker)'
DefaultTracker = _DefaultTracker()
del _DefaultTracker

class Mock(object):

    def __init__(self, name, returns=None, returns_iter=None,
                 returns_func=None, raises=None, show_attrs=False,
                 tracker=DefaultTracker, **kw):
        _obsetattr = object.__setattr__
        _obsetattr(self, 'mock_name', name)
        _obsetattr(self, 'mock_returns', returns)
        if returns_iter is not None:
            returns_iter = iter(returns_iter)
        _obsetattr(self, 'mock_returns_iter', returns_iter)
        _obsetattr(self, 'mock_returns_func', returns_func)
        _obsetattr(self, 'mock_raises', raises)
        _obsetattr(self, 'mock_attrs', kw)
        _obsetattr(self, 'mock_show_attrs', show_attrs)
        if tracker is DefaultTracker:
            tracker = Printer(sys.stdout)
        _obsetattr(self, 'mock_tracker', tracker)

    def __repr__(self):
        return '<Mock %s %s>' % (hex(id(self)), self.mock_name)

    def __call__(self, *args, **kw):
        if self.mock_tracker is not None:
            self.mock_tracker.call(self.mock_name, *args, **kw)
        return self._mock_return(*args, **kw)

    def _mock_return(self, *args, **kw):
        if self.mock_raises is not None:
            raise self.mock_raises
        elif self.mock_returns is not None:
            return self.mock_returns
        elif self.mock_returns_iter is not None:
            try:
                return self.mock_returns_iter.next()
            except StopIteration:
                raise Exception("No more mock return values are present.")
        elif self.mock_returns_func is not None:
            return self.mock_returns_func(*args, **kw)
        else:
            return None

    def __getattr__(self, attr):
        if attr not in self.mock_attrs:
            if self.mock_name:
                new_name = self.mock_name + '.' + attr
            else:
                new_name = attr
            self.mock_attrs[attr] = Mock(new_name,
                show_attrs=self.mock_show_attrs,
                tracker=self.mock_tracker)
        return self.mock_attrs[attr]

    def __setattr__(self, attr, value):
        if attr in frozenset((
            'mock_raises',
            'mock_returns',
            'mock_returns_func',
            'mock_returns_iter',
            'mock_tracker',
            'show_attrs',
            )):
            if attr == 'mock_returns_iter' and value is not None:
                value = iter(value)
            object.__setattr__(self, attr, value)
        else:
            if self.mock_show_attrs and self.mock_tracker is not None:
                self.mock_tracker.set(self.mock_name, attr, value)
            self.mock_attrs[attr] = value 

__test__ = {
    "Mock" :
    r"""
    Test setting various "mock_" attributes on an existing Mock object.

    >>> m = Mock('mock_obj', tracker=None)
    >>> m.mock_returns = 42
    >>> m()
    42
    >>> m.mock_returns = None
    >>> m.mock_returns_func = lambda x: x*x
    >>> m(3)
    9
    >>> m.mock_returns_func = None
    >>> m.mock_returns_iter = [True, False]
    >>> m()
    True
    >>> m()
    False
    >>> m.mock_returns_iter = None
    >>> m.mock_raises = ValueError
    >>> try:
    ...     m()
    ... except ValueError:
    ...     pass
    ... else:
    ...     raise AssertionError('m() should have raised ValueError')
    """,

    "mock" :
    r"""
    An additional test for mocking a function accessed directly (i.e.
    not via object attributes).

    >>> import os
    >>> rename = os.rename
    >>> orig_id = id(rename)
    >>> mock("rename")
    >>> mock_id = id(rename)
    >>> mock("rename")
    >>> mock_id != id(rename)
    True
    >>> restore()
    >>> orig_id == id(rename) == id(os.rename)
    True

    The example from the module docstring, done with the mock/restore
    functions.

    >>> import smtplib
    >>> def send_email(from_addr, to_addr, subject, body):
    ...     conn = smtplib.SMTP('localhost')
    ...     msg = 'To: %s\nFrom: %s\nSubject: %s\n\n%s' % (
    ...         to_addr, from_addr, subject, body)
    ...     conn.sendmail(from_addr, [to_addr], msg)
    ...     conn.quit()

    >>> mock("smtplib.SMTP", returns=Mock('smtp_connection'))
    >>> send_email('ianb@colorstudy.com', 'joe@example.com',
    ...            'Hi there!', 'How is it going?')
    Called smtplib.SMTP('localhost')
    Called smtp_connection.sendmail(
        'ianb@colorstudy.com',
        ['joe@example.com'],
        'To: joe@example.com\nFrom: ianb@colorstudy.com\nSubject: Hi there!\n\nHow is it going?')
    Called smtp_connection.quit()
    >>> restore()

    """,
}

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
