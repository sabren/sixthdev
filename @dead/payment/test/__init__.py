"""
test cases for python payment module
"""
__ver__="$Id$"

from testPayment import *
import unittest

suites = {
    "payment" : unittest.makeSuite(PaymentTestCase, "check_"),
    }

