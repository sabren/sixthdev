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
        assert weblib.sess is self.sess, "sess doesn't register itself with weblib"
        

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


    def tearDown(self):
        del self.sess

    """
    #@TODO: make this into an automated test..
    import sys
    sys.path.append("c:/zike/code/weblib/")
    import Sess
    sess = Sess.Sess(Sess.SessPool("test.dbm"))
    
    class Fungus:
        pass
    
    
        sess.start("2dfb8b368d3422cc176bc0cf8948d84d")


        if sess.has_key("x"):
        sess["x"] = sess["x"] + 1
    else:
    sess["x"] = 0
    
    a, b, c = "A", "B", "C"
    sess["z"] = Fungus()
    sess["y"] = (5, 4, "three", ("a","b","c"), (((a), b), c), [], {"x":"y"})
    
    print "now sess[x] = " + `sess["x"]`
    print "now sess[y] = " + `sess["y"]`
    print "now sess[z] = " + `sess["z"]`
    
    sess.freeze()
    
    """
