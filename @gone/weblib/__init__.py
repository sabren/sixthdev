#
# weblib : a library for web stuff
# 
##########################################################

# start with some utility functions... 


### unique identifier generator, for sessions, etc #######

def uid():
    """Returns a 32 character, printable, unique string"""
    import md5, whrandom, string
    tmp, uid = "", ""
    
    # first, just get some random numbers
    for i in range(64):
        tmp = tmp + chr(whrandom.randint(0,255))

    # then make a 16-byte md5 digest...
    tmp = md5.new(tmp).digest()

    # and, since md5 is unprintable,
    # reformat it in hexidecimal:
    for i in tmp:
        uid = uid + string.zfill(hex(ord(i))[2:],2)        

    return uid


### HTML encoder #########################################

import htmlentitydefs

#@TODO: is there really no built-in way to turn a hash inside out?
_entitymap = {}
for i in htmlentitydefs.entitydefs.keys():
    _entitymap[htmlentitydefs.entitydefs[i]] = i


def htmlEncode(s):
    res = ""
    for ch in s:
        if _entitymap.has_key(ch):
            res = res + "&" + _entitymap[ch] + ";"
        else:
            res = res + ch
    return res

#### URL encoding ########################################

def urlEncode(what):
    """This works the way ASP's urlEncode does, OR lets you do it
    the urllib way (using a dict)"""
    
    res = None
    import urllib
    if type(what) == type(""):
        res = urllib.quote(what)
    elif type(what) == type({}):
        res = urllib.urlencode(what)
    else:
        raise "urlEncode doesn't know how to deal with this kind of data"

    return res


def urlDecode(what):
    res = None
    import urllib

    if type(what) == type(""):
        res = urllib.unquote(what)
        # is this right?!?!?!?
        import string
        res = string.replace(res, "+", " ")

    elif type(what) == type({}):
        res = urllib.urldecode(what)
    else:
        raise "urlDecode doesn't know how to deal with this kind of data"

    return res



### and now, the herd of singletons ##########################

# In all of these cases, importing * imports a class with the
# same name as the module. This means the module basically
# disappears, and all the user sees is that weblib has
# a bunch of classes defined.

from Engine import *
from Request import *
from Response import *
from Sess import *
from Auth import *
from Perm import *

# the config module is different. It defines a SessPool
# object called pool... This is why we don't import SessPool
# in the section above.
#
# we put it in a seperate module so that it would be easy to
# customize.

from config import pool

# We don't want to define the singletons more than once, though.
# Otherwise, we'd lose session data and waste time everytime some
# subfuction somewhere said "import weblib"... So, we check for
# __weblib__ in the global namespace first.

import __builtin__

if not __builtin__.__dict__.get("__weblib__"):

    class CgiResponse(Response):
        """In CGI-mode, we want to insert headers automatically..."""
        
        def __init__(self):
            import sys
            Response.__init__(self, out=sys.stdout)
            sys.stdout = self


        def __del__(self):
            self.flush()
            import sys
            sys.stdout = self.out

    import sys
    stdout = sys.stdout

    request = Request()
    response = CgiResponse()

    sess = Sess(pool)
    auth = Auth()
    perm = Perm()

    __builtin__.__weblib__ = 1
