"""
Sess.py : emulates PHPLIB's session support in python

@TODO: python-style license lingo
"""

from Request import request

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

## Sess : a session handler ################

class Sess:

    ## attributes ##########################

    def __init__(self, pool):
        self.sid = ""
        self.name = "weblib"
        self.mode = "cookie"
        self.fallbackMode = "get"
        self.magic = "abracadabra"
        self.lifetime = 0
        self.gcTime = 1440 # purge sessions older than 24 hrs (1440 mins)
        self.gcProb = 1    # probability of garbage collection as a %
        
        # naturally, you keep your Sess in a SessPool.. :)
        
        self._pool = pool   # where to store the data
        self._bag = {}      # all the stuff to remember

    ## public methods ########################

    def start(self, sid=""):
        """starts the session. call at the top of the page

        Not really sure why you'd ever want to pass
        the sid variable in.. except possibly for testing..
        but PHPLIB lets you do it, so I guess I will, too.
        """
        if sid == "":
            self.sid = self._getSid()
        else:
            self.sid = sid
        if __debug__:
            print "sid =" + self.sid
        self.thaw()
        self._gc()


    def abandon(self):
        """abandons the session"""
        self.sid = ""
        self._bag = {}

    def url(oldurl):
        """ returns oldurl, but referencing the current session.

        If in get mode, the current session id is attached to this
        URL, else the URL is returned unmodified.

        """
        # @TODO: code url()
        return oldurl

    def freeze(self):
        """freezes sess and dumps it into the sesspool. call at end of page"""
        self._pool.putSess(self.name, self.sid, dumps(self._bag))

    def thaw(self):
        """gets a frozen sess out of the sesspool and thaws it out"""
        frozen = self._pool.getSess(self.name, self.sid)
        if frozen is None:
            self._bag = {}
        else:
            self._bag = loads(frozen)


    ## dictionary methods #####################   
    ## ... guess I coulda just extended UserDict.. <shrug> :)
    
    def __getitem__(self, key):
        return self._bag[key]
    
    def __setitem__(self, key, value):
        self._bag[key] = value

    def __delitem__(self, key):
        del self._bag[key]

    def __len__(self):
        return len(self._bag)

    def keys(self):
        return self._bag.keys()

    def has_key(self, key):
        return self._bag.has_key(key)


    ## internal methods ####################

    def _getSid(self):
        """figures out which session id to use"""

        sid = ""
        
        # first try to get the sid from the browser..
        try:
            if self.mode == "cookie":
                sid = request.cookie[self.name]
            elif self.mode == "get":
                sid = request.querystring[self.name]
            else:
                raise "Unknown Sess.mode: " + self.mode
        except KeyError:
            pass

        # if that didn't work, just make one up..
        if sid == "":
            import unique
            sid = unique.uid()
                
        return sid

    def _gc(self):
        """occasionally drains the sesspool"""
        import whrandom
        if (whrandom.random() * 100 <= self.gcProb):
            self._pool.drain(self.name, 0)
            

## SessPool : for holding frozen Sesses :) ##########################

class SessPool:

    """The default, SessPool uses a flat text file,
    so you should subclass it, or just build your own object with the
    same interface (getSess(), setSess(), and drain())..."""
    
    def __init__(self, filename):
        import dumbdbm
        self.storage = dumbdbm.open(filename,"c")
        
    def getSess(self, name, sid):
        """returns the sess with the specified name and id, or None"""
        if self.storage.has_key(`name`+`sid`):
            return self.storage[`name` + `sid`]
        else:
            return None

    def putSess(self, name, sid, frozensess):
        """stores a frozen sess with the specified name and id"""
        self.storage[`name` + `sid`] = frozensess

    def drain(self, name, sincewhen):
        """(should) performs garbage collection to kill off old sesses"""
        # 'cept this is just a dummy version, and it don't do nuttin. :)
        pass


if __name__ == "__main__":
    pass

"""
### this should all happen in the framework ###
from weblib import sess
sesspool = weblib.SessPool()
sess.start(sesspool)

### this happens inside your code ###
sess["x"] = sess["x"] + 1
### and this really ought to happen in zebra: ###
print "you have visited this page", sess["x"], "times."

### this happens back in the framework... ###
sess.freeze()
"""
