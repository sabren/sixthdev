"""
unit tests for lecter interpreter
"""
__ver__="$Id$"

import unittest, lecter
from lecter import TRUE, FALSE

class InterpreterTestCase(unittest.TestCase):

    def check_truth(self):
        i = lecter.Interpreter()
        assert i.eval("true?")==TRUE,\
               "true shold be true"
        assert i.eval("false?")==FALSE,\
               "false should be false"

    def check_assert0(self):
        i = lecter.Interpreter()
        i.eval("something.")
        assert i.eval("something?")==TRUE,\
               "asserting something/0 didn't work."
        
    def check_assert1(self):
        i = lecter.Interpreter()
        i.eval("hot(fire).")
        assert i.eval("hot(fire)?")==TRUE,\
               "asserting hot(fire) didn't work."

        actual = i.eval("hot($x)?")
        assert actual==({"$x":"fire"},), \
               "can't query about what's hot. (got %s) " % str(actual)

    def check_parse(self):
        i = lecter.Interpreter()
        actual = i.parse("pred")
        assert actual  == ("pred", ()),\
               "pred/0 didn't parse right: %s" % str(actual)
        actual = i.parse("pred(arg)")
        assert actual == ("pred", ("arg",)),\
               "pred/1 didn't parse right: %s" % str(actual)
        
        
