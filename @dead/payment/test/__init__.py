"""
test cases for python payment module
"""
__ver__="$Id$"

from testPayment import *
from testAuthorizeNetPayment import *
import unittest

suites = {
    "payment" : unittest.makeSuite(PaymentTestCase, "check_"),
    "authorize.net":unittest.makeSuite(AuthorizeNetPaymentTestCase, "check_"),
    }

