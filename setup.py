import re

from setuptools import setup, find_packages


def get_version() -> str:
    """
    Read the version value from the __init__ file without importing it.
    This fixes the missing dependencies issue when installing the package.
    """
    file_path = "yajl/__init__.py"
    version_pattern = re.compile(r"__version__\s*=\s*['\"]([^'\"]+)['\"]")
    with open(file_path, 'r') as file:
        for line in file:
            match = version_pattern.search(line)
            if match:
                return match.group(1)

    # If we get here, we didn't find a version - raise an exception.
    raise RuntimeError("Unable to find version string.")


setup(name='yajl-py',
      version=get_version(),
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
          'six',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
