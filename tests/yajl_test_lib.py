'''
Helper module to import yajl from parent src dir
'''
import os
import sys
BASEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASEPATH, '%s/..' %BASEPATH] + sys.path

import yajl
