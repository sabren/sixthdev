"""
Test cases for the Password class

$Id$
"""

import unittest
import zikebase

class PasswordTestCase(unittest.TestCase):


    def check_set(self):
        pw = zikebase.Password()
        pw.set("myPassWord")

        assert pw == "myPassWord", \
               "Password doesn't compare with strings correctly."

        assert pw == zikebase.Password(pw.crypted), \
               "Password doesn't compare with other Passwords correctly."
