"""
unit tests for weblib tools
"""
import unittest
import handy
import html
import os
import zebra

class ToolsTestCase(unittest.TestCase):

    def check_urlDecode(self):
        """
        check that + signs work right:
        """
        assert handy.urlDecode("+") == " ", \
               "urlDecode screws up on + signs"
        assert handy.urlDecode("%2b") == "+", \
               "urlDecode screws up on %2b"

    def check_html(self):
        #@TODO: make this its own test suite!
        # this shouldn't crash on empty options list:
        html.select("box", [])



    def setUp(self):
        file = open("test/junk.zb","w")
        print >> file, "* for each:"
        print >> file, "    {:a:}"        
        file.close()

        file = open("test/xmljunk.zbx", "w")
        print >> file, zebra.trim(
            '''
            <?xml version="1.0"?>
            <zebra>
            <for series="each">
            <xpr>a</xpr><nl/>
            </for>
            </zebra>
            ''')
        file.close()
        
    def check_fetch(self):
        a = {"a":"x"}
        assert zebra.fetch("test/junk", {"each":[a]}) == "x\n"
        assert zebra.fetch("test/junk.zb", {"each":[a]}) == "x\n"
        assert zebra.fetch("test/xmljunk.zbx", {"each":[a]}) == "x\n"        


    def tearDown(self):
        os.unlink("test/junk.zb")
        os.unlink("test/xmljunk.zbx")
        
