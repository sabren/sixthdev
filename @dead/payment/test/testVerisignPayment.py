"""
test cases for VerisignPayment
"""
__ver__=\
  "$Id$"

import unittest
import payment
import test

class VerisignPaymentTestCase(unittest.TestCase):

    def check_charge(self):
        acct = payment.create("Verisign",
                              merchant = test.merchant["Verisign"],
                              card = "5105105105105100",
                              expires = "05/2005")

        acct.charge(1)
        assert acct.result == payment.APPROVED, \
               "charge didn't work!"

        acct.charge(101)
        assert acct.result == payment.DENIED, \
               "charge should have failed but didn't!"

