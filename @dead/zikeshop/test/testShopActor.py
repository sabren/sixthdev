"""
test code for the ShopActor class

$Id$
"""
import zikeshop
import unittest

class ShopActorTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        pass

