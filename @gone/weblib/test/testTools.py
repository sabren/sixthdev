"""
unit tests for weblib tools
"""
import unittest
import weblib

class ToolsTestCase(unittest.TestCase):

    def check_urlDecode(self):
        """
        check that + signs work right:
        """

        assert weblib.urlDecode("+") == " ", \
               "urlDecode screws up on + signs"
        assert weblib.urlDecode("%2b") == "+", \
               "urlDecode screws up on %2b"

    def check_html(self):
        #@TODO: make this its own test suite!
        import weblib.html

        # this shouldn't crash on empty options list:
        weblib.html.select("box", [])
    
