"""
test cases for python shipment module
"""
__ver__="$Id$"


from testUPSShipment import *
import unittest

suites = {
    "UpsShipment" : unittest.makeSuite(UpsShipmentTestCase, "check_"),
    }
