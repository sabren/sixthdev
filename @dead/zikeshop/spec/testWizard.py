"""
test routines for the Wizard class
"""
__ver__="$Id$"

import unittest
import zikeshop

class WizardTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()

    
        
