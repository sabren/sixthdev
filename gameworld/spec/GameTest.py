
import unittest
from gameworld import Map, Game, Avatar


class GameTest(unittest.TestCase):
        
    def test_observable(self):
        g = Game()
        a = Avatar()
        
        self.events = 0
        def observer(*args): self.events += 1
        g.register(observer)

        g.spawn(a, (5,5))
        a.walk(Map.SOUTH)
        assert self.events == 2
       

if __name__=="__main__":
    unittest.main()

