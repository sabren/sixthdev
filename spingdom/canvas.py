# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------------
# Name:         canvas.py
# Purpose:      The canvas class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# RCS-ID:       $Id$
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
#----------------------------------------------------------------------------

import wx
from lines import LineShape
from composit import *

NoDragging = 0
StartDraggingLeft = 1
ContinueDraggingLeft = 2
StartDraggingRight = 3
ContinueDraggingRight = 4

KEY_SHIFT, KEY_CTRL = 1, 2

DEFAULT_MOUSE_TOLERANCE = 3


# Helper function: True if 'contains' wholly contains 'contained'.
def WhollyContains(contains, contained):
    xp1, yp1 = contains.x, contains.y
    xp2, yp2 = contained.x, contained.y
    
    w1, h1 = contains.GetBoundingBoxMax()
    w2, h2 = contained.GetBoundingBoxMax()
    
    left1 = xp1 - w1 / 2.0
    top1 = yp1 - h1 / 2.0
    right1 = xp1 + w1 / 2.0
    bottom1 = yp1 + h1 / 2.0
    
    left2 = xp2 - w2 / 2.0
    top2 = yp2 - h2 / 2.0
    right2 = xp2 + w2 / 2.0
    bottom2 = yp2 + h2 / 2.0
    
    return ((left1 <= left2)
            and (top1 <= top2)
            and (right1 >= right2)
            and (bottom1 >= bottom2))


