import sys
sys.path = ["."] + sys.path
import test
import unittest



# import test always works, because test is part of the standard
# python distribution (but it's just a dummy module)

# .. BUT, if the current directory contains a "test" module, python
# will use that instead. If that's the case, we want to look for a
# variable called "suite" or a list called "suites"

class ZikeTestResult(unittest._TextTestResult):
    def printHeader(self):
        if self.errors: print

class ZikeTestRunner(unittest.TextTestRunner):
    def __init__(self):
        unittest.TextTestRunner.__init__(self, sys.stdout)
    def run(self, test):
        result = ZikeTestResult(self.stream)
        test(result)
        result.printResult()
        return result


import sys
if "sys" in sys.argv:
    ### ACCEPTANCE TESTS ####################
    #@TODO: unhardcode this
    import glob
    for test in glob.glob("test/sys_*.lec"):
        # print the test name:
        print "[%s]:" % test[9:-4]
        execfile(test)
elif len(sys.argv) > 1:
    exec "from test.test%s import %sTestCase; TC=%sTestCase" \
         % ((sys.argv[1],) * 3)
    ZikeTestRunner().run(unittest.makeSuite(TC, "check_"))
else:
    ### UNIT TESTS ##########################
    ## case A: single suite
    if test.__dict__.has_key('suite'):
        ZikeTestRunner().run(test.suite)

    ## case B: multiple suites
    elif test.__dict__.has_key('suites'):
        for suite in test.suites.keys():
            print "** testing", suite + ":",
            ZikeTestRunner().run(test.suites[suite])
            print

    ## case C: no suites
    else:
        print "no test suite found."


