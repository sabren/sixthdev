"""
test cases for lecter
"""
__ver__="$Id$"

import unittest

from testInterpreter import *
from testWildcard import *

suites = {
    "Interpreter" : unittest.makeSuite(InterpreterTestCase, "check_"),
    "Wildcard" : unittest.makeSuite(WildcardTestCase, "check_"),
    }

