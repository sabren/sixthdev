"""
Classes for easy server-side web scripting in Python.

$Id$
"""

# start with some utility functions... 


#### selectBox() ####################################################


def selectBox(name, rows, blank=None, extra=''):
    """rows should be a sequence of (real value, displayed value, isSelected)"""
    res = '<select name="%s" %s>\n' % (name, extra)
    if blank is not None:
        res = res + '<OPTION value="%s">&nbsp;</OPTION>\n' % blank
    for row in rows:
        res = res + '<OPTION value="%s"' % row[0]
        if row[2]:
            res = res + " SELECTED"
        res = res + '>%s</OPTION>\n' % row[1]
    res = res + '</select>'
    return res



#### trim() for saving bandwith while making code look nice ####

def trim(s):
    """strips leading indentation from a multi-line string."""

    import string
    lines = string.split(s, "\n")

    # strip leading blank line
    if lines[0] == "":
        lines = lines[1:]
        
    # strip indentation
    indent = len(lines[0]) - len(string.lstrip(lines[0]))
    for i in range(len(lines)):
        lines[i] = lines[i][indent:]

    return string.join(lines, "\n")



#### indent() for the opposite of trim ##########################

def indent(s, depth=1, indenter="    "):
    import string
    lines = string.split(s, "\n")

    # don't indent trailing newline
    trailer = ""
    if lines[-1] == "":
        lines = lines[:-1]
        # BUT.. add it back in later
        trailer = "\n"
        
    for i in range(len(lines)):
        lines[i] = (indenter * depth) + lines[i]
        
    return string.join(lines, "\n") + trailer
   

#### deNone() replaces None with the replacement string ##########

def deNone(s, replacement=''):
    # if s won't be zero, you might as well use:
    # "s or ''" instead of "deNone(s)"
    if s is None:
        return replacement
    else:
        return s
    


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
del i


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


## sub-modules ################################################

# In all of these cases, we importsa class with the
# same name as the module. This means the module basically
# disappears, and all the user sees is that weblib has
# a bunch of classes defined.

from Actor import Actor
from Engine import Engine
from Request import Request
from Response import Response
from Sess import Sess
from Auth import Auth
from Perm import Perm


# note that the actual singletons (request, response, etc)
# are not created unless you do "import weblib.script", or
# create an Engine.


# the config module is different. It defines a SessPool
# object called pool... This is why we don't import SessPool
# in the section above.
#
# we put it in a seperate module so that it would be easy to
# customize.

from config import *