class ShapeCanvas(wx.ScrolledWindow):

    """
    This is not so much a canvas for drawing as
    the top-level component or contral that
    responds to user interaction and other
    events from wx.

    .mouseTolerance sets the tolerance within which
    a mouse move is ignored. The default is 3 pixels.


    with .avoidRefreshes=True, refreshes are minimized,
    but the diagram may need manual refreshing occasionally.
    """
    
    def __init__(self, parent = None, id = -1,
                 pos = wx.DefaultPosition, size = wx.DefaultSize,
                 style = wx.BORDER, name = "ShapeCanvas"):
        
        wx.ScrolledWindow.__init__(self, parent, id, pos, size, style, name)
        
        self.diagram = None
        self._dragState = NoDragging
        self._draggedShape = None
        self._oldDragX = 0
        self._oldDragY = 0
        self._firstDragX = 0
        self._firstDragY = 0
        self._checkTolerance = True # this MAY actually be private...
        self.mouseTolerance = DEFAULT_MOUSE_TOLERANCE
        self.avoidRefreshes = False
        self.snapToGrid = False
        self.gridSpacing = 25.0

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_MOUSE_EVENTS(self, self.OnMouseEvent)
   
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        
        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.SOLID))
        dc.Clear()

        if self.diagram:
            self.diagram.draw(dc)

    def OnMouseEvent(self, evt):
        dc = wx.ClientDC(self)
        self.PrepareDC(dc)
        
        x, y = evt.GetLogicalPosition(dc)

        keys = 0
        if evt.ShiftDown():
            keys |= KEY_SHIFT
        if evt.ControlDown():
            keys |= KEY_CTRL

        dragging = evt.Dragging()

        # Check if we're within the tolerance for mouse movements.
        # If we're very close to the position we started dragging
        # from, this may not be an intentional drag at all.
        if dragging:
            if self._checkTolerance:
                # the difference between two logical coordinates
                # is a logical coordinate
                dx = abs(x - self._firstDragX) 
                dy = abs(y - self._firstDragY)
                toler = self.mouseTolerance
                if (dx <= toler) and (dy <= toler):
                    return
            # If we've ignored the tolerance once, then ALWAYS ignore
            # tolerance in this drag, even if we come back within
            # the tolerance range.
            self._checkTolerance = False

        # Dragging - note that the effect of dragging is left entirely up
        # to the object, so no movement is done unless explicitly done by
        # object.
        if dragging and self._draggedShape and self._dragState == StartDraggingLeft:
            self._dragState = ContinueDraggingLeft

            # If the object isn't m_draggable, transfer message to canvas
            if self._draggedShape.Draggable():
                self._draggedShape.handler.OnBeginDragLeft(x, y, keys, self._draggedAttachment)
            else:
                self._draggedShape = None
                self.OnBeginDragLeft(x, y, keys)

            self._oldDragX, self._oldDragY = x, y

        elif dragging and self._draggedShape and self._dragState == ContinueDraggingLeft:
            # Continue dragging
            self._draggedShape.handler.OnDragLeft(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.handler.OnDragLeft(True, x, y, keys, self._draggedAttachment)
            self._oldDragX, self._oldDragY = x, y

        elif evt.LeftUp() and self._draggedShape and self._dragState == ContinueDraggingLeft:
            self._dragState = NoDragging
            self._checkTolerance = True

            self._draggedShape.handler.OnDragLeft(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.handler.OnEndDragLeft(x, y, keys, self._draggedAttachment)
            self._draggedShape = None

        elif dragging and self._draggedShape and self._dragState == StartDraggingRight:
            self._dragState = ContinueDraggingRight
            if self._draggedShape.Draggable:
                self._draggedShape.handler.OnBeginDragRight(x, y, keys, self._draggedAttachment)
            else:
                self._draggedShape = None
                self.OnBeginDragRight(x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif dragging and self._draggedShape and self._dragState == ContinueDraggingRight:
            # Continue dragging
            self._draggedShape.handler.OnDragRight(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.handler.OnDragRight(True, x, y, keys, self._draggedAttachment)
            self._oldDragX, self._oldDragY = x, y

        elif evt.RightUp() and self._draggedShape and self._dragState == ContinueDraggingRight:
            self._dragState = NoDragging
            self._checkTolerance = True

            self._draggedShape.handler.OnDragRight(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.handler.OnEndDragRight(x, y, keys, self._draggedAttachment)
            self._draggedShape = None

        # All following events sent to canvas, not object
        elif dragging and not self._draggedShape and self._dragState == StartDraggingLeft:
            self._dragState = ContinueDraggingLeft
            self.OnBeginDragLeft(x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif dragging and not self._draggedShape and self._dragState == ContinueDraggingLeft:
            # Continue dragging
            self.OnDragLeft(False, self._oldDragX, self._oldDragY, keys)
            self.OnDragLeft(True, x, y, keys)
            self._oldDragX, self._oldDragY = x, y                

        elif evt.LeftUp() and not self._draggedShape and self._dragState == ContinueDraggingLeft:
            self._dragState = NoDragging
            self._checkTolerance = True

            self.OnDragLeft(False, self._oldDragX, self._oldDragY, keys)
            self.OnEndDragLeft(x, y, keys)
            self._draggedShape = None

        elif dragging and not self._draggedShape and self._dragState == StartDraggingRight:
            self._dragState = ContinueDraggingRight
            self.OnBeginDragRight(x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif dragging and not self._draggedShape and self._dragState == ContinueDraggingRight:
            # Continue dragging
            self.OnDragRight(False, self._oldDragX, self._oldDragY, keys)
            self.OnDragRight(True, x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif evt.RightUp() and not self._draggedShape and self._dragState == ContinueDraggingRight:
            self._dragState = NoDragging
            self._checkTolerance = True

            self.OnDragRight(False, self._oldDragX, self._oldDragY, keys)
            self.OnEndDragRight(x, y, keys)
            self._draggedShape = None

        # Non-dragging events
        elif evt.IsButton():
            self._checkTolerance = True

            # Find the nearest object
            attachment = 0

            nearest_object, attachment = self.FindShape(x, y)
            if nearest_object: # Object event
                if evt.LeftDown():
                    self._draggedShape = nearest_object
                    self._draggedAttachment = attachment
                    self._dragState = StartDraggingLeft
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.LeftUp():
                    # N.B. Only register a click if the same object was
                    # identified for down *and* up.
                    if nearest_object == self._draggedShape:
                        nearest_object.handler.OnLeftClick(x, y, keys, attachment)
                    self._draggedShape = None
                    self._dragState = NoDragging

                elif evt.LeftDClick():
                    nearest_object.handler.OnLeftDoubleClick(x, y, keys, attachment)
                    self._draggedShape = None
                    self._dragState = NoDragging

                elif evt.RightDown():
                    self._draggedShape = nearest_object
                    self._draggedAttachment = attachment
                    self._dragState = StartDraggingRight
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.RightUp():
                    if nearest_object == self._draggedShape:
                        nearest_object.handler.OnRightClick(x, y, keys, attachment)
                    self._draggedShape = None
                    self._dragState = NoDragging

            else: # Canvas event
                if evt.LeftDown():
                    self._draggedShape = None
                    self._dragState = StartDraggingLeft
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.LeftUp():
                    self.OnLeftClick(x, y, keys)
                    self._draggedShape = None
                    self._dragState = NoDragging

                elif evt.RightDown():
                    self._draggedShape = None
                    self._dragState = StartDraggingRight
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.RightUp():
                    self.OnRightClick(x, y, keys)
                    self._draggedShape = None
                    self._dragState = NoDragging

    def FindShape(self, x, y, info = None, notObject = None):
        nearest = 100000.0
        nearest_attachment = 0
        nearest_object = None

        # Go backward through the object list, since we want:
        # (a) to have the control points drawn LAST to overlay
        #     the other objects
        # (b) to find the control points FIRST if they exist

        rl = self.diagram.children[:]
        rl.reverse()
        for object in rl:
            # First pass for lines, which might be inside a container, so we
            # want lines to take priority over containers. This first loop
            # could fail if we clickout side a line, so then we'll
            # try other shapes.
            if object.IsShown() and \
               isinstance(object, LineShape) and \
               object.HitTest(x, y) and \
               ((info == None) or isinstance(object, info)) and \
               (not notObject or not notObject.HasDescendant(object)):
                temp_attachment, dist = object.HitTest(x, y)
                # A line is trickier to spot than a normal object.
                # For a line, since it's the diagonal of the box
                # we use for the hit test, we may have several
                # lines in the box and therefore we need to be able
                # to specify the nearest point to the centre of the line
                # as our hit criterion, to give the user some room for
                # manouevre.
                if dist < nearest:
                    nearest = dist
                    nearest_object = object
                    nearest_attachment = temp_attachment

        for object in rl:
            # On second pass, only ever consider non-composites or
            # divisions. If children want to pass up control to
            # the composite, that's up to them.
            if (object.IsShown() and 
                   (isinstance(object, DivisionShape) or 
                    not isinstance(object, CompositeShape)) and 
                    object.HitTest(x, y) and 
                    (info == None or isinstance(object, info)) and 
                    (not notObject or not notObject.HasDescendant(object))):
                temp_attachment, dist = object.HitTest(x, y)
                if not isinstance(object, LineShape):
                    # If we've hit a container, and we have already
                    # found a line in the first pass, then ignore
                    # the container in case the line is in the container.
                    # Check for division in case line straddles divisions
                    # (i.e. is not wholly contained).
                    if not nearest_object or not (isinstance(object, DivisionShape) or WhollyContains(object, nearest_object)):
                        nearest_object = object
                        nearest_attachment = temp_attachment
                        break

        return nearest_object, nearest_attachment

    def AddShape(self, object, addAfter = None):
        object.canvas = self
        self.diagram.AddShape(object, addAfter)
        # @TODO: remove Shape.canvas!!
        # @TODO: remove canvas.AddShape!! 
        # There is NO reason for diagrams or
        # shapes to have a reference to canvas.
        # (And anyway the canvas is more like
        # the control)
        
    def InsertShape(self, object):
        self.diagram.InsertShape(object)

    def RemoveShape(self, object):
        self.diagram.RemoveShape(object)

    def quickRedraw(self, dc):
        if self.avoidRefreshes:
            pass
        else:
            self.Redraw(dc)

    def Redraw(self, dc):
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.diagram.draw(dc)
        self.SetCursor(wx.STANDARD_CURSOR)

    def Snap(self, x, y):
        """
        Snaps the coordinate to the nearest grid position,
        if .snapToGrid is on.
        """
        if self.snapToGrid:
            return (self.gridSpacing * int(x / self.gridSpacing + 0.5),
                    self.gridSpacing * int(y / self.gridSpacing + 0.5))
        return x, y


    def OnLeftClick(self, x, y, keys = 0):
        pass

    def OnRightClick(self, x, y, keys = 0):
        pass

    def OnDragLeft(self, draw, x, y, keys = 0):
        pass

    def OnBeginDragLeft(self, x, y, keys = 0):
        pass

    def OnEndDragLeft(self, x, y, keys = 0):
        pass

    def OnDragRight(self, draw, x, y, keys = 0):
        pass

    def OnBeginDragRight(self, x, y, keys = 0):
        pass

    def OnEndDragRight(self, x, y, keys = 0):
        pass
