import unittest
from gameworld import Avatar, Map, Blocked

class AvatarTest(unittest.TestCase):

    def test_move(self):
        m = Map()
        a = Avatar(m, (5,5))
        assert m.locate(a) == (5,5)
        a.move(m.NORTH)
        assert m.locate(a) == (5,4)

    def test_move_collision(self):
        m = Map()
        m.place(object(), (5,4))
        a = Avatar(m, (5,5))
        self.assertRaises(Blocked, a.move, m.NORTH)

    def test_face(self):
        m = Map()
        a1 = Avatar(m, (5,5))
        assert a1.facing == m.SOUTH
        a2 = Avatar(m, (5,5), m.NORTH)
        assert a2.facing == m.NORTH
        a1.face(m.WEST)
        assert a1.facing == m.WEST
        

if __name__=="__main__":
    unittest.main()
    
