"""
This is for distutils and py2exe:

% python setup.py py2exe
"""

from distutils.core import setup
import py2exe

setup(name="cvssh",
      scripts=["cvssh.py"],
)
