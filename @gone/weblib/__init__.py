#
# weblib : a library for web stuff
# 


### first, import the singletons ##########################

from Request import *
request = Request()

from Response import *
response = Response()

from Sess import *
from SessPool import *
sess = {}

from Auth import *
from Perm import *


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

#### URL encoder ########################################

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




##############3


def printNormal():
    pass

def printIntercept():
    pass

## import sys
## stdout = sys.stdout
## sys.stdout = response

## ### but allow the old behavior, if needed ######

## def normalPrint():
##     sys.stdout = stdout


