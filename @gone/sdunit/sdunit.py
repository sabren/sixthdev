"""
sdunit - xUnit for sixthday
"""
__ver__="$Id$"

import sys
import unittest

## custom pyunit classes #########################

class ZikeTestResult(unittest._TextTestResult):
    def printHeader(self):
        if self.errors:
            print

class ZikeTestRunner(unittest.TextTestRunner):
    def __init__(self):
        unittest.TextTestRunner.__init__(self, sys.stdout)

    def run(self, test):
        result = ZikeTestResult(self.stream)
        test(result)
        result.printResult()
        return result

## helper functions  #############################

def testModuleInCurrentDirectory():
    # checks current dir first, since "test" is a standard module
    sys.path = ["."] + sys.path
    import test
    return test

def wantSpecificTest():
    return len(sys.argv) > 1

def runRequestedTest():
    exec "from test.test%s import %sTestCase; TC=%sTestCase" \
         % ((sys.argv[1],) * 3)
    ZikeTestRunner().run(unittest.makeSuite(TC, "check_"))


## main ##########################################

if __name__=="__main__":

    testmodule = testModuleInCurrentDirectory()

    if wantSpecificTest():
        runRequestedTest()

    elif hasattr(testmodule, 'suite'):
        ZikeTestRunner().run(testmodule.suite)

    elif hasattr(testmodule, 'suites'):
        for suite in testmodule.suites.keys():
            print "** testing", suite + ":",
            ZikeTestRunner().run(testmodule.suites[suite])
            print
    else:
        print "no test suite found."
