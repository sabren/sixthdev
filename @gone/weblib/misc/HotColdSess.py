"""
HotColdSess.py : DEPRECATED SESSION CLASS

THIS CLASS HAS SPORADIC BUGS RELATED TO PICKLING!!!

Hot and Cold indicates two layers of pickling... You have a
dictionary of pickled objects. This was the original Sess,
but it turns out that python sometimes has trouble parsing
one pickled string inside another.

Why two layers? It's so you can pickle objects and then
unpickle the session without having that object loaded on
the next page... Eg, in zikeshop, a Cart object used to
be stored directly in the session, so Cart had to be imported
on every page or loading the session would cause an error
(it would try to make a Cart without knowing what a cart
should be like)..

Since Zikeshop now simply stores Cart's DATA in the session,
and this HotCold business leads to weird errors anyway,
I'm just putting this class aside. If anyone wants to
put the time into fixing it, go for it.

Unfortunately, I don't have a test case that illustrates the
problem.. It's very rare. One example was putting a product
into the zikeshop session when the product had an ID of 92.
the same product with an ID of 91 or 93 worked, and a
different product given the ID 92 failed. 

All in all, I figured there just wasn't much point in all this
pickling, so we now have Sess that can't take objects without
them being imported first.

"""
__ver__="$Id$"

import weblib

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


## HotColdSess : a session handler ################

class HotColdSess:

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

    def __init__(self, pool, request, response):

        self._request = request
        self._response = response
        self._pool = pool     # where to store the data
        self._warmData = {}   # unpickled, live data
        self._coldData = {}   # still-pickled data



    ## public methods ########################

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
        import string
        
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
        "dictionary interface"
        return self._warmData.has_key(name) or self._coldData.has_key(name)


    def __setitem__(self, key, value):
        "dictionary interface"
        self._warmData[key] = value


    def __getitem__(self, key):
        "dictionary interface"
        if self._warmData.has_key(key):
            return self._warmData[key]
        
        elif self._coldData.has_key(key):
            self._warmData[key] = loads(self._coldData[key])
            return self._warmData[key]
        
        else:
            raise KeyError, key + " not found in session."


    def __delitem__(self, key):
        "dictionary interface"
        if self.has_key(key):
            if self._warmData.has_key(key): del self._warmData[key]
            if self._coldData.has_key(key): del self._coldData[key]
        else:
            raise KeyError, key


    def keys(self):
        "dictionary interface"
        # this might be faster if i used a dictionary..
        allKeys = self._coldData.keys()
        for key in self._warmData.keys():
            if not key in allKeys:
                allKeys.append(key)
        return allKeys
        
    

    def get(self, key, failObj = None):
        "dictionary interface"
        try:
            return self[key]
        except KeyError:
            return failObj

            
    def clear(self):
        "dictionary interface"
        self._warmData.clear()
        self._coldData.clear()
        self._freeze()

    ## internal methods ####################


    def _getSid(self):
        """figures out which session id to use"""

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
            import weblib
            sid = weblib.uid()

        #@TODO: add code for timeouts wrt setCookie
        if self.mode == "cookie":
            # always update the cookie
            self._response.addCookie(self.name, sid)
                
        return sid



    def _gc(self):
        """occasionally drains the sesspool"""
        import random
        if (random.random() * 100 <= self.gcProb):
            self._pool.drain(self.name, 0)
            

    def _freeze(self):
        """freezes sess and dumps it into the sesspool. call at end of page"""

        # first, merge warm and cool data:
        for key in self._warmData.keys():
            self._coldData[key] = dumps(self._warmData[key], 1)

        # now, freeze the cold stuff:
        self._pool.putSess(self.name, self.sid,
                           dumps(self._coldData, 1)) # 1 for binary





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

