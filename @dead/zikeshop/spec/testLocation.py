"""
test cases for zikeshop.Location
"""
__ver__ = "$Id$"

import unittest
import zikeshop

class LocationTestCase(unittest.TestCase):

    def check_inventory(self):
        prod1 = zikeshop.Product()
        prod2 = zikeshop.Product()

        loc = zikeshop.Location()
        loc.incInventory(prod1, 10)
        loc.incInventory(prod2, 5)
        loc.decInventory(prod1, 2)

        assert loc.calcInventory(prod1) == 8, \
               "location inventory doesn't work!"

