"""
testActor.py - unit tests for Actor.py

$Id$
"""
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

        weblib.request = {"GOAL":"GOAL"}
        actor = weblib.Actor()
        assert actor.input == {"GOAL":"GOAL"}, \
               "Wrong default input when weblib.request IS defined:\n%s" \
               % actor.input
        del weblib.request

        actor = weblib.Actor()
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
        
        hamlet = Shakespearean()
        hamlet.question = None
        hamlet.act()

        assert hamlet.question == "?", \
               "act() doesn't default to calling act_(). :("
        
    def check_inEngine(self):
        "I thought this was having problems in other tests. it wasn't."

        req = weblib.Request(form={"E":"X"})
        eng = weblib.Engine(request=req, script=weblib.trim(
            """
            import weblib
            a = weblib.Actor()
            assert a.input["E"] == "X", 'form failed'
            """))

        eng.run()
        assert eng.result == eng.SUCCESS, \
               "Doesn't use correct request when in an Engine:\n %s" \
               % eng.error
        
