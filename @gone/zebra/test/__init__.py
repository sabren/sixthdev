"""
Test cases for Zebra.

$Id$
"""

import unittest

from testZbr2xml import *
from testXml2mdl import *
from testBootstrap import *

suites = {
    "zbr2xml" : unittest.makeSuite(Zbr2xmlTestCase, "check_"),
    "xml2mdl" : unittest.makeSuite(Xml2mdlTestCase, "check_"),
    "bootstrap" : unittest.makeSuite(BootstrapTestCase, "check_"),
    }

