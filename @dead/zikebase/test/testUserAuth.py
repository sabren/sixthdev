"""
testUserAuth.py - test suite for zikebase.UserAuth

$Id$
"""

import unittest
import zikebase.test


class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()

    def tearDown(self):
	pass
