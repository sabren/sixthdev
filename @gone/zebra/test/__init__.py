#
# testzebra.py
#
import unittest

from testXml2mdl import *
from testBootstrap import *

suites = {
    "bootstrap" : unittest.makeSuite(BootstrapTestCase, "check_"),
    "xml2mdl" : unittest.makeSuite(Xml2mdlTestCase, "check_")
#    "zebra": unittest.makeSuite(ZebraTestCase, "check_"),
#    "parser": unittest.makeSuite(ParserTestCase, "check_"),
    }


if __name__=="__main__":
    for suite in suites:
        unittest.TextTestRunner().run(suite)
