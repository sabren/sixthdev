"""
testSess.py - unit tests for weblib.Sess

$Id$
"""

import unittest
import weblib
import sqlTest

#@TODO: there ought to be test cases for each type of SessPool

from weblib import SessPool


class SessTestCase(unittest.TestCase):

    def setUp(self, sid=None):
        self.sess = weblib.Sess(SessPool.SqlSessPool(sqlTest.dbc))
        self.sess.start(sid)

    def check_engine(self):
        assert self.sess.engine==weblib, "sess.engine doesn't default to weblib. :/"


    def check_sid(self):
        sid = self.sess.sid
        assert len(sid)==32, "sess.sid isn't right."


    def check_persistence(self):       
        self.sess["x"] = 10
        self.sess.stop()
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
        assert gotError, \
               "Sess didn't raise keyError on nonexistant key"


        cat = self.sess.get("cat", "Indiana")
        assert cat == "Indiana", \
               "Sess doesn't do .get()"
        

        self.sess["cat"] = "Indy"
        assert self.sess.keys() == ['cat'], \
               "sess.keys() doesn't work"


        self.sess.clear()
        assert self.sess.get("cat") is None, \
               "sess.clear() doesn't work"


    def check_del(self):
        self.setUp("deltest")
        self.sess["cat"] = "indy"

        del self.sess["cat"]

        assert self.sess.get("cat") is None, "Didn't delete key from warmData"

        self.sess["cat"] = "indy"
        self.sess.stop()
        del self.sess
        self.setUp("deltest")
        del self.sess["cat"]

        assert self.sess.get("cat") is None, "Didn't delete key from coldData"
        
        


    def tearDown(self):
        del self.sess
