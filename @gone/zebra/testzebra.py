#
# testzebra.py
#
import unittest
import zebra
import string
from PHPGenerator import PHPGenerator
from PyGenerator import PyGenerator
from ziketools import *

#######################################
class zebraTestCase(unittest.TestCase):
    def setUp(self):
        self.zEngine = zebra.Engine(PyGenerator())

    ## actual test cases ####################

    def checkTrim(self):
        """Check to make sure our internal trim() function works"""
        assert trim("""
        one
        two
           three
        """) == "one\ntwo\n   three\n"


    def checkIndent(self):
        output = indent("one\ntwo\n  three", 1)
        goal = "    one\n    two\n      three"
        assert output==goal, showdiff(output, goal)
    
    def checkPHP_Simple(self):
        self.zEngine = zebra.Engine(PHPGenerator())
        
        """Check Simple PHP3 output."""
        
        output = self.zEngine.compile(trim("""
        * zebra
        hello, world!
        """))
                                      
        goal = trim("""
        <?
        print "hello, world!";
        ?>
        """)

        assert output == goal, showdiff(output, goal)

    def checkPySimple(self):
        """Check simple Python output"""
        python = self.zEngine.compile(trim("""
        * zebra
        hello,
        ** show
         world!
        """))
        
        exec(python)
        output = fetch()
        
        goal = "hello, world!"

        assert output == goal, showdiff(output, goal)


    def checkPyInterpolate(self):
        """Make sure interpolation works right"""
        
        python = self.zEngine.compile(trim(r"""
        * zebra
        ** stripe name="EMPTY"
        ** show
        \{this} should show up in the report.
        \\\{so should this}
        but this should just be a slash: \\{!EMPTY}
        """))

        exec(python)
        output = fetch()

        goal = trim(r"""
        {this} should show up in the report.
        \{so should this}
        but this should just be a slash: """ + '\\')

        assert output==goal, showdiff(output, goal)


    def checkPyReport(self):
        """check to make sure reports work"""
        python = self.zEngine.compile(trim("""
        * zebra
        ** source name="database" class="csvdb"
        .
        ** query name="myquery" source="database"
        testcsv.csv
        ** show
        Here is the report:
        
        ** report query="myquery"
        *** head
        HEADER!
        -------
        
        *** group field="guy"
        **** head
        {guy} loves {girl}
        
        **** body
        ***** if test="{lyric}"
            a little bit of {girl} {lyric}
            
        **** foot
        ... and {girl} loves {guy}
        
        *** foot
        -------
        FOOTER!
        
        """))

        dump = open("actual.py","w")
        dump.write(python)
        dump.close

        # now compile it and run the report
        exec(python)
        output = fetch()

        goal = trim("""
        Here is the report:
        HEADER!
        -------
        fred loves wilma
        ... and wilma loves fred
        homer loves marge
        ... and marge loves homer
        lou loves everyone
            a little bit of monica in my life
            a little bit of erica by my side
            a little bit of rita is all i need
            a little bit of tina is what i see
            a little bit of sandra in the sun
            a little bit of mary all night long
            a little bit of jessica here i am
            a little bit of you makes me your man
        ... and everyone loves lou
        -------
        FOOTER!
        """)

        assert output==goal, showdiff(output, goal)

    def checkParseQueryAndSource(self):
        dict = self.zEngine.parse(trim("""
        * zebra
        ** source name="database" class="csv"
        .
        ** query name="myquery" source="database"
        testcsv.csv
        """))

        # all this stuff must be true:
        assert dict.has_key("sources"), "No ['sources']!!"
        assert dict['sources'].has_key('database'), \
               "<source> doesn't get stored in sources dict"
        assert dict['sources']['database']['class'] == 'csv', \
               "<source> doesn't remember class attribute"
        assert dict['sources']['database']['connector'] == ['.'], \
               "<source> doesn't remember connector attribute"

        # and if queries work, all this must be true:
        assert dict.has_key("queries"), "No ['queries']!!"
        assert dict['queries'].has_key('myquery'), \
               "<query> doesn't get stored in the ['queries']!"
        assert dict['queries']['myquery']['source'] == 'database', \
               "<query> doesn't store the source!"
        assert dict['queries']['myquery']['query'] == ['testcsv.csv'], \
               "<query> doesn't store the actual query!"
        
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
