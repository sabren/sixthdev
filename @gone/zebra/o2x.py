#!/usr/bin/env python
#################################################
## o2x : emacs outline mode to xml             ##
##                                             ##
## version 1.0  created 11/23/1999             ##
## by sabren@manifestation.com                 ##
##                                             ##
## under the GNU Lesser GPL, found at:         ##
##    http://www.gnu.org/copyleft/lesser.html  ##
#################################################
## o2x home page:                              ##
## http://www.sabren.com/code/python/          ##
#################################################
##
## synopsis:
## converts emacs outline mode files to xml
##
## example outline file (input):
## -----------------------------
## * top attribute="whatever"
## this is part of the top!
## try & escape <this>!!
## ** middle
## middle is a child of the top!
## *** bottom
## bottom is a child of middle
## ** /
## we're back in the top!
## -----------------------------
##
## here's what that becomes:
## -----------------------------
## <?xml version="1.0"?>
## <top attribute="whatever">
## this is part of the top!
## try &amp; escape &lt;this&gt;!!
## <middle>
## middle is a child of the top!
## <bottom>
## bottom is a child of middle
## </bottom>
## </middle>
## we're back in the top!
## </top>
## -----------------------------
#################################################
# changelog
# 1.1 : 1219.1999 - added support for \*
#       (so the first char on a line can be *)
#       no longer inserts newline at start of tag
#################################################
import string

# exceptions are fun for the whole family:
o2xException = "o2x Error"

# declare it as a function, so you can use
# it in your own python programs:
#
# from o2x import o2x
# print o2x(sometext)

def o2x ( text ):
    res   = "" # results to return
    stack = [] # stack of xml tags
    lines = string.split(text, "\n")
    depth = lastdepth = 0
    lineno = 0

    ## first add the header
    res = '<?xml version="1.0"?>\n'

    for line in lines:
        lineno = lineno + 1

        # let blank lines through:
        if not string.strip(line):
            res = res + "\n"
            continue

        # escape XML characters (&, <, and >)
        line = string.replace(line, "&", "&amp;");
        line = string.replace(line, "<", "&lt;");
        line = string.replace(line, ">", "&gt;");

        # handle * lines (outline branches):
        if (line) and (line[0] == "*"):

            # first, how deep are we?
            depth = 0
            while line[depth] == "*":
                depth = depth + 1

            if depth > lastdepth + 1:
                raise o2xException, "Invalid depth at line " + `lineno`

            for difference in range (lastdepth - depth + 1):
                tag = stack[-1]; stack = stack[:-1]
                res = res + "</" + tag + ">\n"

            tag = string.strip(line[depth:])

            # / is just a fake way to escape back to a certain depth..
            # so don't actually count it:
            if tag != "/":

                # opening tag has attributes:
                res = res + "<" + tag + ">"

                # but a closing tag doesn't:
                firstspace = string.find(tag, " ")
                if firstspace > -1:
                    tag = tag[:firstspace]

                if tag:
                    stack.append(tag)

            # remember how deep we were:
            lastdepth = depth

        # now handle non-* lines (outline leaves)
        else:
            # \* lets you put *'s at the front
            if line[:2] == "\\*":
                line = "*" + line[2:]
            res = res + line + "\n"

    while len(stack):
        # pop the last thing off the stack:
        tag = stack[-1]; stack = stack[:-1]
        res = res + "</" + tag + ">\n"

    return res


## if this module is invoked from the command line, expect
## a parameter giving the name of an emacs outline file.

if __name__ == "__main__":
    import sys

    try:
        outline = open(sys.argv[1], "r").read()
    except:
        sys.stderr.write("------------------------------\n")
        sys.stderr.write("something's wrong!\n")
        sys.stderr.write("------------------------------\n")
        sys.stderr.write("usage: o2x.py <outlinefile>\n")
        sys.stderr.write("Converts an emacs outline file to xml.\n")

    if outline:
        try:
            print o2x(outline)
        except o2xException, extraInfo:
            sys.stderr.write("error:" + extraInfo)

# end #

