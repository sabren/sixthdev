"""
testUser.py - test suite for zikebase.User

$Id$
"""

import unittest
import zikebase.test


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("DELETE FROM base_user")


    def tearDown(self):
	pass
