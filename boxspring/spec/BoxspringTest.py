
import unittest
from boxspring import *

class BoxspringTest(unittest.TestCase):
    def test_box(self):
        assert Box(0,0,10,10).contains(5,5)
        assert not Box(0,0,10,10).contains(15,15)
        assert Box(10,10,10,10).contains(15,15)
        assert Box(10,10,10,10).contains(20,20)
        assert not Box(10,10,10,10,).contains(21,21)
        assert Box(0,0,1,1).lineColor == "black"
        assert Box(0,0,1,1).fillColor == "white"
        self.assertEquals([(0,0),(10,0),(0,10),(10,10)],
                          Box(0,0,10,10).getBounds())

    def test_drawing(self):
        d = Drawing()
        assert d.glyphCount() == 0
        d.addGlyph(Box(0,0, 10,10))
        assert d.glyphCount() == 1
        assert d.glyphAt(5,5)
        assert not d.glyphAt(20,20)
        boxA = Box(0,0,10,10)
        boxB = Box(0,0,10,10)
        d.addGlyph(boxA)
        d.addGlyph(boxB)
        assert d.glyphAt(5,5) is boxB
        d.moveToTop(boxA)
        assert d.glyphAt(5,5) is boxA
        
        
    
if __name__=="__main__":
    unittest.main()
    
    