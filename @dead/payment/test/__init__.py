"""
test cases for python payment module
"""
__ver__="$Id$"


## we don't want people just poking around in someone's
## account, so you'll have to override this yourself:
testMerchant = {
    "AuthorizeNet" : None,
    }

## Here's a simple way to override it without
## messing up the source for CVS. Just create a
## module called testconfig that contains
## testMerchants just like the above.
## Of course, if you're not planning to submit
## a patch, you can just change it above.

try:
    import testconfig
    testMerchant.update(testconfig.testMerchant)
except:
    pass


from testPayment import *
from testAuthorizeNetPayment import *
import unittest

suites = {
    "payment" : unittest.makeSuite(PaymentTestCase, "check_"),
    }

for key in testMerchant.keys():
    if testMerchant[key]:
        suites[key] = \
            unittest.makeSuite(locals()[key + "PaymentTestCase"], "check_")
    else:
        print "skipping %s since no test merchant defined." % key
