"""
test cases for python payment module
"""
__ver__="$Id$"


## we don't want people just poking around in someone's
## account, so you'll have to override this yourself:
merchant = {
    "AuthorizeNet" : None,
    "Verisign" : ("zikeinteract","accessbak"),
    }

## Here's a simple way to override it without
## messing up the source for CVS. Just create a
## module called testconfig that contains
## merchants just like the above.
## Of course, if you're not planning to submit
## a patch, you can just change it above.

try:
    import testconfig
    merchant.update(testconfig.merchant)
except:
    pass


from testAbstractPayment import *
from testAuthorizeNetPayment import *
from testVerisignPayment import *
import unittest

suites = {
    "payment" : unittest.makeSuite(AbstractPaymentTestCase, "check_"),
    }

for key in merchant.keys():
    if merchant[key]:
        suites[key] = \
            unittest.makeSuite(locals()[key + "PaymentTestCase"],
                               "check_")
    else:
        print "skipping %s since no test merchant defined." % key
