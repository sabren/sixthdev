"""
Zebra: a text generation and reporting system

$Id$
"""
import string
import lexer
from zbr2xml import Z2X
from xml2mdl import X2M
from Bootstrap import Bootstrap

###[ Utility Functions ]#######################################

def show(template, model={}):
    #@TODO: clean this up and optimize it!
    ifp = open(template + ".zbr", "r")
    data = Z2X().translate(ifp.read())
    ofp = open(template + ".zbc", "w")
    ofp.write(Bootstrap().compile(data))
    ofp.close()
    namespace = {}
    execfile(template + ".zbc", namespace)
    namespace['show'](model)
    
def escape(s):
    "Escape backslashes, quotes, and newlines"

    replace = {
        "\\":"\\\\",  # backslash
        "\n":"\\n",   # newline
        "'":"\\'",    # single quote
        "\"":"\\\""   # double quote
        }

    res = ""
    for ch in s:
        if ch in replace.keys():
            res = res + replace[ch]
        else:
            res = res + ch
    return res


def trim(s):
    "trim(s) => Strips leading indentation from a multi-line string."

    lines = string.split(s, "\n")

    # strip leading blank line
    if string.strip(lines[0]) == "":
        lines = lines[1:]

    # strip indentation
    indent = len(lines[0]) - len(string.lstrip(lines[0]))
    for i in range(len(lines)):
        lines[i] = lines[i][indent:]

    return string.join(lines, "\n")



def indent(s, depth=1, indenter="    "):
    "indent(s,depth=1,indenter='    ') => Indent a multi-line string."

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
