#
# testzebra.py
#
import unittest
import string
import zebra
from zebra import trim, indent, showdiff
from PHPGenerator import PHPGenerator
from PyGenerator import PyGenerator

#######################################
class ZebraTestCase(unittest.TestCase):
    def setUp(self):
        self.zEngine = zebra.Engine(PyGenerator())

    ## actual test cases ####################

    def check_Trim(self):
        """Check to make sure our internal trim() function works"""
        assert trim(
            """
            one
            two
               three
            """) == "one\ntwo\n   three\n"


    def check_Indent(self):
        output = indent("one\ntwo\n  three", 1)
        goal = "    one\n    two\n      three"
        assert output==goal, showdiff(output, goal)
    

    def check_PHP_Simple(self):
        self.zEngine = zebra.Engine(PHPGenerator())
        
        """Check Simple PHP3 output."""
        
        output = self.zEngine.compile(trim(
            """
            * zebra
            hello, world!
            """))
                                      
        goal = trim(
            """
            <?
            print "hello, world!";
            ?>
            """)

        assert output == goal, showdiff(output, goal)

    def check_PySimple(self):
        """Check simple Python output"""
        
        python = self.zEngine.compile(trim(
            """
            * zebra
            hello,
            ** show
             world!
            """))
        
        exec(python)
        output = fetch()
        
        goal = "hello, world!"

        assert output == goal, showdiff(output, goal)


    def check_PyInterpolate(self):
        """Make sure interpolation works right"""
        
        python = self.zEngine.compile(trim(
            r"""
            * zebra
            ** stripe name="EMPTY"
            ** show
            \{this} should show up in the report.
            \\\{so should this}
            but this should just be a slash: \\{!EMPTY}
            """))

        exec(python)
        output = fetch()

        goal = trim(
            r"""
            {this} should show up in the report.
            \{so should this}
            but this should just be a slash: """ + '\\')
        
        assert output==goal, showdiff(output, goal)


    def check_PyReport(self):
        """check to make sure reports work"""

        python = self.zEngine.compile(trim(
            """
            * zebra
            ** source name="database" class="csvdb"
            .
            ** query name="myquery" source="database"
            test/testcsv.csv
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
        
        # now compile it and run the report
        exec(python)
        output = fetch()

        goal = trim(
            """
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

    def check_ParseQueryAndSource(self):
        dict = self.zEngine.parse(trim(
            """
            * zebra
            ** source name="database" class="csv"
            .
            ** query name="myquery" source="database"
            test/testcsv.csv
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
        assert dict['queries']['myquery']['query'] == ['test/testcsv.csv'], \
               "<query> doesn't store the actual query!"


    def check_exec(self):
        import zebra
        zebra._some_variable = 0
        namespace = {}
        exec(self.zEngine.compile(trim(
            """
            * zebra
            ** exec
            import zebra
            zebra._some_variable = 1
            """)), namespace)
        exec ("show()", namespace)

        assert zebra._some_variable == 1, \
               "Didn't exec correctly!"

        del zebra._some_variable
               
        
    def tearDown(self):
        del self.zEngine

################################################

from testParser import *

suites = {
    "zebra": unittest.makeSuite(ZebraTestCase, "check_"),
    "parser": unittest.makeSuite(ParserTestCase, "check_"),
    }


if __name__=="__main__":
    result = unittest.TextTestRunner().run(suite)
