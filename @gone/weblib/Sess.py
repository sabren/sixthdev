"""
Sess.py : emulates PHPLIB's session support in python

$Id$

@TODO: python-style license lingo
"""

import weblib
import UserDict


try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


## Sess : a session handler ################

class Sess:

    ## attributes ##########################

    sid = ""
    name = "weblib.Sess"
    mode = "cookie"
    fallbackMode = "get"
    magic = "abracadabra"
    lifetime = 0
    gcTime = 1440   # purge sessions older than 24 hrs (1440 mins)
    gcProb = 1      # probability of garbage collection as a %


    ## constructor ############################

    def __init__(self, pool=None, engine=weblib):

        self.engine = engine

        if pool is None:
            from weblib.config import pool
            
        self._pool = pool     # where to store the data
        self._warmData = {}   # unpickled, live data
        self._coldData = {}   # still-pickled data



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
        self._thaw()
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


    def stop(self):
        self._freeze()



    ## dictionary methods ####################
    
    # note that we can't subclass UserDict anymore because we're
    # dealing with two internal dictionaries..
    #
    # We use two dictionaries so that things are only unpickled when
    # you ask for them. This may or may not speed things up, but it
    # lets us pickle objects without forcing the engine to declare
    # them first.
    #
    # ie: To unpickle an instance of class X, class X must be defined
    # in the current namespace. So, if you pickle an X instance on one
    # page, every other page would have to import X. That's a pain,
    # because you can easily break unrelated pages. The two-dictionary
    # setup prevents this situation. With two dictionaries, you only
    # have to import X on pages that actually use the instance.
    #
    # The "warm" dictionary is the live data. The "cold" dictionary
    # is the pickled data we're not using right now.
    

    def has_key(self, name):
        return self._warmData.has_key(name) or self._coldData.has_key(name)


    def __setitem__(self, key, value):
        self._warmData[key] = value


    def __getitem__(self, key):
        if self._warmData.has_key(key):
            return self._warmData[key]
        
        elif self._coldData.has_key(key):
            self._warmData[key] = loads(self._coldData[key])
            return self._warmData[key]
        
        else:
            raise KeyError, key + " not found in session."


    def __delitem__(self, key):

        if self.has_key(key):
            if self._warmData.has_key(key): del self._warmData[key]
            if self._coldData.has_key(key): del self._coldData[key]
        else:
            raise KeyError, key


    def keys(self):
        # this might be faster if i used a dictionary..
        allKeys = self._coldData.keys()
        for key in self._warmData.keys():
            if not key in allKeys:
                allKeys.append(key)
        return allKeys
        
    

    def get(self, key, failObj = None):
        try:
            return self[key]
        except KeyError:
            return failObj

            
    def clear(self):
        self._warmData.clear()
        self._coldData.clear()
        self._freeze()

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
            

    def _freeze(self):
        """freezes sess and dumps it into the sesspool. call at end of page"""

        # first, merge warm and cool data:

        for key in self._warmData.keys():
            self._coldData[key] = dumps(self._warmData[key], 1)

        # now, freeze the cold stuff
        
        self._pool.putSess(self.name, self.sid, dumps(self._coldData, 1)) # 1 for binary




    def _thaw(self):
        """gets a frozen sess out of the sesspool and thaws it out"""
        frozen = self._pool.getSess(self.name, self.sid)
        if frozen is None:
            self._coldData = {}
        else:
            self._coldData = loads(frozen)

        # nothing is actually warm until you use it:
        self._warmData = {}



if __name__ == "__main__":
    pass

