import unittest
from gameworld import Game, Map, Actor, Avatar

class ActorTest(unittest.TestCase):

    def test_cue(self):
        g = Game()
        a = Actor("senw")
        g.place(a, (5,5))

        # it should go in a little circle:
        a.cue(); assert g.locate(a) == (5,6)
        a.cue(); assert g.locate(a) == (6,6)
        a.cue(); assert g.locate(a) == (6,5)
        a.cue(); assert g.locate(a) == (5,5)

        # and then it should repeat:
        a.cue(); assert g.locate(a) == (5,6)

        
if __name__=="__main__":
    unittest.main()
