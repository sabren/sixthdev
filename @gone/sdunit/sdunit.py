"""
sdunit - xUnit for sixthday
"""
__ver__="$Id$"

import os
import sys
import unittest

## custom pyunit classes #########################

class SixthDayTestResult(unittest._TextTestResult):
    def __init__(self, stream):
        unittest._TextTestResult.__init__(self, stream, 1, 1)


class SixthDayTestRunner(unittest.TextTestRunner):
    def __init__(self):
        stream = sys.stdout
        #stream = open("logfile.txt","w")
        unittest.TextTestRunner.__init__(self, stream)

    def run(self, test):
        result = SixthDayTestResult(self.stream)
        test(result)
        result.printErrors()
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
    # old style
    exec "from test.test%s import %sTestCase; TC=%sTestCase" \
         % ((sys.argv[1],) * 3)
    SixthDayTestRunner().run(unittest.makeSuite(TC, "check_"))


def runTest(name):
    # new style (literate)
    exec "from spec.%sTest import %sTest; TC=%sTest" \
         % (name, name, name)
    print "%20s: " % name, 
    SixthDayTestRunner().run(unittest.makeSuite(TC, "check_"))
    
def runSpecificTest():
    runTest(sys.argv[1])
    

## main ##########################################

if __name__=="__main__":

    if os.path.exists("./spec"):
        print "-=" * 10 + "+"
        # new style (literate) "spec" directory
        if wantSpecificTest():
            runSpecificTest()
        else:
            [runTest(file[:-len("Test.py")])
             for file in os.listdir("spec")
             if file.endswith("Test.py")]
        print "-=" * 10 + "+"
            
    else:
        # old style "test" directory
        testmodule = testModuleInCurrentDirectory()

        if wantSpecificTest():
            runRequestedTest()

        elif hasattr(testmodule, 'suite'):
            SixthDayTestRunner().run(testmodule.suite)

        elif hasattr(testmodule, 'suites'):
            for suite in testmodule.suites.keys():
                print "** testing", suite + ": ",
                SixthDayTestRunner().run(testmodule.suites[suite])
        else:
            print "no test suite found."

