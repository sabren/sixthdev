#!/usr/bin/python
from PythonCardPrototype import model
from wxPython.wx import *
from boxspring import Drawing, Box

class MyBox(Box):
    def __init__(self, x, y):
        """
        x and y are the center coordinates
        """
        super(MyBox, self).__init__(x-50, y-25, 100, 50)

    def draw(self, canvas):
        canvas.setFillColor(self.fillColor)
        canvas.DrawRectangle(self.x, self.y, self.w, self.h)
        
    def toggle(self):
        if self.fillColor == "white":
            self.fillColor = "red"
        else:
            self.fillColor = "white"
        
    
        

class BoxSpring(model.Background):

    def on_openBackground(self, event):
        # this seems to be the place to initalize things.
        self.drawing = Drawing()
        self.focus = None
        self.canvas = self.components.canvas
        
        self.gripx = 0  # grip is how far the cursor is from the center
        self.gripy = 0  # of whatever box we're holding.

    def on_menuFileExit_select(self, event):
        self.Close()

    def on_canvas_mouseDown(self, event):
        """
        Look through the boxes in reverse 
        so we can pick up the topmost one.
        """
        g = self.drawing.glyphAt(event.x, event.y)
        if g:
            self.focus = g
            self.gripx = g.x - event.x
            self.gripy = g.y - event.y

    def on_canvas_mouseUp(self, event):
        # move to top and release:
        if self.focus:
            self.drawing.moveToTop(self.focus)
            self.focus.draw(self.canvas)
            self.focus = None

    def on_canvas_mouseDrag(self, event):
        if self.focus:
            self.canvas.autoRefresh = 0
            self.erase(self.focus.x, self.focus.y,
                       self.focus.w, self.focus.h)
            self.redraw(self.focus.getBounds())
            self.focus.x = event.x + self.gripx
            self.focus.y = event.y + self.gripy
            self.canvas.autoRefresh = 1
            self.focus.draw(self.canvas)
                    
    def on_canvas_mouseDoubleClick(self, event):
        if self.focus: return
        g = self.drawing.glyphAt(event.x, event.y)
        if g:
            g.toggle()
            g.draw(self.canvas)
        else:
            b = MyBox(event.x, event.y)
            self.drawing.addGlyph(b)
            b.draw(self.canvas)
            self.focus = b
            self.gripx = 0
            self.gripy = 0
        
        
    def erase(self, x, y, w, h):
        self.canvas._setForegroundColor("white")
        self.canvas.setFillColor("white")
        self.canvas.drawRectangle(x,y,w,h)
        self.canvas._setForegroundColor("black")
        
    def redraw(self, rectangle):
        bounds = rectangle
        for b in self.drawing.glyphs:
            if b is self.focus:
                continue
            else:
                for x,y in rectangle:
                    if b.contains(x,y):
                        b.draw(self.canvas)
                        bounds.extend(b.getBounds())
                        break

if __name__ == '__main__':
    app = model.PythonCardApp(BoxSpring)
    app.MainLoop()
