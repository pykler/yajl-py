import os
import sys
BASEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASEPATH, '%s/..' %BASEPATH] + sys.path

import yajl
import unittest
import minimock
from StringIO import StringIO

class MockTestCase(unittest.TestCase):
    '''
    A TestCase class that integrates minimock functionailty
    `self.tt` minimock tracker object
    `self.mock` calls minimock.mock using tracker=`self.tt`
    `self.assertSameTrace` calls minimock.assert_same_trace with `self.tt`
    '''
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tt = minimock.TraceTracker()

    def tearDown(self):
        minimock.restore()
        unittest.TestCase.tearDown(self)

    def mock(self, *args, **kwargs):
        if 'tracker' not in kwargs:
            kwargs['tracker'] = self.tt
        return minimock.mock(*args, **kwargs)

    def assertSameTrace(self, want):
        minimock.assert_same_trace(self.tt, want)
