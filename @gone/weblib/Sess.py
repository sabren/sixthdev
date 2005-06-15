"""
Sess.py : emulates PHPLIB's session support in python
"""
__ver__="$Id$"


# NOTE: this module used to have two layers of pickling
# _warmdata and _coldData, which allowed it to store
# objects without having to import that object on every page.
# but python seems to have trouble pickling a dictionary of
# prepickled objects, so that method is deprecated.. If anyone
# really needs it, look at HotColdSess.py (the old version)

import string
import UserDict
import weblib
import whrandom

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


## Sess : a session handler ################

class Sess(UserDict.UserDict):
    # can't get rid of this __super until b/c UserDict is old-style class
    __super = UserDict.UserDict

    ## constructor ############################

    def __init__(self, pool, request, response):
        self.__super.__init__(self)
        self._request = request
        self._response = response
        self._pool = pool # where to store the data
        
        self.sid = ""   
        self.name = "weblib.Sess"
        self.mode = "cookie"
        self.fallbackMode = "get"
        self.magic = "abracadabra"
        self.lifetime = 0
        self.gcTime = 1440   # purge sessions older than 24 hrs (1440 mins)
        self.gcProb = 1      # probability of garbage collection as a %

        # a function to make new sids
        self.sidmaker = weblib.uid


    ## public methods ########################

    def pop(self, key):
        res = self.data[key]
        del self.data[key]
        return res

    def start(self, sid=None):
        """
        starts the session. call at the top of the page.

        Not really sure why you'd ever want to pass
        the sid variable in.. except possibly for testing..
        but PHPLIB lets you do it, so I guess I will, too.
        """
        if sid is None:
            self.sid = self._getSid()
        else:
            self.sid = sid
        #@TODO: this was an emergiceny hack. fix me!
        from Cookie import Morsel
        if isinstance(self.sid, Morsel):
            self.sid = self.sid.value
        self._thaw()        
        self._gc()


    def abandon(self):
        """
        abandons the session
        """
        self.clear()
        self.sid = ""


    def url(self, oldurl):
        """
        returns oldurl, but referencing the current session.

        If in get mode, the current session id is attached to this
        URL, else the URL is returned unmodified.
        """
        # if there's not already a querystring:
        if string.find(oldurl, "?") == -1:
            return oldurl + "?%s=%s" % (self.name, self.sid)
        else:
            return oldurl + "&%s=%s" % (self.name, self.sid)

        #@TODO: have sess.url overwrite old sess ID's in querystring


    def stop(self):
        """
        Call at end of page to stop the session. (it calls _freeze)
        """
        self._freeze()
        self._pool.done()



    ## internal methods ####################

    def newUniqueSid(self):
        sid = None        
        while sid is None:
            sid = self.sidmaker()
            if self._pool.getSess(self.name, sid):
                sid = None
        return sid

    def _getSid(self):
        """
        figures out which session id to use
        """
        sid = None

        # first try to get the sid from the browser..
        for mode in (self.mode, self.fallbackMode):
            if sid is None:
                try:
                    if mode == "cookie":
                        sid = self._request.cookie[self.name]
                    elif mode == "get":
                        sid = self._request.query[self.name]
                    else:
                        raise "Unknown mode: " + mode
                except KeyError:
                    pass

        # if that didn't work, just make one up..
        if sid is None:
            sid = self.newUniqueSid()

        #@TODO: add code for timeouts wrt setCookie
        if self.mode == "cookie":
            # always update the cookie
            self._response.addCookie(self.name, sid)
                
        return sid



    def _gc(self):
        """
        occasionally drains the sesspool
        """
        if (whrandom.random() * 100 <= self.gcProb):
            self._pool.drain(self.name, 0)
            

    def _freeze(self):
        """
        freezes sess and dumps it into the sesspool. call at end of page
        """

        # freeze the data stuff:
        self._pool.putSess(self.name, self.sid,
                           dumps(self.data, 0)) # 1=binary, 0=ascii

    def _thaw(self):
        """
        gets a frozen sess out of the sesspool and thaws it out
        """
        frozen = self._pool.getSess(self.name, self.sid)
        if frozen is None:
            self.data = {}
        else:
            self.data = loads(frozen)

