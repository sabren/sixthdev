#
# testzebra.py
#

import unittest
import zebra
import string

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

class zebraTestCase(unittest.TestCase):
    def setUp(self):
        self.zEngine = zebra.Engine()
        pass

    ## actual test cases ####################

    def checkTrim(self):
        """Check to make sure our internal trim() function works"""
        assert trim("""
        one
        two
           three
        """) == "one\ntwo\n   three\n"

    
    def checkSimplePHP3(self):
        """Check Simple PHP3 output."""
        
        output = self.zEngine.compile(trim("""
        * zebra
        hello, world!
        """))
                                      
        goal = trim("""
        <?
        print "hello, world!\\n";
        ?>
        """)

        assert output == goal
    
    def tearDown(self):
        del self.zEngine

################################################

def run():
    suite = unittest.TestSuite()
    for t in dir(zebraTestCase):
        if t[:5] == "check":
            suite.addTest(zebraTestCase(t))

    result = unittest.TextTestRunner().run(suite)
    
if __name__=="__main__":
    run()
