
class Glyph(object):
    pass

class Drawing(Glyph):
    """
    I am a Composite Glyph
    """
    def __init__(self):
        self.glyphs = []
    def glyphCount(self):
        return len(self.glyphs)
    def addGlyph(self, glyph):
        self.glyphs.append(glyph)
    def moveToTop(self, glyph):
        self.glyphs.remove(glyph)
        self.addGlyph(glyph)        
    def glyphAt(self, a, b):
        """
        Return the topmost glyph at the specified coordinates.
        """
        for i in range(len(self.glyphs), 0, -1):
            g = self.glyphs[i-1]
            if g.contains(a, b):
                return g
        return None

class Box(Glyph):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.lineColor = "black"
        self.fillColor = "white"
    def getBounds(self):
        return [(self.x, self.y), (self.x+self.w, self.y),
                (self.x, self.y+self.h), (self.x+self.w, self.y+self.h)]
    def contains(self, a, b):
        return ((self.x <= a <= (self.x + self.w))
           and  (self.y <= b <= (self.y + self.h)))
           