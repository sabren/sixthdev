"""
test zebra's lexer

$Id$
"""
import unittest
import zebra

class LexerTestCase(unittest.TestCase):

    def check_simpleLex(self):
        goal = [("NAME", "x")]
        actual = zebra.lexer.lex("x")
        assert actual == goal, \
               "didn't parse single var correctly:\n%s" % str(actual)
        

    def check_lambda(self):
        "we don't want to allow lambdas!"

        try:
            print zebra.lexer.parse("lambda x: 4+x")
        except SyntaxError:
            gotError = 1
        else:
            gotError = 0

        assert gotError, \
               "lambdas should raise an error!"

        
