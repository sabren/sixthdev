"""
Zebra: a text generation and reporting system

$Id$
"""
import string
from Generator import Generator
from Parser import Parser
from Engine import Engine
from Bootstrap import Bootstrap
import xml2mdl

###[ Utility Functions ]#######################################

def trim(s):
    """strips leading indentation from a multi-line string."""
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


def showdiff(a, b):
    assert type(a)==type(b), \
           "can't compare " + `type(a)` + " to " + `type(b)`
    if type(a)==type([]):
        a = string.join(a, "\n")
        b = string.join(b, "\n")
    return "these don't match:\n[" + a + "]\n--\n[" + b + ']'


def stripuid (uidString):
    """utility for comparing strings with embedded UID's"""
    def uidrepl(matchobj):
        return "$$UID$$"
    return re.sub ('[a-f0-9]{32}', uidrepl, uidString)



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

