# handy routines
# $Id$

import string

def xmlEncode(s):
    """
    xmlEncode(s) ->  s with >, <, and & escaped as &gt;, &lt; and &amp;
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
        


def sendmail(msg):
    """
    sendmail(msg) -> None  (sends an email.)
    """
    print '<pre style="background:gold; border:solid black 1px; color:black">'\
          + xmlEncode(msg) + '</pre>'



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

def readable(bytes):
    """
    convert a bytecount into human-readable text
    """
    x = bytes
    b = x % 1000; x-=b; x/=1000
    k = x % 1000; x-=k; x/=1000
    m = x % 1000; x-=m; x/=1000
    g = x % 1000; x-=g; x/=1000
    if g: return str(g) + "." + string.zfill(str(m),3)[0] + "G"
    if m: return str(m) + "." + string.zfill(str(k),3)[0] + "M"
    if k: return str(k) + "." + string.zfill(str(b),3)[0] + "k"
    return str(b)
