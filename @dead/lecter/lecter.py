#!/usr/bin/env python
"""
lecter - a python preprocessor

   lecter is a well mannered, logical, and somewhat
   psychotic computer language that eats other languages
   for breakfast. :)

   actually, it's a preprocessor for python, adding
   the following features:

   * design by contract (require/ensure)
   * assignment operators
   * ?: ternary operator

   see also lecter-mode.el for emacs support

"""

import string, re

_indent = 0

def lectify(pyCode):
    """Strip comments, make all statements single-lined, and return a
    list of lecter lines..."""
    global _indent
    pyLines = string.split(pyCode, "\n")
    lcLines = []
    isContinued = 0

    # handle comments, blanks, and continuations
    reIgnore = re.compile("^\s*(#.*)?$")
    for line in pyLines:

        # ignore comment-lines / blanks
        if not reIgnore.match(line):
            
            # continuations:
            if isContinued:
                lcLines[-1] = lcLines[-1] + string.lstrip(line)

            wasContinued = isContinued
            
            if line[-1] == "\\":
                line = line[:-1]
                isContinued = 1
            else:
                isContinued = 0

            if not wasContinued:
                lcLines.append(line)


    # strip indentation based on first nonblank line
    # (useful for test cases, at least..)
    indent = len(lcLines[0]) - len(string.lstrip(lcLines[0]))
    for i in range(len(lcLines)):
        lcLines[i] = lcLines[i][indent:]

    return lcLines


def delistify(lcLines):
    global _indent
    """Turn a list of lines back into a python program..."""
    lcCode = ""
    for i in range(len(lcLines)):
        lcCode = lcCode + " " * indent + lcLines[i]
    return lcCode


def handleIIF(pyCode):
    return pyCode


class LecterEngine:
    def eat(self, pyCode):
        pyCode = handleIIF(pyCode)
        return pyCode


## instantiate the compiler:
Hannibal = LecterEngine()

