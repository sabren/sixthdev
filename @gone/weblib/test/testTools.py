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
               "urlDecode scews up on %2b"
