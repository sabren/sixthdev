"""
test cases for AuthorizeNetPayment
"""
__ver__=\
  "$Id$"

import unittest
import payment

class AuthorizeNetPaymentTestCase(unittest.TestCase):

    def check_charge(self):
        acct = payment.create("AuthorizeNet",
                              card = "4222222222222")
        result = acct.charge(1)
        assert result == payment.SUCCESS, \
               "charge didn't work!"
               
            

