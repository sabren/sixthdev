#!/usr/bin/python
from PythonCardPrototype import model, dialog
from boxspring import Drawing, Box
from wxPython.wx import *
import pickle

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
        
    
        
class Arrow:
    def __init__(self, start):
        self.start = start
        self.end = start

    def erase(self, canvase):
        pass

    def draw(self):
        canvas._setForegroundColor("silver")
        canvas.DrawLine(self.start.x, self.start.y, self.end.x, self.end.y)        

    def bounds(self):
        l = min(self.start.x, self.end.x)
        r = max(self.start.x, self.end.x)
        t = min(self.start.y, self.end.y)
        b = min(self.start.x, self.end.y)
        return [(l,t), (r,t), (l,b), (r,b)]

    def point(self, canvas, x,y):
        self.end.x = x
        self.end.y = y


class BoxSpring(model.Background):

    def newDrawing(self):
        self.drawing = Drawing()
        self.focus = None
        self.filename = None

    def openDrawing(self, filename):
        self.newDrawing()
        file = open(filename)
        self.drawing = pickle.load(file)
        file.close()
        self.filename = filename

    def saveDrawing(self, filename):
        self.filename = filename
        file = open(filename, "w")
        pickle.dump(self.drawing, file)
        file.close()

    def on_openBackground(self, event):
        # this seems to be the place to initalize things.
        self.newDrawing()
        self.canvas = self.components.canvas
        
        self.gripx = 0  # grip is how far the cursor is from the center
        self.gripy = 0  # of whatever box we're holding.

    def on_menuFileExit_select(self, event):
        self.Close()

    def defaultPath(self):
        return "w:/"

    def on_menuFileOpen_select(self, event):
        result = dialog.openFileDialog(self, 'Open',
                                       self.defaultPath(), '', '*.box' )
        if result['accepted']:
            path = result['paths'][0]            
            self.openDrawing(path)
            self.refresh()

    def on_menuFileSaveAs_select(self, event):
        result = dialog.saveFileDialog(self, 'Save As',
                                       self.defaultPath(), '', '*.box' )
        if result['accepted']:
            path = result['paths'][0]            
            self.saveDrawing(path)

    def on_menuFileSave_select(self, event):
        if self.filename:
            self.saveDrawing(self.filename)
        else:
            self.on_menuFileSaveAs_select(event)

    def on_canvas_mouseDown(self, event):
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

    def on_canvas_mouseMove(self, event):
        if isinstance(self.focus, Arrow):
            self.focus.point(self.canvas, event.x, event.y)
                    
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

    def refresh(self):
        self.canvas.Clear()
        for g in self.drawing.glyphs:
            g.draw(self.canvas)
        
    def redraw(self, rectangle):
        bounds = rectangle
        for g in self.drawing.glyphs:
            if g is self.focus:
                continue
            else:
                for x,y in rectangle:
                    if g.contains(x,y):
                        g.draw(self.canvas)
                        bounds.extend(g.getBounds())
                        break

if __name__ == '__main__':
    app = model.PythonCardApp(BoxSpring)
    app.MainLoop()
