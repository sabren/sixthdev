"""
testActor.py - unit tests for Actor.py
"""
__ver__="$Id$"

import unittest
import weblib

class ActorTestCase(unittest.TestCase):

    def setUp(self):
        if hasattr(weblib, "request"):
            self._REQ = weblib.request


    def tearDown(self):
        if hasattr(self, "_REQ"):
            weblib.request = self._REQ


    def check_input(self):

        ## used to rely on weblib.request.. now should NOT
        weblib.request = {"GOAL":"GOAL"}
        actor = weblib.Actor({})
        assert actor.input == {}, \
               "Wrong default input when weblib.request IS defined:\n%s" \
               % actor.input
        del weblib.request

        actor = weblib.Actor({})
        assert actor.input == {}, \
               "Wrong default input when weblib.request IS NOT defined"

        actor = weblib.Actor({"red":"blue"})
        assert actor.input == {"red":"blue"}, \
               "Wrong .input when input is supplied"
        

    def check_act_(self):

        class Shakespearean(weblib.Actor):
            def act_(self):
                ToBe = "?"
                self.question = ToBe or (not ToBe)
        
        hamlet = Shakespearean({})
        hamlet.question = None
        hamlet.act()

        assert hamlet.question == "?", \
               "act() doesn't default to calling act_(). :("
               
    def check_write(self):
        devito = weblib.Actor({})
        goal = "what's the worst that could happen?"
        devito.write(goal)
        actual = devito.act()
        assert actual == goal, \
               "Actor.write() doesn't work. got: %s" % actual


    def check_jump(self):
        brando = weblib.Actor({})
        self.assertRaises(weblib.Redirect,
                          brando.redirect, action="somewhere")
        
