"""
unit tests for weblib tools
"""
import unittest
import handy
import html

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
    
