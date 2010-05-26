from setuptools import setup, find_packages
import sys, os

from yajl import __version__ as version

setup(name='yajl-py',
      version=version,
      description="Pure Python Yajl Wrapper",
      long_description="""\
Pure Python wrapper to the excellent Yajl (Yet Another Json Library) C library""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='yajl json parsing',
      author='Hatem Nassrat',
      author_email='hnassrat@gmail.com',
      url='http://pykler.github.com/yajl-py/',
      license='PSF',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
