#!/usr/bin/env python
"""
lecter - a python preprocessor

   lecter is a well mannered, logical, and somewhat
   psychotic computer language that eats other languages
   for breakfast. :)

   actually, it's a preprocessor for python, adding
   the following features:

   * evil curlies:
      for x in range(100) {
          print x
      }

      #or:

      for x in range(100):
          print x
          
   * design by contract (require/ensure/implies)
   * assignment operators ( +=, -=, /=, *= )
   * immediate if:
         print 'x is', x > 0 ? 'positive' : 'negative'
   * foreach someSequence: print this
   * easy class access:
         class.x = 1  # translates to: self.__class__.x = 1
   * switch statement:
         switch x:
         case 1:
             pass
         case 2:
             pass
         case in (3,5):
             pass
   * extended 'try' syntax:
         try:
             print 'do something'
         except:
             print 'catch errors'
         finally:
             print 'clean up' # not allowed in real Python

   maybe someday:
   * /regexp/  and  x =~ /regexp/

   see also lecter-mode.el for emacs support (well.. someday)

"""

import string, re

_indent = 0

def stripUselessLines(lcCode):
    """remove all comment-lines and blank lines from lecter source.
    NB: this does NOT delete comments at the END of a line, and it
    makes sure every line is followed by a \n"""
    res = ""
    for line in string.split(lcCode,"\n"):
        stripped = string.strip(line)
        # ignore comment lines and blanks:
        if (stripped != '') and (stripped[0] != '#'):
            res = res + line + "\n"
    # strip the final, so it's easier to split() later:
    res = res[:-1]
    return res


def deTabify(s):
    """Replace each tab in s with 8 spaces"""
    return string.replace(s, '\t', '        ')


def deLectify(lcCode):
    """Strip comments, turn curlies into python equivalents,
    make all statements single-lined, and otherwise clean up shop.
    Returns a list lines..."""
    global _indent

    # first, simplify the code a bit...
    lcCode = deTabify(stripUselessLines(lcCode))

    # start building a list..
    newLines = []
    oldLines = string.split(lcCode, "\n")
    
    isContinued = 0
    openStack = [''] # tracks open parens, etc..
    opener = {"]" : "[",
              ")" : "(",
              "}" : "{"}
    inString = 0
    
    tokOperators = ('in', 'is', '=', '==', '!=', '<>',
                    '>', '<', '<=', '>=', '%', '+', '-',
                    '*', '/', '+=', '-=', '*=', '/=',
                    '<<', '>>') # did I miss any?

    for lpos in range(len(oldLines)):
        line = oldLines[lpos]

        ## we're going to go through the line character
        ## by character and keep track of what context
        ## we're in...
        ##
        ## this would probably be a whole lot simpler
        ## with a lexer/parser, but how do you write
        ## something like that for a language whose
        ## syntax changes on the fly? Maybe that's
        ## what flex/plex is all about...

        p = '' # previous char
        token = '' # current token
        ptoken = '' # previous token
        for cpos in range(len(line)):
            c = line[cpos] # current char
            
            if not inString:

                # quote or doublequote enters string mode:
                if (c in '"\''):
                    openStack.append(c)
                    inString = 1

                # pound sign signals a comment, so ignore rest of line.
                elif c == '#':
                    line = string.rstrip(line[:cpos])
                    break # out of "for c in line" loop
                    
                ## make sure []'s and ()'s balance:
                elif c in '[(':
                    openStack.append(c)
                elif c in ')]':
                    o = openStack.pop()
                    assert o == opener[c], \
                           "unbalanced: " + c + " doesn't match " +  o

                ## "{" either starts a block or a dictionary
                ## my rule is that if we're not in the middle
                ## of an expression, it's a block.. more
                ## specifically, it's ALWAYS a block UNLESS
                ## we've got something in the openStack, eg:
                ## 
                ##    mytuple = ("a", {}, {})
                ##
                ## or the previous token was an operator
                ## that works with dicts.. so this:
                ##
                ## for i in {'a':1, 'b':2}.keys() {
                ##    print 'hello}{ :)'
                ## }
                ##
                ## ... does the right thing.. But this
                ## gives a syntax error:
                ##
                ## {'a':1}
                ##
                ## which is just fine and dandy with me,
                ## since I can't think of a use for that
                ## right now anyway. (I may make an
                ## exception later on if there's ever
                ## an interactive lecter)

                elif c == "{":
                    if (openStack[-1] not in ('',':')):
                        # we're inside some kinda structure
                        # so just assume it's a dict..
                        openStack.append(c)
                    elif (ptoken in tokOperators):
                        # we're in some sort of expression,
                        # so pretend it's a dict.
                        # (actually, some operators don't
                        # apply to dicts, but that's okay
                        # because they don't apply to
                        # blocks, either...)
                        openStack.append(c)
                    else:
                        # it's a block!
                        openStack.append(':')
                        # first, blank out the curly..
                        line = line[:cpos] + ' ' + line[cpos+1:]
                        line = string.rstrip(line)
                        if line=='':
                            # it was the only thing on the line,
                            # so the previous line started the block..
                            # eg:
                            # try
                            # {
                            #    ....
                            # }
                            newLines[-1] = newLines[-1] + ':'
                        else:
                            # this line is the block
                            line = line + ':'
                            
                        #@TODO: now I can muddle whitespace... muahahaha.

                elif c=='}':
                    o = openStack.pop()
                    if o == ':':
                        # just pretend it isn't there...
                        # i think that's the right thing, anyway..
                        line = line[:cpos] + ' ' + line[cpos+1:]

                    else:
                        assert o == '{', \
                           "unbalanced: " + c + " doesn't match " +  o

                elif c ==' ':
                    ptoken = token
                    token = ''
                else: #not a special character:
                    token = token + c
                        
            else: # we are in a string
                
                # might be a single or double quoted string,
                # so just compare the last value on openstack:
                if (c == openStack[-1]) and (p != '\''):
                    inString = 0
                    openStack.pop()
                
            p = c # c becomes the "previous" character

        # if we've blanked it out (like if it's a "}")
        #just move on to the next one:
        if string.strip(line) == "":
            break        

        # continuations:
        if isContinued:
            newLines[-1] = newLines[-1] + string.lstrip(line)

        wasContinued = isContinued

        if line[-1] == "\\":
            line = line[:-1]
            isContinued = 1
        else:
            isContinued = 0

        if not wasContinued:
            newLines.append(line)


    # strip indentation based on first nonblank line
    # (useful for test cases, at least..)
    indent = len(newLines[0]) - len(string.lstrip(newLines[0]))
    for i in range(len(newLines)):
        newLines[i] = newLines[i][indent:]

    return newLines


def delistify(lcLines):
    global _indent
    """Turn a list of lines back into a python program..."""
    lcCode = ""
    for i in range(len(lcLines)):
        lcCode = lcCode + " " * indent + lcLines[i]
    return lcCode


def handleIIF(lcCode):
    pyCode = lcCode
    return pyCode


class LecterEngine:
    def eat(self, pyCode):
        pyCode = handleIIF(pyCode)
        return pyCode


## instantiate the compiler:
Hannibal = LecterEngine()

