"""
testSess.py - unit tests for weblib.Sess
"""
__ver__="$Id$"

import unittest
import weblib

#@TODO: there ought to be test cases for each type of SessPool

from weblib import SessPool, RequestBuilder


class SessTest(unittest.TestCase):
    dict = {"":""} # @TODO: why doesn't it work with just {} ??
    
    def setUp(self, sid=None):
        self.builder = weblib.RequestBuilder()
        self.pool = SessPool.InMemorySessPool(SessTest.dict)
        self.sess = weblib.Sess(self.pool,
                                self.builder.build(),
                                weblib.Response())
        self.sess.start(sid)

    def test_sid(self):
        """
        A generated session id (sid) should be 32 chars.
        """
        sid = self.sess.sid
        assert len(sid)==32, "sess.sid isn't right."


    def test_persistence(self):
        """
        If you add something to one Sess object, it should persist in
        the next, provided the two Sess objects use the same SessPool.
        """
        self.sess["x"] = 10
        self.sess.stop()
        sid = self.sess.sid

        del self.sess
        self.setUp(sid)

        assert self.sess["x"]==10, "peristence doesn't work! :/"


    def test_dictstuff(self):
        
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


    def test_del(self):
        self.setUp("deltest")
        self.sess["cat"] = "indy"

        del self.sess["cat"]

        assert self.sess.get("cat") is None, \
               "Didn't delete key from warmData"

        self.sess["cat"] = "indy"
        self.sess.stop()
        del self.sess
        self.setUp("deltest")
        del self.sess["cat"]

        assert self.sess.get("cat") is None, \
               "Didn't delete key from coldData"


    def test_url(self):
        #@TODO: more advanced checks..
        self.sess.name = "sess"
        self.sess.sid = "ABC"
        assert self.sess.url("http://x.com") == "http://x.com?sess=ABC", \
               "sess.url() doesn't encode correctly.."

        assert self.sess.url("http://x.com?xyz=123") \
               == "http://x.com?xyz=123&sess=ABC", \
               "sess.url() doesn't encode correctly.."

        assert self.sess.url("checkout.py?auth_checkout_flag=1") \
               == "checkout.py?auth_checkout_flag=1&sess=ABC", \
               "sess.url() doesn't encode correctly.."
        

    def test_CookieSid(self):
        """
        sess should read sid from the cookie.
        """
        req = self.builder.build(cookie={"weblib.Sess":"123"},
                             querystring="weblib.Sess=ABC")
        sess = weblib.Sess(self.pool, req, weblib.Response())
        
        actual = sess._getSid()
        assert actual == "123", \
               "getSid doesn't read the cookie: %s.." % actual

    def test_QuerySid(self):
        """
        if no cookie, sess should read from the querystring
        """
        req = self.builder.build(querystring="weblib.Sess=ABC")
        sess = weblib.Sess(self.pool, req, weblib.Response())

        actual = sess._getSid()
        assert actual == "ABC", \
               "getSid doesn't read the querystring (fallback): %s" % actual


    def tearDown(self):
        del self.sess
