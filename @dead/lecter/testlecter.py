#
# testlecter.py - test cases for lecter
#

import unittest
# at-> http://www.xprogramming.com/ftp/TestingFramework/python/pyunit-1.0.zip

import weblib.uid
import re, string
import lecter


def stripuid (uidString):
    """utility for comparing strings with embedded UID's"""
    def uidrepl(matchobj):
        return "$$UID$$"
    return re.sub ('[a-f0-9]{32}', uidrepl, uidString)


def showdiff(a, b):
    assert type(a)==type(b), \
           "can't compare " + `type(a)` + " to " + `type(b)`
    if type(a)==type([]):
        a = string.join(a, "\n")
        b = string.join(b, "\n")
    return "these don't match:\n[" + a + "]\n--\n[" + b + ']'

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


############### main test class: #####################
class lecterTestCase(unittest.TestCase):

    def checkStripUselessLines(self):
        output = lecter.stripUselessLines(trim("""
        #simple comment
        
        x = 1 # end of line comment
        print '#not a comment'
        print \"#not a comment\"
        """))

        goal = trim("""
        x = 1 # end of line comment
        print '#not a comment'
        print \"#not a comment\"""")

        assert goal==output, showdiff(goal, output)

    def checkDeLectifyBalanced(self):

        # this should work:
        lecter.deLectify("([][][[[]]][([()])])")

        # let's try for an error:
        unbalanced = 0
        try:
            # this should not:
            lecter.deLectify("([][][[[]]]][([()])])")
        except:
            unbalanced = 1

        assert unbalanced, "didn't catch unbalanced []()'s"


    def checkDeLectifyCurlies(self):
        # should not give syntax errror:
        output = lecter.deLectify(trim("""
        for i in {'a':1, 'b':2}.keys() {
            print 'hello}{ :) ' # just to mess with it :)
        }
        """))

        goal = [
        "for i in {'a':1, 'b':2}.keys():",
        "    print 'hello}{ :) '",
        ]

        assert output==goal, showdiff(output, goal)

    def nocheckComplexDeLectify(self):
        """does it strip comments and consolidate multi-line statements?"""

        output = lecter.deLectify("""
        print 'keep this # comment'
        print ")#look#a-Testwith\\nEmacs\\\\Cruft\\"andEscapes!"
        
        set = [1, 2,
               3, 4] # just a list
        for y in set:
            print "this is a
                split line"
            print "and so " \
              + "is this"
        """) #"# <- more cruft

        goal = [
            'print \'keep this # comment\'',
            'print ")#look#a-Testwith\\nEmacs\\\\Cruft\\"andEscapes!"',
            'set = [1, 2, 3, 4]',
            'for y in set:',
            '    print "this is a \\n        split line"',
            '    print "and so " + "is this"']

        assert output == goal, showdiff(output, goal)


    ## makes sure lecter correctly parses lines
    def checkSimpleDeLectify(self):
        result = lecter.deLectify(r"""
        try:
            print "hello,", \
                  "world!!"


        except:
        # this line should be ignored...
            # this one too... \
            "but not this!"
            print "something happened."
        """)

        assert result == [
            'try:',
            '    print "hello,", "world!!"',
            'except:',
            '    "but not this!"',
            '    print "something happened."'
            ], "deLectify doesn't parse lines correctly."


    ## makes sure lecter handles the basic syntax for ?:
    ##@TOODO: turn this back on
    def scheckSimpleIIF(self):
        result = stripuid(Hannibal.eat("""
        catlover = 1
        pet = catlover ? "cat" : "dog"
        """))

        assert result == """
        catlover = 1
        if catlover:
            $$UID$$ = "cat"
        else:
            $$UID$$ = "dog"
        pet = $$UID$$
        """, "simple immediate if (:?) support isn't working."


    ## @TODO: Can Lecter handle """x = (test ? 5 : (4)) + 5""" ??
    def checkComplexIIF(self):
        pass


    ## is lecter a BadAss? :)
    def checkBadAss(self):
        pass # you better believe it. <g>


### run the tests ###########################################


def run():
    suite = unittest.TestSuite()
    for t in dir(lecterTestCase):
        if t[:5] == "check":
            suite.addTest(lecterTestCase(t))

    result = unittest.TextTestRunner().run(suite)
    
if __name__=="__main__":
    run()

############################################################
############################################################
############# It's all junk below this line ################
############################################################
############################################################

### @TODO: clean all this crap up and put it up top
if 1==0:    
    suite = unittest.TestSuite()

#@TODO: move uid out of weblib..
#@TODO: reuse that generic routine I made for weblib..
#@TODO: add routine for stripping continuations, comments, multilines, etc.
#@TODO: map lines in generated .py source to lines in .lc source? (for error handling)

## maybe add some sort of test case for:
## checkShlex ? - would require a lexer, probably..
## checkIterator ?- "foreach" - perhaps using "this" as keyword?
## checkBeStrict
## checkBeEvil
## checkConst

    ## what about complex stuff like # \'s and """'s ?
    ## ..stuff for which I'd need a real parser (at least a lexer)
##    suite.addTest(lecterTestCase("checkComplexListify"))
    
    # and can we conditionally remove chunks a la IFDEF?
##    suite.addTest(lecterTestCase("checkListifyConst"))
    # and can we put them back together when the work is done?
##    suite.addTest(lecterTestCase("checkListify"))
    
##     # proper indentation level for generated python
##     suite.addTest(lecterTestCase("checkIndentation"))

##    # the :? (immediate if) operator
##    suite.addTest(lecterTestCase("checkSimpleIIF"))
##    suite.addTest(lecterTestCase("checkComplexIIF"))

##     # design by contract
##     suite.addTest(lecterTestCase("checkRequire"))
##     suite.addTest(lecterTestCase("checkEnsure"))

##     # stuff for the whitespace whiners:
##     suite.addTest(lecterTestCase("checkCurlies"))
##     suite.addtest(lecterTestCase("checkCurlyWords"))
##     suite.addTest(lecterTestCase("checkEnd"))
##     suite.addTest(lecterTestCase("checkEndIf"))
##     suite.addTest(lecterTestCase("checkEnd_If"))

##     # auto-assignment operators ( += , -=, *=, /= )
##     suite.addTest(lecterTestCase("checkAddAss"))
##     suite.addTest(lecterTestCase("checkMulAss"))
##     suite.addTest(lecterTestCase("checkSubAss"))
##     suite.addTest(lecterTestCase("checkDivAss"))
    suite.addTest(lecterTestCase("checkBadAss")) # :)

    resultfile = open("results.txt", "w")
    #unittest.TextTestRunner(resultfile).run(suite)
    unittest.TextTestRunner().run(suite)
