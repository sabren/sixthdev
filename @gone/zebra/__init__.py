"""
Zebra: a text generation and reporting system

$Id$
"""
import os
import string
import lexer
from zbr2xml import Z2X
from xml2mdl import X2M
from Bootstrap import Bootstrap

###[ Utility Functions ]#######################################

def old_parse(string):
    """
    parse the old, non-xml format
    """
    return Bootstrap().toObject(Z2X().translate(string))

def parse(string):
    """
    parse the xml format
    """
    return Bootstrap().toObject(string)

def fetch(template, model={}):
    """
    fetch the template, and appy it to the model
    """
    path, filename = os.path.split(template)   
    cwd = os.getcwd()
    if path:
        os.chdir(path)

    try:
        # @TODO: make the .zb explicit in the call
        if not os.path.exists(filename):
            if os.path.exists(filename + ".zb"):
                filename += ".zb"
            else:
                raise IOError, "%s not found" % filename

        src = open(filename).read()
        if filename.endswith(".zb"):
            rpt = old_parse(src)
        else:
            rpt = parse(src)
        res = rpt.fetch(model)
    finally:
        # cleanup and go home
        os.chdir(cwd)
        
    return res



def show(template, model={}):
    """
    same as fetch(), but prints the result
    """
    print fetch(template, model)
    
def escape(s):
    """
    Escape backslashes, quotes, and newlines
    """
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
