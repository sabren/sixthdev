"""
test cases for python payment module
"""
__ver__="$Id$"

from testAccount import *
import unittest

suites = {
    "account" : unittest.makeSuite(AccountTestCase, "check_"),
    }

