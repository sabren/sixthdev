import unittest
from gameworld import Map

class MapTest(unittest.TestCase):

    def test_findAdjacent(self):
        m = Map()
        assert m.findAdjacent(m.NORTH, (5,5)) == (5,4)
        assert m.findAdjacent(m.SOUTH, (5,5)) == (5,6)
        assert m.findAdjacent(m.EAST, (5,5)) == (4,5)
        assert m.findAdjacent(m.WEST, (5,5)) == (6,5)

    def test_place(self):
        m = Map()
        m.place(object(), (3,3))
        assert m.isOccupied((3,3))
        assert not m.isOccupied((3,4))

    def test_remove(self):
        m = Map()
        o1 = object()
        m.place(o1, (3,3))
        assert m.isOccupied((3,3))
        m.remove(o1)
        assert not m.isOccupied((3,3))

    def test_locate(self):
        m = Map()
        thing = object()
        other = object()
        m.place(thing, "fresno")
        assert m.locate(thing) == "fresno"
        assert m.locate(other) is None
        
    

if __name__=="__main__":
    unittest.main()
    
