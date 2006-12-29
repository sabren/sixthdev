# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------------
# Name:         diagram.py
# Purpose:      Diagram class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# RCS-ID:       $Id$
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
#----------------------------------------------------------------------------

class Diagram(object):
    """
    Encapsulates an entire diagram, with methods for drawing.

    Derived from:
      Object
    """
    def __init__(self):
        self.children = []

    def draw(self, dc):
        """
        Draw the shapes in the diagram on the specified device context.
        """
        for object in self.children:
            object.Draw(dc)

    def AddShape(self, object, addAfter = None):
        """
        Adds a shape to the diagram. If addAfter is not None, the shape
        will be added after addAfter.

        NOTE: you must assign shape.canvas first, because .canvas
        is tightly coupled to... well everything. It was originally
        added here, but I wanted to get rid of Diagram.canvas.
        """
        assert object.canvas, \
               "for now, assign .canvas before adding shape to diagram"
        
        if not object in self.children:
            if addAfter:
                self.children.insert(self.children.index(addAfter) + 1, object)
            else:
                self.children.append(object)

    def InsertShape(self, object):
        """
        Insert a shape at the front of the shape list.
        """
        self.children.insert(0, object)

    def RemoveShape(self, object):
        """
        Remove the shape from the diagram (non-recursively)
        but do not delete it.
        """
        if object in self.children:
            self.children.remove(object)
            
    def RemoveAllShapes(self):
        """
        Remove all shapes from the diagram but do not delete the shapes.
        """
        self.children = []

    def DeleteAllShapes(self):
        """
        Remove and delete all shapes in the diagram.
        """
        for shape in self.children[:]:
            if not shape.GetParent():
                self.RemoveShape(shape)
                shape.Delete()
                
    def ShowAll(self, show):
        """
        Call Show for each shape in the diagram.
        """
        for shape in self.children:
            shape.Show(show)

    def RecentreAll(self, dc):
        """
        Make sure all text that should be centred, is centred.
        """
        for shape in self.children:
            shape.Recentre(dc)
   
    def FindShape(self, id):
        """
        Return the shape for the given identifier.
        """
        for shape in self.children:
            if shape.id == id:
                return shape
        return None

