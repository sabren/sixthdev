from PythonCardPrototype import model
from wxPython.wx import *

class Box:
    def __init__(self, x, y):
        """
        x and y are the center coordinates
        """
        self.x = x
        self.y = y
        self.w = 100
        self.h = 50
        self.fill = "white"
        self.line = "black"

    def contains(self, x, y):
        return ( self.left() <= x <= self.right() ) \
           and ( self.top() <= y <= self.bottom() )

    def draw(self, canvas):
        canvas.setFillColor(self.fill)
        canvas.DrawRectangle(self.left(), self.top(), self.w, self.h)
        
    def erase(self, canvas):
        canvas._setForegroundColor("white")
        self.draw(canvas)
        canvas._setForegroundColor("black")

    def left(self):
        return self.x - self.w/2
    def right(self):
        return self.x + self.w/2
    def top(self):
        return self.y - self.h/2
    def bottom(self):
        return self.y + self.h/2

    def bounds(self):
        l = self.left()
        r = self.right()
        t = self.top()
        b = self.bottom()
        return [(l,t), (r,t), (l,b), (r,b)]
                 

class BoxSpring(model.Background):

    def on_openBackground(self, event):
        # this seems to be the place to initalize things.
        self.boxes = []
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
        for i in range(len(self.boxes),0,-1):
            b = self.boxes[i-1]
            if b.contains(event.x, event.y):
                self.focus = b
                self.gripx = b.x - event.x
                self.gripy = b.y - event.y
                break

    def on_canvas_mouseUp(self, event):
        # move to top and release:
        if self.focus:
            self.boxes.remove(self.focus)
            self.boxes.append(self.focus)
            self.focus.draw(self.canvas)
            self.focus = None

    def on_canvas_mouseDrag(self, event):
        if self.focus:
            self.canvas.autoRefresh = 0
            self.focus.erase(self.canvas)
            self.redraw(self.focus.bounds())
            self.focus.x = event.x + self.gripx
            self.focus.y = event.y + self.gripy
            self.canvas.autoRefresh = 1
            self.focus.draw(self.canvas)
                    
    def on_canvas_mouseDoubleClick(self, event):
        b = Box(event.x, event.y)
        self.boxes.append(b)
        b.draw(self.canvas)
        self.focus = b
        self.gripx = 0
        self.gripy = 0

    def redraw(self, rectangle):
        bounds = rectangle
        for b in self.boxes:
            if b is self.focus:
                continue
            else:
                for x,y in rectangle:
                    if b.contains(x,y):
                        b.draw(self.canvas)
                        bounds.extend(b.bounds())
                        break

if __name__ == '__main__':
    app = model.PythonCardApp(BoxSpring)
    app.MainLoop()
