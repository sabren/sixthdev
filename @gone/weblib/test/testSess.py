#
# tstSess.py - unit tests for Sess.py
#

import unittest
from weblib import Sess, DBSessPool
import test


class SessTestCase(unittest.TestCase):
    def setUp(self):
        self.sess = Sess(DBSessPool(test.dbc))

    def check_sid(self):
        self.sess.start()
        sid = self.sess.sid
        assert len(sid)==32, "sess.sid isn't right."

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
