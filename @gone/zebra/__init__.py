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

def compile(template):
    ifp = open(template + ".zb", "r")
    data = Z2X().translate(ifp.read())
    ofp = open(template + ".zbc", "w")
    #@TODO: also use python's compiler, once the bugs are worked out.
    ofp.write(Bootstrap().compile(data))
    ofp.close()
    ifp.close()
    

def fetch(template, model={}):
    """
    fetch the template, and appy it to the model
    """
    import os.path

    path, filename = os.path.split(template)
    cwd = os.getcwd()
    if path:
        os.chdir(path)
    
    doCompile = 0
    # if existing compiled template:
    if os.path.exists(filename + ".zbc"):
        # if also uncompiled template:
        if os.path.exists(filename + ".zb"):
            # and the uncompiled is newer:
            if os.path.getmtime(filename + '.zb') \
               > os.path.getmtime(filename + '.zbc'):
                doCompile = 1
    else:
        # no existing template, so compile
        doCompile = 1

    if doCompile:
        compile(filename)

    # get the result..
    namespace = {}
    execfile(filename + ".zbc", namespace)
    res = namespace['fetch'](model)

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
