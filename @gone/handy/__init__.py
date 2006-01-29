"""
Misc handy routines
"""
import os
import sys
import random
import string
import tempfile
import operator

def randpass(length=5):    
    okay = "abcdefghijkmnopqrstuvwxyz2345678923456789"
    res = ""
    for i in range(length+1):
        res += okay[random.randrange(0, len(okay))]
    return res


def reconcile(seriesA, seriesB):
    extraA = [x for x in seriesA if x not in seriesB]
    extraB = [x for x in seriesB if x not in seriesA]
    return (extraA, extraB)



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

def sendmail(mail):
    import os
    sender = os.popen("/usr/sbin/sendmail -t", "w")
    sender.write(mail)
    sender.close()


def trim(s):
    """
    strips leading indentation from a multi-line string.
    for saving bandwith while making code look nice
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
   



def uid():
    """
    unique identifier generator, for sessions, etc
    Returns a 32 character, printable, unique string
    """
    import md5, string
    tmp, uid = "", ""
    
    # first, just get some random numbers
    for i in range(64):
        tmp = tmp + chr(random.randint(0,255))

    # then make a 16-byte md5 digest...
    tmp = md5.new(tmp).digest()

    # and, since md5 is unprintable,
    # reformat it in hexidecimal:
    for i in tmp:
        uid = uid + string.zfill(hex(ord(i))[2:],2)        

    return uid


def edit(s):
    """
    launch an editor...
    """
    ed = os.environ.get("EDITOR", "vi")
    fn = tempfile.mktemp()
    tf = open(fn,"w")
    tf.write(s)
    tf.close()
    os.system("%s %s" % (ed, fn))
    return open(fn).read()


def sum(series, initial=None):
    return reduce(operator.add, series, 0)


class Everything:
    def __contains__(self, thing):
        return True
Everything=Everything()

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


def deNone(s, replacement=''):
    """
    replaces None with the replacement string
    """
    # if s won't be zero, you might as well use:
    # "s or ''" instead of "deNone(s)"
    if s is None:
        return replacement
    else:
        return s


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
        




if __name__=="__main__":
    #print edit("testing...")
    assert sum((1,2,3)) == 6
    assert 234324 in Everything
