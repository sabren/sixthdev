"""
Sess.py : emulates PHPLIB's session support in python

@TODO: python-style license lingo
"""

import weblib
import UserDict

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

## Sess : a session handler ################

class Sess(UserDict.UserDict):

    ## attributes ##########################

    def __init__(self, pool=None, engine=weblib):

        self.engine = engine
        # if we don't have an engine, store a pointer to us in weblib:
        if self.engine is weblib:
            weblib.sess = self
        
        self.sid = ""
        self.name = "weblib.Sess"
        self.mode = "cookie"
        self.fallbackMode = "get"
        self.magic = "abracadabra"
        self.lifetime = 0
        self.gcTime = 1440 # purge sessions older than 24 hrs (1440 mins)
        self.gcProb = 1    # probability of garbage collection as a %
        
        # naturally, you keep your Sess in a SessPool.. :)
        
        self._pool = pool   # where to store the data
        self.data = {}      # all the stuff to remember

    ## public methods ########################

    def start(self, sid=None):
        """starts the session. call at the top of the page.

        Not really sure why you'd ever want to pass
        the sid variable in.. except possibly for testing..
        but PHPLIB lets you do it, so I guess I will, too.
        """
        if sid is None:
            self.sid = self._getSid()
        else:
            self.sid = sid
        self.thaw()
        self._gc()


    def abandon(self):
        """abandons the session"""
        self.sid = ""
        self.clear()

    def url(oldurl):
        """ returns oldurl, but referencing the current session.

        If in get mode, the current session id is attached to this
        URL, else the URL is returned unmodified.

        """
        # @TODO: code url()
        return oldurl

    def freeze(self):
        """freezes sess and dumps it into the sesspool. call at end of page"""
        self._pool.putSess(self.name, self.sid, dumps(self.data, 1)) # 1 for binary

    def thaw(self):
        """gets a frozen sess out of the sesspool and thaws it out"""
        frozen = self._pool.getSess(self.name, self.sid)
        if frozen is None:
            self.data = {}
        else:
            self.data = loads(frozen)

    ## internal methods ####################

    def _getSid(self):
        """figures out which session id to use"""

        sid = None
        
        # first try to get the sid from the browser..
        try:
            if self.mode == "cookie":
                sid = self.engine.request.cookie[self.name]
            elif self.mode == "get":
                sid = self.engine.request.querystring[self.name]
            else:
                raise "Unknown Sess.mode: " + self.mode
        except KeyError:
            pass

        # if that didn't work, just make one up..
        if sid is None:
            import weblib
            sid = weblib.uid()
            #@TODO: add code for timeouts wrt setCookie
            if self.mode == "cookie":
                self.engine.response.addCookie(self.name, sid)
                
        return sid

    def _gc(self):
        """occasionally drains the sesspool"""
        import whrandom
        if (whrandom.random() * 100 <= self.gcProb):
            self._pool.drain(self.name, 0)
            


if __name__ == "__main__":
    pass

