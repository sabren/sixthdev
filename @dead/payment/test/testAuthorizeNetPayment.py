"""
test cases for AuthorizeNetPayment
"""
__ver__=\
  "$Id$"

import unittest
import payment
import test

class AuthorizeNetPaymentTestCase(unittest.TestCase):

    def check_charge(self):
        acct = payment.create("AuthorizeNet",
                              test = 1,
                              merchant = test.merchant["AuthorizeNet"],
                              card = "4222222222222",
                              expires = "02/03")

        acct.charge(1)
        assert acct.result == payment.APPROVED, \
               "charge didn't work!"

