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

class Finished(Exception):
    """
    Raise this when you're done with your page.
    Or call RES.end()
    """
    pass

from handy import trim
from handy import uid

def htmlEncode(s):
    """
    htmlEncode(s) ->  s with >, <, and & escaped as &gt;, &lt; and &amp;
    """
    res = ""
    for ch in s:
        if ch == ">":
            res = res + "&gt;"
        elif ch=="<":
            res = res + "&lt;"
        elif ch=="&":
            res=res + "&amp;"
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
from Request import Request, RequestBuilder, RequestData
from Response import Response
from Sess import Sess
import SessPool
