#
# testPerm.py - unit tests for Perm.py
#

import unittest
import weblib

class PermTestCase(unittest.TestCase):

    def check_engine(self):
        perm = weblib.Perm()
        assert perm.engine==weblib, "perm.engine doesn't default to weblib"
        assert weblib.perm is perm, "perm doesn't register itself in weblib"
        

    def checkInt(self):
        pass
