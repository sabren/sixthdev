"""
weblib: Classes for easy server-side web scripting in Python.
"""
__ver__="$Id$"

#### Exceptions ######################################################

class Redirect(Exception):
    """
    Raise this when you want to redirect but don't have access to
    a response object. (Eg, for testing without the RES variable,
    or just so you don't have to keep passing it down a call stack)
    """
    pass

#### utility functions ###############################################

def selectBox(name, rows, blank=None, extra=''):
    """
    display a selectbox
    #@TODO: get rid of weblib.selectBox - we have html.select now
    rows should be a sequence of (real value, displayed value, isSelected)
    """
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

def trim(s):
    """
    strips leading indentation from a multi-line string.
    for saving bandwith while making code look nice
    @TODO: this should be in handy
    """

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


def indent(s, depth=1, indenter="    "):
    """
    opposite of trim
    @TODO: this should be in handy
    """
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
   

def deNone(s, replacement=''):
    """
    replaces None with the replacement string
    @TODO: this should be in handy
    """
    # if s won't be zero, you might as well use:
    # "s or ''" instead of "deNone(s)"
    if s is None:
        return replacement
    else:
        return s
    
def uid():
    """
    unique identifier generator, for sessions, etc
    Returns a 32 character, printable, unique string
    @TODO: should be in handy
    """
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
    if s is not None:
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
        import string
        res = urllib.unquote(string.replace(what, "+", " "))

    elif type(what) == type({}):
        res = urllib.urldecode(what)
    else:
        raise "urlDecode doesn't know how to deal with this kind of data"

    return res


## sub-modules ################################################

# In all of these cases, we import a class with the same name as the
# module. This means the module basically disappears, and all the user
# sees is that weblib has a bunch of classes defined.

from Engine import Engine
from Request import Request
from Response import Response
from Sess import Sess


