import unittest
from gameworld import Avatar, Game, Map, Wall, event

class AvatarTest(unittest.TestCase):

    def setUp(self):
        self.g = Game()
        self.a = Avatar()
        self.g.spawn(self.a, (5,5))
        
    def test_walk(self):
        assert self.g.locate(self.a) == (5,5)
        self.a.walk(Map.NORTH)
        assert self.g.locate(self.a) == (5,4)

    def test_walk_blocked(self):
        self.g.place(Wall(), (5,4))
        self.a.walk(Map.NORTH)
        assert self.g.locate(self.a) == (5,5)


if __name__=="__main__":
    unittest.main()
