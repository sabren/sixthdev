"""
test cases for main payment routines
"""
__ver__="$Id$"

import unittest
import payment

class PaymentTestCase(unittest.TestCase):

    def check_create(self):
        acct = payment.create("AuthorizeNet", card="4444444444444442")
        assert acct.__class__ == payment.AuthorizeNetPayment, \
               "create() didn't make the correct class."

        try:
            acct = payment.create("SOMETHING THAT DOESN'T EXIST")
        except NameError:
            gotError = 1
        else:
            gotError = 0

        assert gotError, \
               "Didn't get NameError when trying to create invalid class."

        
    
