"""
unit tests for zdc.Connection
"""
__ver__="$Id$"
import unittest
import zdc

class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.dbc = zdc.Connection()

    def check_open(self):
        self.dbc.open("mysql")
