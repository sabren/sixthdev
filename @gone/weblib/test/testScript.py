"""
testScript.py - unit tests for weblib.script

$Id$
"""
import unittest
import weblib

class ScriptTestCase(unittest.TestCase):

    def check_cgi(self):
        import os, string
        actual = os.popen('python -c"import weblib.script; print \'hello\'"').readlines()

        # scond line should be the set-cookie. ignore it!
        actual = string.join([actual[0]] + actual[2:], '')
        
        target = weblib.trim(
            """
            Content-type: text/html
            
            hello
            """)

        assert actual==target, "didn't get headers in CGI-mode!"

            
