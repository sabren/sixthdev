"""
testSess.py - unit tests for weblib.Sess

$Id$
"""

import unittest
import weblib
import test

#@TODO: there ought to be test cases for each type of SessPool

from weblib import SessPool


class SessTestCase(unittest.TestCase):

    def setUp(self, sid=None):
        self.sess = weblib.Sess(SessPool.SqlSessPool(test.dbc))
        self.sess.start(sid)

    def check_engine(self):
        assert self.sess.engine==weblib, "sess.engine doesn't default to weblib. :/"


    def check_sid(self):
        sid = self.sess.sid
        assert len(sid)==32, "sess.sid isn't right."


    def check_persistence(self):       
        self.sess["x"] = 10
        self.sess.freeze()
        sid = self.sess.sid

        del self.sess
        self.setUp(sid)

        assert self.sess["x"]==10, "peristence doesn't work! :/"


    def check_dictstuff(self):
        
        gotError = 0
        try:
            cat = self.sess["cat"]
        except KeyError:
            gotError = 1

        assert gotError, "Didn't get keyError on nonexistant key"

        self.sess["cat"] = "Indy"

        assert self.sess.keys() == ['cat'], "sess.keys() doesn't work"


    def tearDown(self):
        del self.sess
