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


