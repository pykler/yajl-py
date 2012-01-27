import os
import sys
BASEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASEPATH, '%s/..' %BASEPATH] + sys.path

import yajl
import unittest
from minimocktest import MockTestCase
from StringIO import StringIO
