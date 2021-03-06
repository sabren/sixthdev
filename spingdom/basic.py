# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------------
# Name:         basic.py
# Purpose:      The basic OGL shapes
#
# Author:       Pierre Hj�lm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# RCS-ID:       $Id$
# Copyright:    (c) 2004 Pierre Hj�lm - 1998 Julian Smart
# Licence:      wxWindows license
#----------------------------------------------------------------------------

import wx
import math
from oglmisc import *

DragOffsetX = 0.0
DragOffsetY = 0.0

def OGLInitialize():
    global WhiteBackgroundPen, WhiteBackgroundBrush, TransparentPen
    global BlackForegroundPen, NormalFont
    
    WhiteBackgroundPen = wx.Pen(wx.WHITE, 1, wx.SOLID)
    WhiteBackgroundBrush = wx.Brush(wx.WHITE, wx.SOLID)

    TransparentPen = wx.Pen(wx.WHITE, 1, wx.TRANSPARENT)
    BlackForegroundPen = wx.Pen(wx.BLACK, 1, wx.SOLID)

    NormalFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)


class ShapeTextLine(object):
    def __init__(self, the_x, the_y, the_line):
        self.x = the_x
        self.y = the_y
        self.text = the_line

    def SetText(self, text):
        self.text = text

    def GetText(self):
        return self.text



class NullEventHandler(object):
    """
    Null object so we don't have to keep checking
    for ShapeEvtHandler.prev

    This also gives a nice, concise view of the
    various event handlers.
    """
    def OnDraw(self, dc): pass
    def OnMoveLinks(self, dc): pass
    def OnMoveLink(self, dc, moveControlPoints = True): pass
    def OnDrawContents(self, dc): pass
    def OnDrawBranches(self, dc, erase = False): pass
    def OnSize(self, x, y): pass
    def OnMovePre(self, dc, x, y, old_x, old_y, display = True): return True
    def OnMovePost(self, dc, x, y, old_x, old_y, display = True): return True
    def OnErase(self, dc): pass
    def OnEraseContents(self, dc): pass
    def OnHighlight(self, dc): pass
    def OnLeftClick(self, x, y, keys, attachment): pass            
    def OnLeftDoubleClick(self, x, y, keys = 0, attachment = 0): pass
    def OnRightClick(self, x, y, keys = 0, attachment = 0): pass
    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0): pass
    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0): pass
    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0): pass
    def OnDragRight(self, draw, x, y, keys = 0, attachment = 0): pass
    def OnBeginDragRight(self, x, y, keys = 0, attachment = 0): pass
    def OnEndDragRight(self, x, y, keys = 0, attachment = 0): pass

    # > Control points ('handles') redirect control to the actual shape,
    # > to make it easier to override sizing behaviour.
    # ... so what? the shape can be it's own previousHandler then.
    # @TODO: Figure out why that warranted a comment. :)
    def OnSizingDragLeft(self, pt, draw, x, y, keys = 0, attachment = 0): pass
    def OnSizingBeginDragLeft(self, pt, x, y, keys = 0, attachment = 0): pass
    def OnSizingEndDragLeft(self, pt, x, y, keys = 0, attachment = 0): pass
    
    def OnDrawOutline(self, x, y, w, h): pass
    def OnDrawControlPoints(self, dc): pass
    def OnEraseControlPoints(self, dc): pass

    # Can override this to prevent or intercept line reordering.
    def OnChangeAttachment(self, attachment, line, ordering): pass

    
class ShapeEvtHandler(object):
    def __init__(self, prev = None, shape = None):
        self.prev = prev or NullEventHandler()
        self.shape = shape

    def __del__(self):
        pass

    def OnDelete(self):
        if self!=self.shape:
            del self

    def __getattr__(self, name):
        """
        This gets called if an event method has
        not been overwritten. By default, we just
        pass the event to the previous handler.
        """
        def proxy(*args, **kw):
            return getattr(self.prev, name)(*args, **kw)
        return proxy

    # these two didn't proxy to _previousHandler.
    # they just said "pass" by default. why?
    def OnBeginSize(self, w, h): pass
    def OnEndSize(self, w, h): pass

            
class Shape(ShapeEvtHandler):
    """OGL base class

    Shape(canvas = None)
    
    Shape is the top-level, abstract object that all other objects
    are derived from. All common functionality is represented by Shape's
    members, and overriden members that appear in derived classes and have
    behaviour as documented for Shape, are not documented separately.
    """
    
    GraphicsInSizeToContents = False
    
    def __init__(self, canvas = None):
        super(Shape, self).__init__()
        
        self.handler = self
        self.shape = self
        self.id = 0
        self._formatted = False
        self.canvas = canvas
        self.x = 0.0
        self.y = 0.0
        self._pen = BlackForegroundPen
        self._brush = wx.WHITE_BRUSH
        self._font = NormalFont
        self._textColour = wx.BLACK
        self._textColourName = wx.BLACK
        self._visible = False
        self._selected = False
        self._attachmentMode = ATTACHMENT_MODE_NONE
        self._spaceAttachments = True
        self._disableLabel = False
        self._fixedWidth = False
        self._fixedHeight = False
        self._drawHandles = True
        self._sensitivity = OP_ALL
        self._draggable = True
        self._parent = None
        self._formatMode = FORMAT_CENTRE_HORIZ | FORMAT_CENTRE_VERT
        self._shadowMode = SHADOW_NONE
        self._shadowOffsetX = 6
        self._shadowOffsetY = 6
        self._shadowBrush = wx.BLACK_BRUSH
        self._textMarginX = 5
        self._textMarginY = 5
        self._regionName = "0"
        self._centreResize = True
        self._maintainAspectRatio = False
        self._highlighted = False
        self._rotation = 0.0
        self._branchNeckLength = 10
        self._branchStemLength = 10
        self._branchSpacing = 10
        self._branchStyle = BRANCHING_ATTACHMENT_NORMAL
        
        self._regions = []
        self._lines = []
        self._controlPoints = []
        self._attachmentPoints = []
        self._text = []
        self._children = []
        
        # Set up a default region. Much of the above will be put into
        # the region eventually (the duplication is for compatibility)
        region = ShapeRegion()
        region.SetName("0")
        region.SetFont(NormalFont)
        region.SetFormatMode(FORMAT_CENTRE_HORIZ | FORMAT_CENTRE_VERT)
        region.SetColour("BLACK")
        self._regions.append(region)

    def __str__(self):
        return "<%s.%s>" % (self.__class__.__module__, self.__class__.__name__)

    def GetClassName(self):
        return str(self.__class__).split(".")[-1][:-2]


    def Delete(self):
        """
        Fully disconnect this shape from parents, children, the
        canvas, etc.
        """
        if self._parent:
            self._parent.GetChildren().remove(self)

        for child in self.GetChildren():
            child.Delete()

        self.ClearText()
        self.ClearRegions()
        self.ClearAttachments()

        self.shape = None
        
        if self.canvas:
            self.RemoveFromCanvas(self.canvas)

        if self.handler:
            self.handler.OnDelete()
        self.handler = None
        
    def __del__(self):
        ShapeEvtHandler.__del__(self)

    def Draggable(self):
        """TRUE if the shape may be dragged by the user."""
        return True
    
    def GetBranchStyle(self):
        return self._branchStyle

    def GetRotation(self):
        """Return the angle of rotation in radians."""
        return self._rotation

    def SetRotation(self, rotation):
        self._rotation = rotation
        
    def SetHighlight(self, hi, recurse = False):
        """Set the highlight for a shape. Shape highlighting is unimplemented."""
        self._highlighted = hi
        if recurse:
            for shape in self._children:
                shape.SetHighlight(hi, recurse)

    def SetSensitivityFilter(self, sens = OP_ALL, recursive = False):
        """Set the shape to be sensitive or insensitive to specific mouse
        operations.

        sens is a bitlist of the following:

        * OP_CLICK_LEFT
        * OP_CLICK_RIGHT
        * OP_DRAG_LEFT
        * OP_DRAG_RIGHT
        * OP_ALL (equivalent to a combination of all the above).
        """
        self._draggable = sens & OP_DRAG_LEFT

        self._sensitivity = sens
        if recursive:
            for shape in self._children:
                shape.SetSensitivityFilter(sens, True)

    def SetDraggable(self, drag, recursive = False):
        """Set the shape to be draggable or not draggable."""
        self._draggable = drag
        if drag:
            self._sensitivity |= OP_DRAG_LEFT
        elif self._sensitivity & OP_DRAG_LEFT:
            self._sensitivity -= OP_DRAG_LEFT

        if recursive:
            for shape in self._children:
                shape.SetDraggable(drag, True)

    def SetDrawHandles(self, drawH):
        """Set the drawHandles flag for this shape and all descendants.
        If drawH is TRUE (the default), any handles (control points) will
        be drawn. Otherwise, the handles will not be drawn.
        """
        self._drawHandles = drawH
        for shape in self._children:
            shape.SetDrawHandles(drawH)

    def SetShadowMode(self, mode, redraw = False):
        """Set the shadow mode (whether a shadow is drawn or not).
        mode can be one of the following:

        SHADOW_NONE
          No shadow (the default). 
        SHADOW_LEFT
          Shadow on the left side. 
        SHADOW_RIGHT
          Shadow on the right side.
        """
        if redraw and self.canvas:
            dc = wx.ClientDC(self.canvas)
            self.canvas.PrepareDC(dc)
            self.Erase(dc)
            self._shadowMode = mode
            self.Draw(dc)
        else:
            self._shadowMode = mode

    def GetShadowMode(self):
        """Return the current shadow mode setting"""
        return self._shadowMode

    def SetCanvas(self, theCanvas):
        """Identical to Shape.Attach."""
        self.canvas = theCanvas
        for shape in self._children:
            shape.SetCanvas(theCanvas)

    def AddToCanvas(self, theCanvas, addAfter = None):
        """Add the shape to the canvas's shape list.
        If addAfter is non-NULL, will add the shape after this one.
        """
        theCanvas.AddShape(self, addAfter)

        lastImage = self
        for object in self._children:
            object.AddToCanvas(theCanvas, lastImage)
            lastImage = object

    def InsertInCanvas(self, theCanvas):
        """Insert the shape at the front of the shape list of canvas."""
        theCanvas.InsertShape(self)

        lastImage = self
        for object in self._children:
            object.AddToCanvas(theCanvas, lastImage)
            lastImage = object

    def RemoveFromCanvas(self, theCanvas):
        """Remove the shape from the canvas."""
        if self.Selected():
            self.Select(False)
        
        self.canvas = None
        theCanvas.RemoveShape(self)
        for object in self._children:
            object.RemoveFromCanvas(theCanvas)

    def ClearAttachments(self):
        """Clear internal custom attachment point shapes (of class
        wxAttachmentPoint).
        """
        self._attachmentPoints = []

    def ClearText(self, regionId = 0):
        """Clear the text from the specified text region."""
        if regionId == 0:
            self._text = ""
        if regionId < len(self._regions):
            self._regions[regionId].ClearText()
            
    def ClearRegions(self):
        """Clear the ShapeRegions from the shape."""
        self._regions = []
            
    def AddRegion(self, region):
        """Add a region to the shape."""
        self._regions.append(region)

    def SetDefaultRegionSize(self):
        """Set the default region to be consistent with the shape size."""
        if not self._regions:
            return
        w, h = self.GetBoundingBoxMax()
        self._regions[0].SetSize(w, h)

    def HitTest(self, x, y):
        """Given a point on a canvas, returns TRUE if the point was on the
        shape, and returns the nearest attachment point and distance from
        the given point and target.
        """
        width, height = self.GetBoundingBoxMax()
        if abs(width) < 4:
            width = 4.0
        if abs(height) < 4:
            height = 4.0

        width += 4 # Allowance for inaccurate mousing
        height += 4
        
        left = self.x - width / 2.0
        top = self.y - height / 2.0
        right = self.x + width / 2.0
        bottom = self.y + height / 2.0

        nearest_attachment = 0

        # If within the bounding box, check the attachment points
        # within the object.
        if x >= left and x <= right and y >= top and y <= bottom:
            n = self.GetNumberOfAttachments()
            nearest = 999999

            # GetAttachmentPosition[Edge] takes a logical attachment position,
            # i.e. if it's rotated through 90%, position 0 is East-facing.

            for i in range(n):
                e = self.GetAttachmentPositionEdge(i)
                if e:
                    xp, yp = e
                    l = math.sqrt(((xp - x) * (xp - x)) + (yp - y) * (yp - y))
                    if l < nearest:
                        nearest = l
                        nearest_attachment = i

            return nearest_attachment, nearest
        return False
    
    # Format a text string according to the region size, adding
    # strings with positions to region text list
    
    def FormatText(self, dc, s, i = 0):
        """Reformat the given text region; defaults to formatting the
        default region.
        """
        self.ClearText(i)

        if not self._regions:
            return

        if i > len(self._regions):
            return

        region = self._regions[i]
        region._regionText = s
        dc.SetFont(region.GetFont())

        w, h = region.GetSize()

        stringList = FormatText(dc, s, (w - 2 * self._textMarginX),
                                (h - 2 * self._textMarginY), region.GetFormatMode())
        for s in stringList:
            line = ShapeTextLine(0.0, 0.0, s)
            region.GetFormattedText().append(line)

        actualW = w
        actualH = h
        # Don't try to resize an object with more than one image (this
        # case should be dealt with by overriden handlers)
        if (region.GetFormatMode() & FORMAT_SIZE_TO_CONTENTS) and \
           len(region.GetFormattedText()) and \
           len(self._regions) == 1 and \
           not Shape.GraphicsInSizeToContents:

            actualW, actualH = GetCentredTextExtent(dc, region.GetFormattedText())
            if actualW + 2 * self._textMarginX != w or actualH + 2 * self._textMarginY != h:
                # If we are a descendant of a composite, must make sure
                # the composite gets resized properly

                topAncestor = self.GetTopAncestor()
                if topAncestor != self:
                    Shape.GraphicsInSizeToContents = True

                    composite = topAncestor
                    composite.Erase(dc)
                    self.SetSize(actualW + 2 * self._textMarginX, actualH + 2 * self._textMarginY)
                    self.Move(dc, self.x, self.y)
                    composite.CalculateSize()
                    if composite.Selected():
                        composite.DeleteControlPoints(dc)
                        composite.MakeControlPoints()
                        composite.MakeMandatoryControlPoints()
                    # Where infinite recursion might happen if we didn't stop it
                    composite.Draw(dc)
                    Shape.GraphicsInSizeToContents = False
                else:
                    self.Erase(dc)
                    
                self.SetSize(actualW + 2 * self._textMarginX, actualH + 2 * self._textMarginY)
                self.Move(dc, self.x, self.y)
                self.EraseContents(dc)
        CentreText(dc, region.GetFormattedText(), self.x, self.y, actualW - 2 * self._textMarginX, actualH - 2 * self._textMarginY, region.GetFormatMode())
        self._formatted = True

    def Recentre(self, dc):
        """Do recentring (or other formatting) for all the text regions
        for this shape.
        """
        w, h = self.GetBoundingBoxMin()
        for region in self._regions:
            CentreText(dc, region.GetFormattedText(), self.x, self.y, w - 2 * self._textMarginX, h - 2 * self._textMarginY, region.GetFormatMode())

    def GetPerimeterPoint(self, x1, y1, x2, y2):
        """Get the point at which the line from (x1, y1) to (x2, y2) hits
        the shape. Returns False if the line doesn't hit the perimeter.
        """
        return False

    def SetPen(self, the_pen):
        """Set the pen for drawing the shape's outline."""
        self._pen = the_pen

    def SetBrush(self, the_brush):
        """Set the brush for filling the shape's shape."""
        self._brush = the_brush

    # Get the top - most (non-division) ancestor, or self
    def GetTopAncestor(self):
        """Return the top-most ancestor of this shape (the root of
        the composite).
        """
        if not self.GetParent():
            return self

        if isinstance(self.GetParent(), DivisionShape):
            return self
        return self.GetParent().GetTopAncestor()

    # Region functions
    def SetFont(self, the_font, regionId = 0):
        """Set the font for the specified text region."""
        self._font = the_font
        if regionId < len(self._regions):
            self._regions[regionId].SetFont(the_font)

    def GetFont(self, regionId = 0):
        """Get the font for the specified text region."""
        if regionId >= len(self._regions):
            return None
        return self._regions[regionId].GetFont()

    def SetFormatMode(self, mode, regionId = 0):
        """Set the format mode of the default text region. The argument
        can be a bit list of the following:

        FORMAT_NONE
          No formatting. 
        FORMAT_CENTRE_HORIZ
          Horizontal centring. 
        FORMAT_CENTRE_VERT
          Vertical centring.
        """
        if regionId < len(self._regions):
            self._regions[regionId].SetFormatMode(mode)

    def GetFormatMode(self, regionId = 0):
        if regionId >= len(self._regions):
            return 0
        return self._regions[regionId].GetFormatMode()

    def SetTextColour(self, the_colour, regionId = 0):
        """Set the colour for the specified text region."""
        self._textColour = wx.TheColourDatabase.Find(the_colour)
        self._textColourName = the_colour

        if regionId < len(self._regions):
            self._regions[regionId].SetColour(the_colour)
            
    def GetTextColour(self, regionId = 0):
        """Get the colour for the specified text region."""
        if regionId >= len(self._regions):
            return ""
        return self._regions[regionId].GetColour()

    def SetRegionName(self, name, regionId = 0):
        """Set the name for this region.
        The name for a region is unique within the scope of the whole
        composite, whereas a region id is unique only for a single image.
        """
        if regionId < len(self._regions):
            self._regions[regionId].SetName(name)

    def GetRegionName(self, regionId = 0):
        """Get the region's name.
        A region's name can be used to uniquely determine a region within
        an entire composite image hierarchy. See also Shape.SetRegionName.
        """
        if regionId >= len(self._regions):
            return ""
        return self._regions[regionId].GetName()

    def GetRegionId(self, name):
        """Get the region's identifier by name.
        This is not unique for within an entire composite, but is unique
        for the image.
        """
        for i, r in enumerate(self._regions):
            if r.GetName() == name:
                return i
        return -1

    # Name all _regions in all subimages recursively
    def NameRegions(self, parentName=""):
        """Make unique names for all the regions in a shape or composite shape."""
        n = self.GetNumberOfTextRegions()
        for i in range(n):
            if parentName:
                buff = parentName+"."+str(i)
            else:
                buff = str(i)
            self.SetRegionName(buff, i)

        for j, child in enumerate(self._children):
            if parentName:
                buff = parentName+"."+str(j)
            else:
                buff = str(j)
            child.NameRegions(buff)

    # Get a region by name, possibly looking recursively into composites
    def FindRegion(self, name):
        """Find the actual image ('this' if non-composite) and region id
        for the given region name.
        """
        id = self.GetRegionId(name)
        if id > -1:
            return self, id

        for child in self._children:
            actualImage, regionId = child.FindRegion(name)
            if actualImage:
                return actualImage, regionId

        return None, -1

    # Finds all region names for this image (composite or simple).
    def FindRegionNames(self):
        """Get a list of all region names for this image (composite or simple)."""
        list = []
        n = self.GetNumberOfTextRegions()
        for i in range(n):
            list.append(self.GetRegionName(i))

        for child in self._children:
            list += child.FindRegionNames()

        return list

    def AssignNewIds(self):
        """Assign new ids to this image and its children."""
        self.id = wx.NewId()
        for child in self._children:
            child.AssignNewIds()

    def OnDraw(self, dc):
        pass

    def OnMoveLinks(self, dc):
        # Want to set the ends of all attached links
        # to point to / from this object

        for line in self._lines:
            line.handler.OnMoveLink(dc)

    def OnDrawContents(self, dc):
        if not self._regions:
            return
        
        bound_x, bound_y = self.GetBoundingBoxMin()

        if self._pen:
            dc.SetPen(self._pen)

        for region in self._regions:
            if region.GetFont():
                dc.SetFont(region.GetFont())

            dc.SetTextForeground(region.GetActualColourObject())
            dc.SetBackgroundMode(wx.TRANSPARENT)
            if not self._formatted:
                CentreText(dc, region.GetFormattedText(), self.x, self.y, bound_x - 2 * self._textMarginX, bound_y - 2 * self._textMarginY, region.GetFormatMode())
                self._formatted = True

            if not self.GetDisableLabel():
                DrawFormattedText(dc, region.GetFormattedText(), self.x, self.y, bound_x - 2 * self._textMarginX, bound_y - 2 * self._textMarginY, region.GetFormatMode())
            

    def DrawContents(self, dc):
        """Draw the internal graphic of the shape (such as text).

        Do not override this function: override OnDrawContents, which
        is called by this function.
        """
        self.handler.OnDrawContents(dc)

    def OnSize(self, x, y):
        pass

    def OnMovePre(self, dc, x, y, old_x, old_y, display = True):
        return True

    def OnErase(self, dc):
        if not self._visible:
            return

        # Erase links
        for line in self._lines:
            line.handler.OnErase(dc)

        self.handler.OnEraseContents(dc)

    def OnEraseContents(self, dc):
        if not self._visible:
            return
        
        xp, yp = self.x, self.y
        minX, minY = self.GetBoundingBoxMin()
        maxX, maxY = self.GetBoundingBoxMax()

        topLeftX = xp - maxX / 2.0 - 2
        topLeftY = yp - maxY / 2.0 - 2

        penWidth = 0
        if self._pen:
            penWidth = self._pen.GetWidth()

        dc.SetPen(self.GetBackgroundPen())
        dc.SetBrush(self.GetBackgroundBrush())

        dc.DrawRectangle(topLeftX - penWidth, topLeftY - penWidth, maxX + penWidth * 2 + 4, maxY + penWidth * 2 + 4)

    def EraseLinks(self, dc, attachment = -1, recurse = False):
        """Erase links attached to this shape, but do not repair damage
        caused to other shapes.
        """
        if not self._visible:
            return

        for line in self._lines:
            if attachment == -1 or (line.GetTo() == self and line.GetAttachmentTo() == attachment or line.GetFrom() == self and line.GetAttachmentFrom() == attachment):
                line.handler.OnErase(dc)

        if recurse:
            for child in self._children:
                child.EraseLinks(dc, attachment, recurse)

    def DrawLinks(self, dc, attachment = -1, recurse = False):
        """Draws any lines linked to this shape."""
        if not self._visible:
            return

        for line in self._lines:
            if attachment == -1 or (line.GetTo() == self and line.GetAttachmentTo() == attachment or line.GetFrom() == self and line.GetAttachmentFrom() == attachment):
                line.Draw(dc)
                
        if recurse:
            for child in self._children:
                child.DrawLinks(dc, attachment, recurse)

    #  Returns TRUE if pt1 <= pt2 in the sense that one point comes before
    #  another on an edge of the shape.
    # attachmentPoint is the attachment point (= side) in question.

    # This is the default, rectangular implementation.
    def AttachmentSortTest(self, attachmentPoint, pt1, pt2):
        """Return TRUE if pt1 is less than or equal to pt2, in the sense
        that one point comes before another on an edge of the shape.

        attachment is the attachment point (side) in question.

        This function is used in Shape.MoveLineToNewAttachment to determine
        the new line ordering.
        """
        physicalAttachment = self.LogicalToPhysicalAttachment(attachmentPoint)
        if physicalAttachment in [0, 2]:
            return pt1[0] <= pt2[0]
        elif physicalAttachment in [1, 3]:
            return pt1[1] <= pt2[1]

        return False

    def MoveLineToNewAttachment(self, dc, to_move, x, y):
        """Move the given line (which must already be attached to the shape)
        to a different attachment point on the shape, or a different order
        on the same attachment.

        Calls Shape.AttachmentSortTest and then
        ShapeEvtHandler.OnChangeAttachment.
        """
        if self.GetAttachmentMode() == ATTACHMENT_MODE_NONE:
            return False

        # Is (x, y) on this object? If so, find the new attachment point
        # the user has moved the point to
        hit = self.HitTest(x, y)
        if not hit:
            return False

        newAttachment, distance = hit
        
        self.EraseLinks(dc)

        if to_move.GetTo() == self:
            oldAttachment = to_move.GetAttachmentTo()
        else:
            oldAttachment = to_move.GetAttachmentFrom()

        # The links in a new ordering
        # First, add all links to the new list
        newOrdering = self._lines[:]
        
        # Delete the line object from the list of links; we're going to move
        # it to another position in the list
        del newOrdering[newOrdering.index(to_move)]

        old_x = -99999.9
        old_y = -99999.9

        found = False

        for line in newOrdering:
            if line.GetTo() == self and oldAttachment == line.GetAttachmentTo() or \
               line.GetFrom() == self and oldAttachment == line.GetAttachmentFrom():
                startX, startY, endX, endY = line.GetEnds()
                if line.GetTo() == self:
                    xp = endX
                    yp = endY
                else:
                    xp = startX
                    yp = startY

                thisPoint = wx.RealPoint(xp, yp)
                lastPoint = wx.RealPoint(old_x, old_y)
                newPoint = wx.RealPoint(x, y)

                if self.AttachmentSortTest(newAttachment, newPoint, thisPoint) and self.AttachmentSortTest(newAttachment, lastPoint, newPoint):
                    found = True
                    newOrdering.insert(newOrdering.index(line), to_move)

                old_x = xp
                old_y = yp
            if found:
                break

        if not found:
            newOrdering.append(to_move)

        self.handler.OnChangeAttachment(newAttachment, to_move, newOrdering)
        return True

    def OnChangeAttachment(self, attachment, line, ordering):
        if line.GetTo() == self:
            line.SetAttachmentTo(attachment)
        else:
            line.SetAttachmentFrom(attachment)

        self.ApplyAttachmentOrdering(ordering)

        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)
        self.MoveLinks(dc)

        self.canvas.quickRedraw(dc)

    # Reorders the lines according to the given list
    def ApplyAttachmentOrdering(self, linesToSort):
        """Apply the line ordering in linesToSort to the shape, to reorder
        the way lines are attached.
        """
        linesStore = self._lines[:]

        self._lines = []

        for line in linesToSort:
            if line in linesStore:
                del linesStore[linesStore.index(line)]
                self._lines.append(line)

        # Now add any lines that haven't been listed in linesToSort
        self._lines += linesStore

    def SortLines(self, attachment, linesToSort):
        """ Reorder the lines coming into the node image at this attachment
        position, in the order in which they appear in linesToSort.

        Any remaining lines not in the list will be added to the end.
        """
        # This is a temporary store of all the lines at this attachment
        # point. We'll tick them off as we've processed them.
        linesAtThisAttachment = []

        for line in self._lines[:]:
            if line.GetTo() == self and line.GetAttachmentTo() == attachment or \
               line.GetFrom() == self and line.GetAttachmentFrom() == attachment:
                linesAtThisAttachment.append(line)
                del self._lines[self._lines.index(line)]

        for line in linesToSort:
            if line in linesAtThisAttachment:
                # Done this one
                del linesAtThisAttachment[linesAtThisAttachment.index(line)]
                self._lines.append(line)

        # Now add any lines that haven't been listed in linesToSort
        self._lines += linesAtThisAttachment

    def OnHighlight(self, dc):
        pass

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        if self._sensitivity & OP_CLICK_LEFT != OP_CLICK_LEFT:
            if self._parent:
                attachment, dist = self._parent.HitTest(x, y)
                self._parent.handler.OnLeftClick(x, y, keys, attachment)

    def OnRightClick(self, x, y, keys = 0, attachment = 0):
        if self._sensitivity & OP_CLICK_RIGHT != OP_CLICK_RIGHT:
            attachment, dist = self._parent.HitTest(x, y)
            self._parent.handler.OnRightClick(x, y, keys, attachment)

    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        if self._sensitivity & OP_DRAG_LEFT != OP_DRAG_LEFT:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.handler.OnDragLeft(draw, x, y, keys, attachment)
            return


        xx = x + DragOffsetX
        yy = y + DragOffsetY

        xx, yy = self.canvas.Snap(xx, yy)
        w, h = self.GetBoundingBoxMax()
        self.handler.OnDrawOutline(xx, yy, w, h)

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        global DragOffsetX, DragOffsetY
        
        if self._sensitivity & OP_DRAG_LEFT != OP_DRAG_LEFT:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.handler.OnBeginDragLeft(x, y, keys, attachment)
            return

        DragOffsetX = self.x - x
        DragOffsetY = self.y - y

        xx = x + DragOffsetX
        yy = y + DragOffsetY
        xx, yy = self.canvas.Snap(xx, yy)

        w, h = self.GetBoundingBoxMax()
        self.handler.OnDrawOutline(xx, yy, w, h)
        self.canvas.CaptureMouse()

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        if self.canvas.HasCapture():
            self.canvas.ReleaseMouse()
        if self._sensitivity & OP_DRAG_LEFT != OP_DRAG_LEFT:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.handler.OnEndDragLeft(x, y, keys, attachment)
            return

        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        dc.SetLogicalFunction(wx.COPY)
        xx = x + DragOffsetX
        yy = y + DragOffsetY
        xx, yy = self.canvas.Snap(xx, yy)

        # New policy: erase shape at end of drag.
        self.Erase(dc)

        self.Move(dc, xx, yy)
        self.canvas.quickRedraw(dc)

    def OnDragRight(self, draw, x, y, keys = 0, attachment = 0):
        if self._sensitivity & OP_DRAG_RIGHT != OP_DRAG_RIGHT:
            if self._parent:
                attachment, dist = self._parent.HitTest(x, y)
                self._parent.handler.OnDragRight(draw, x, y, keys, attachment)
            return

    def OnBeginDragRight(self, x, y, keys = 0, attachment = 0):
        if self._sensitivity & OP_DRAG_RIGHT != OP_DRAG_RIGHT:
            if self._parent:
                attachment, dist = self._parent.HitTest(x, y)
                self._parent.handler.OnBeginDragRight(x, y, keys, attachment)
            return

    def OnEndDragRight(self, x, y, keys = 0, attachment = 0):
        if self._sensitivity & OP_DRAG_RIGHT != OP_DRAG_RIGHT:
            if self._parent:
                attachment, dist = self._parent.HitTest(x, y)
                self._parent.handler.OnEndDragRight(x, y, keys, attachment)
            return



    def OnDrawOutline(self, x, y, w, h):
        dc = self.buildOutlineDC()
        points = [[x - w / 2.0, y - h / 2.0],
                [x + w / 2.0, y - h / 2.0],
                [x + w / 2.0, y + h / 2.0],
                [x - w / 2.0, y + h / 2.0],
                [x - w / 2.0, y - h / 2.0],
                ]
        dc.DrawLines(points)

    def buildOutlineDC(self):
        assert self.canvas
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)
        dc.SetLogicalFunction(OGLRBLF)
        
        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        return dc
        

    def Move(self, dc, x, y, display = True):
        """Move the shape to the given position.
        Redraw if display is TRUE.
        """
        old_x = self.x
        old_y = self.y

        if not self.handler.OnMovePre(dc, x, y, old_x, old_y, display):
            return

        self.x, self.y = x, y

        self.ResetControlPoints()

        if display:
            self.Draw(dc)

        self.MoveLinks(dc)

        self.handler.OnMovePost(dc, x, y, old_x, old_y, display)

    def MoveLinks(self, dc):
        """Redraw all the lines attached to the shape."""
        self.handler.OnMoveLinks(dc)

    def Draw(self, dc):
        """Draw the whole shape and any lines attached to it.

        Do not override this function: override OnDraw, which is called
        by this function.
        """
        if self._visible:
            self.handler.OnDraw(dc)
            self.handler.OnDrawContents(dc)
            self.handler.OnDrawControlPoints(dc)
            self.handler.OnDrawBranches(dc)

    def Flash(self):
        """Flash the shape."""
        if self.canvas:
            dc = wx.ClientDC(self.canvas)
            self.canvas.PrepareDC(dc)

            dc.SetLogicalFunction(OGLRBLF)
            self.Draw(dc)
            dc.SetLogicalFunction(wx.COPY)
            self.Draw(dc)

    def Show(self, show):
        """Set a flag indicating whether the shape should be drawn."""
        self._visible = show
        for child in self._children:
            child.Show(show)

    def Erase(self, dc):
        """Erase the shape.
        Does not repair damage caused to other shapes.
        """
        self.handler.OnErase(dc)
        self.handler.OnEraseControlPoints(dc)
        self.handler.OnDrawBranches(dc, erase = True)

    def EraseContents(self, dc):
        """Erase the shape contents, that is, the area within the shape's
        minimum bounding box.
        """
        self.handler.OnEraseContents(dc)

    def AddText(self, string):
        """Add a line of text to the shape's default text region."""
        if not self._regions:
            return

        region = self._regions[0]
        #region.ClearText()
        new_line = ShapeTextLine(0, 0, string)
        text = region.GetFormattedText()
        text.append(new_line)

        self._formatted = False

    def SetSize(self, x, y, recursive = True):
        """Set the shape's size."""
        self.SetAttachmentSize(x, y)
        self.SetDefaultRegionSize()

    def SetAttachmentSize(self, w, h):
        width, height = self.GetBoundingBoxMin()
        if width == 0:
            scaleX = 1.0
        else:
            scaleX = float(w) / width
        if height == 0:
            scaleY = 1.0
        else:
            scaleY = float(h) / height

        for point in self._attachmentPoints:
            point.x = point.x * scaleX
            point.y = point.y * scaleY

    # Add line FROM this object
    def AddLine(self, line, other, attachFrom = 0, attachTo = 0, positionFrom = -1, positionTo = -1):
        """Add a line between this shape and the given other shape, at the
        specified attachment points.

        The position in the list of lines at each end can also be specified,
        so that the line will be drawn at a particular point on its attachment
        point.
        """
        if positionFrom == -1:
            if not line in self._lines:
                self._lines.append(line)
        else:
            # Don't preserve old ordering if we have new ordering instructions
            try:
                self._lines.remove(line)
            except ValueError:
                pass
            if positionFrom < len(self._lines):
                self._lines.insert(positionFrom, line)
            else:
                self._lines.append(line)

        if positionTo == -1:
            if not other in other._lines:
                other._lines.append(line)
        else:
            # Don't preserve old ordering if we have new ordering instructions
            try:
                other._lines.remove(line)
            except ValueError:
                pass
            if positionTo < len(other._lines):
                other._lines.insert(positionTo, line)
            else:
                other._lines.append(line)
            
        line.SetFrom(self)
        line.SetTo(other)
        line.SetAttachments(attachFrom, attachTo)

        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)
        self.MoveLinks(dc)
        
    def RemoveLine(self, line):
        """Remove the given line from the shape's list of attached lines."""
        if line.GetFrom() == self:
            line.GetTo()._lines.remove(line)
        else:
            line.GetFrom()._lines.remove(line)

        self._lines.remove(line)

    # Default - make 6 control points
    def MakeControlPoints(self):
        """Make a list of control points (draggable handles) appropriate to
        the shape.
        """
        maxX, maxY = self.GetBoundingBoxMax()
        minX, minY = self.GetBoundingBoxMin()

        widthMin = minX + CONTROL_POINT_SIZE + 2
        heightMin = minY + CONTROL_POINT_SIZE + 2

        # Offsets from main object
        top = -heightMin / 2.0
        bottom = heightMin / 2.0 + (maxY - minY)
        left = -widthMin / 2.0
        right = widthMin / 2.0 + (maxX - minX)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, left, top, CONTROL_POINT_DIAGONAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, 0, top, CONTROL_POINT_VERTICAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, right, top, CONTROL_POINT_DIAGONAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, right, 0, CONTROL_POINT_HORIZONTAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, right, bottom, CONTROL_POINT_DIAGONAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, 0, bottom, CONTROL_POINT_VERTICAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, left, bottom, CONTROL_POINT_DIAGONAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

        control = ControlPoint(self.canvas, self, CONTROL_POINT_SIZE, left, 0, CONTROL_POINT_HORIZONTAL)
        self.canvas.AddShape(control)
        self._controlPoints.append(control)

    def MakeMandatoryControlPoints(self):
        """Make the mandatory control points.

        For example, the control point on a dividing line should appear even
        if the divided rectangle shape's handles should not appear (because
        it is the child of a composite, and children are not resizable).
        """
        for child in self._children:
            child.MakeMandatoryControlPoints()

    def ResetMandatoryControlPoints(self):
        """Reset the mandatory control points."""
        for child in self._children:
            child.ResetMandatoryControlPoints()

    def ResetControlPoints(self):
        """Reset the positions of the control points (for instance when the
        shape's shape has changed).
        """
        self.ResetMandatoryControlPoints()

        if len(self._controlPoints) == 0:
            return

        maxX, maxY = self.GetBoundingBoxMax()
        minX, minY = self.GetBoundingBoxMin()

        widthMin = minX + CONTROL_POINT_SIZE + 2
        heightMin = minY + CONTROL_POINT_SIZE + 2
        
        # Offsets from main object
        top = -heightMin / 2.0
        bottom = heightMin / 2.0 + (maxY - minY)
        left = -widthMin / 2.0
        right = widthMin / 2.0 + (maxX - minX)

        self._controlPoints[0].xoffset = left
        self._controlPoints[0].yoffset = top

        self._controlPoints[1].xoffset = 0
        self._controlPoints[1].yoffset = top

        self._controlPoints[2].xoffset = right
        self._controlPoints[2].yoffset = top

        self._controlPoints[3].xoffset = right
        self._controlPoints[3].yoffset = 0

        self._controlPoints[4].xoffset = right
        self._controlPoints[4].yoffset = bottom

        self._controlPoints[5].xoffset = 0
        self._controlPoints[5].yoffset = bottom

        self._controlPoints[6].xoffset = left
        self._controlPoints[6].yoffset = bottom

        self._controlPoints[7].xoffset = left
        self._controlPoints[7].yoffset = 0

    def DeleteControlPoints(self, dc = None):
        """Delete the control points (or handles) for the shape.

        Does not redraw the shape.
        """
        for control in self._controlPoints[:]:
            if dc:
                control.handler.OnErase(dc)
            control.Delete()
            self._controlPoints.remove(control)
        self._controlPoints = []
        
        # Children of divisions are contained objects,
        # so stop here
        if not isinstance(self, DivisionShape):
            for child in self._children:
                child.DeleteControlPoints(dc)

    def OnDrawControlPoints(self, dc):
        if not self._drawHandles:
            return

        dc.SetBrush(wx.BLACK_BRUSH)
        dc.SetPen(wx.BLACK_PEN)

        for control in self._controlPoints:
            control.Draw(dc)

        # Children of divisions are contained objects,
        # so stop here.
        # This test bypasses the type facility for speed
        # (critical when drawing)

        if not isinstance(self, DivisionShape):
            for child in self._children:
                child.handler.OnDrawControlPoints(dc)

    def OnEraseControlPoints(self, dc):
        for control in self._controlPoints:
            control.Erase(dc)

        if not isinstance(self, DivisionShape):
            for child in self._children:
                child.handler.OnEraseControlPoints(dc)

    def Select(self, select, dc = None):
        """Select or deselect the given shape, drawing or erasing control points
        (handles) as necessary.
        """
        self._selected = select
        if select:
            self.MakeControlPoints()
            # Children of divisions are contained objects,
            # so stop here
            if not isinstance(self, DivisionShape):
                for child in self._children:
                    child.MakeMandatoryControlPoints()
            if dc:
                self.handler.OnDrawControlPoints(dc)
        else:
            self.DeleteControlPoints(dc)
            if not isinstance(self, DivisionShape):
                for child in self._children:
                    child.DeleteControlPoints(dc)

    def Selected(self):
        """TRUE if the shape is currently selected."""
        return self._selected

    def AncestorSelected(self):
        """TRUE if the shape's ancestor is currently selected."""
        if self._selected:
            return True
        if not self.GetParent():
            return False
        return self.GetParent().AncestorSelected()

    def GetNumberOfAttachments(self):
        """Get the number of attachment points for this shape."""
        # Should return the MAXIMUM attachment point id here,
        # so higher-level functions can iterate through all attachments,
        # even if they're not contiguous.

        if len(self._attachmentPoints) == 0:
            return 4
        else:
            maxN = 3
            for point in self._attachmentPoints:
                if point.id > maxN:
                    maxN = point.id
            return maxN + 1

    def AttachmentIsValid(self, attachment):
        """TRUE if attachment is a valid attachment point."""
        if len(self._attachmentPoints) == 0:
            return attachment in range(4)

        for point in self._attachmentPoints:
            if point.id == attachment:
                return True
        return False

    def GetAttachmentPosition(self, attachment, nth = 0, no_arcs = 1, line = None):
        """Get the position at which the given attachment point should be drawn.

        If attachment isn't found among the attachment points of the shape,
        returns None.
        """
        if self._attachmentMode == ATTACHMENT_MODE_NONE:
            return self.x, self.y
        elif self._attachmentMode == ATTACHMENT_MODE_BRANCHING:
            pt, stemPt = self.GetBranchingAttachmentPoint(attachment, nth)
            return pt[0], pt[1]
        elif self._attachmentMode == ATTACHMENT_MODE_EDGE:
            if len(self._attachmentPoints):
                for point in self._attachmentPoints:
                    if point.id == attachment:
                        return self.x + point.x, self.y + point.y
                return None
            else:
                # Assume is rectangular
                w, h = self.GetBoundingBoxMax()
                top = self.y + h / 2.0
                bottom = self.y - h / 2.0
                left = self.x - w / 2.0
                right = self.x + w / 2.0

                # wtf?
                line and line.IsEnd(self)

                physicalAttachment = self.LogicalToPhysicalAttachment(attachment)

                # Simplified code
                if physicalAttachment == 0:
                    pt = self.CalcSimpleAttachment((left, bottom), (right, bottom), nth, no_arcs, line)
                elif physicalAttachment == 1:
                    pt = self.CalcSimpleAttachment((right, bottom), (right, top), nth, no_arcs, line)
                elif physicalAttachment == 2:
                    pt = self.CalcSimpleAttachment((left, top), (right, top), nth, no_arcs, line)
                elif physicalAttachment == 3:
                    pt = self.CalcSimpleAttachment((left, bottom), (left, top), nth, no_arcs, line)
                else:
                    return None
                return pt[0], pt[1]
        return None

    def GetBoundingBoxMax(self):
        """Get the maximum bounding box for the shape, taking into account
        external features such as shadows.
        """
        ww, hh = self.GetBoundingBoxMin()
        if self._shadowMode != SHADOW_NONE:
            ww += self._shadowOffsetX
            hh += self._shadowOffsetY
        return ww, hh

    def GetBoundingBoxMin(self):
        """Get the minimum bounding box for the shape, that defines the area
        available for drawing the contents (such as text).

        Must be overridden.
        """
        return 0, 0
    
    def HasDescendant(self, image):
        """TRUE if image is a descendant of this composite."""
        if image == self:
            return True
        for child in self._children:
            if child.HasDescendant(image):
                return True
        return False

    # Assuming the attachment lies along a vertical or horizontal line,
    # calculate the position on that point.
    def CalcSimpleAttachment(self, pt1, pt2, nth, noArcs, line):
        """Assuming the attachment lies along a vertical or horizontal line,
        calculate the position on that point.

        Parameters:

        pt1
            The first point of the line repesenting the edge of the shape.

        pt2
            The second point of the line representing the edge of the shape.

        nth
            The position on the edge (for example there may be 6 lines at
            this attachment point, and this may be the 2nd line.

        noArcs
            The number of lines at this edge.

        line
            The line shape.

        Remarks

        This function expects the line to be either vertical or horizontal,
        and determines which.
        """
        isEnd = line and line.IsEnd(self)

        # Are we horizontal or vertical?
        isHorizontal = RoughlyEqual(pt1[1], pt2[1])

        if isHorizontal:
            if pt1[0] > pt2[0]:
                firstPoint = pt2
                secondPoint = pt1
            else:
                firstPoint = pt1
                secondPoint = pt2

            if self._spaceAttachments:
                if line and line.GetAlignmentType(isEnd) == LINE_ALIGNMENT_TO_NEXT_HANDLE:
                    # Align line according to the next handle along
                    point = line.GetNextControlPoint(self)
                    if point[0] < firstPoint[0]:
                        x = firstPoint[0]
                    elif point[0] > secondPoint[0]:
                        x = secondPoint[0]
                    else:
                        x = point[0]
                else:
                    x = firstPoint[0] + (nth + 1) * (secondPoint[0] - firstPoint[0]) / (noArcs + 1.0)
            else:
                x = (secondPoint[0] - firstPoint[0]) / 2.0 # Midpoint
            y = pt1[1]
        else:
            assert RoughlyEqual(pt1[0], pt2[0])

            if pt1[1] > pt2[1]:
                firstPoint = pt2
                secondPoint = pt1
            else:
                firstPoint = pt1
                secondPoint = pt2

            if self._spaceAttachments:
                if line and line.GetAlignmentType(isEnd) == LINE_ALIGNMENT_TO_NEXT_HANDLE:
                    # Align line according to the next handle along
                    point = line.GetNextControlPoint(self)
                    if point[1] < firstPoint[1]:
                        y = firstPoint[1]
                    elif point[1] > secondPoint[1]:
                        y = secondPoint[1]
                    else:
                        y = point[1]
                else:
                    y = firstPoint[1] + (nth + 1) * (secondPoint[1] - firstPoint[1]) / (noArcs + 1.0)
            else:
                y = (secondPoint[1] - firstPoint[1]) / 2.0 # Midpoint
            x = pt1[0]

        return x, y

    # Return the zero-based position in m_lines of line
    def GetLinePosition(self, line):
        """Get the zero-based position of line in the list of lines
        for this shape.
        """
        try:
            return self._lines.index(line)
        except:
            return 0


    #            |________|
    #                 | <- root
    #                 | <- neck
    # shoulder1 ->---------<- shoulder2
    #             | | | | |
    #                      <- branching attachment point N-1

    def GetBranchingAttachmentInfo(self, attachment):
        """Get information about where branching connections go.
        
        Returns FALSE if there are no lines at this attachment.
        """
        physicalAttachment = self.LogicalToPhysicalAttachment(attachment)

        # Number of lines at this attachment
        lineCount = self.GetAttachmentLineCount(attachment)

        if not lineCount:
            return False

        totalBranchLength = self._branchSpacing * (lineCount - 1)
        root = self.GetBranchingAttachmentRoot(attachment)

        neck = wx.RealPoint()
        shoulder1 = wx.RealPoint()
        shoulder2 = wx.RealPoint()
        
        # Assume that we have attachment points 0 to 3: top, right, bottom, left
        if physicalAttachment == 0:
            neck[0] = self.x
            neck[1] = root[1] - self._branchNeckLength

            shoulder1[0] = root[0] - totalBranchLength / 2.0
            shoulder2[0] = root[0] + totalBranchLength / 2.0

            shoulder1[1] = neck[1]
            shoulder2[1] = neck[1]
        elif physicalAttachment == 1:
            neck[0] = root[0] + self._branchNeckLength
            neck[1] = root[1]
            
            shoulder1[0] = neck[0]
            shoulder2[0] = neck[0]

            shoulder1[1] = neck[1] - totalBranchLength / 2.0
            shoulder1[1] = neck[1] + totalBranchLength / 2.0
        elif physicalAttachment == 2:
            neck[0] = self.x
            neck[1] = root[1] + self._branchNeckLength

            shoulder1[0] = root[0] - totalBranchLength / 2.0
            shoulder2[0] = root[0] + totalBranchLength / 2.0

            shoulder1[1] = neck[1]
            shoulder2[1] = neck[1]
        elif physicalAttachment == 3:
            neck[0] = root[0] - self._branchNeckLength
            neck[1] = root[1]

            shoulder1[0] = neck[0]
            shoulder2[0] = neck[0]

            shoulder1[1] = neck[1] - totalBranchLength / 2.0
            shoulder2[1] = neck[1] + totalBranchLength / 2.0
        else:
            raise "Unrecognised attachment point in GetBranchingAttachmentInfo"
        return root, neck, shoulder1, shoulder2

    def GetBranchingAttachmentPoint(self, attachment, n):
        physicalAttachment = self.LogicalToPhysicalAttachment(attachment)

        root, neck, shoulder1, shoulder2 = self.GetBranchingAttachmentInfo(attachment)
        pt = wx.RealPoint()
        stemPt = wx.RealPoint()

        if physicalAttachment == 0:
            pt[1] = neck[1] - self._branchStemLength
            pt[0] = shoulder1[0] + n * self._branchSpacing

            stemPt[0] = pt[0]
            stemPt[1] = neck[1]
        elif physicalAttachment == 2:
            pt[1] = neck[1] + self._branchStemLength
            pt[0] = shoulder1[0] + n * self._branchStemLength
            
            stemPt[0] = pt[0]
            stemPt[1] = neck[1]
        elif physicalAttachment == 1:
            pt[0] = neck[0] + self._branchStemLength
            pt[1] = shoulder1[1] + n * self._branchSpacing

            stemPt[0] = neck[0]
            stemPt[1] = pt[1]
        elif physicalAttachment == 3:
            pt[0] = neck[0] - self._branchStemLength
            pt[1] = shoulder1[1] + n * self._branchSpacing

            stemPt[0] = neck[0]
            stemPt[1] = pt[1]
        else:
            raise "Unrecognised attachment point in GetBranchingAttachmentPoint"

        return pt, stemPt

    def GetAttachmentLineCount(self, attachment):
        """Get the number of lines at this attachment position."""
        count = 0
        for lineShape in self._lines:
            if lineShape.GetFrom() == self and lineShape.GetAttachmentFrom() == attachment:
                count += 1
            elif lineShape.GetTo() == self and lineShape.GetAttachmentTo() == attachment:
                count += 1
        return count
    
    def GetBranchingAttachmentRoot(self, attachment):
        """Get the root point at the given attachment."""
        physicalAttachment = self.LogicalToPhysicalAttachment(attachment)

        root = wx.RealPoint()

        width, height = self.GetBoundingBoxMax()

        # Assume that we have attachment points 0 to 3: top, right, bottom, left
        if physicalAttachment == 0:
            root[0] = self.x
            root[1] = self.y - height / 2.0
        elif physicalAttachment == 1:
            root[0] = self.x + width / 2.0
            root[1] = self.y
        elif physicalAttachment == 2:
            root[0] = self.x
            root[1] = self.y + height / 2.0
        elif physicalAttachment == 3:
            root[0] = self.x - width / 2.0
            root[1] = self.y
        else:
            raise "Unrecognised attachment point in GetBranchingAttachmentRoot"

        return root

    # Draw or erase the branches (not the actual arcs though)
    def OnDrawBranchesAttachment(self, dc, attachment, erase = False):

        count = self.GetAttachmentLineCount(attachment)
        if count == 0:
            return

        root, neck, shoulder1, shoulder2 = self.GetBranchingAttachmentInfo(attachment)

        if erase:
            dc.SetPen(wx.WHITE_PEN)
            dc.SetBrush(wx.WHITE_BRUSH)
        else:
            dc.SetPen(wx.BLACK_PEN)
            dc.SetBrush(wx.BLACK_BRUSH)

        # Draw neck
        dc.DrawLine(root[0], root[1], neck[0], neck[1])

        if count > 1:
            # Draw shoulder-to-shoulder line
            dc.DrawLine(shoulder1[0], shoulder1[1], shoulder2[0], shoulder2[1])
        # Draw all the little branches
        for i in range(count):
            pt, stemPt = self.GetBranchingAttachmentPoint(attachment, i)
            dc.DrawLine(stemPt[0], stemPt[1], pt[0], pt[1])

            if self.GetBranchStyle() & BRANCHING_ATTACHMENT_BLOB and count > 1:
                blobSize = 6.0
                dc.DrawEllipse(stemPt[0] - blobSize / 2.0, stemPt[1] - blobSize / 2.0, blobSize, blobSize)

    def OnDrawBranches(self, dc, erase = False):
        if self._attachmentMode != ATTACHMENT_MODE_BRANCHING:
            return
        for i in range(self.GetNumberOfAttachments()):
            self.OnDrawBranchesAttachment(dc, i, erase)

    def GetAttachmentPositionEdge(self, attachment, nth = 0, no_arcs = 1, line = None):
        """ Only get the attachment position at the _edge_ of the shape,
        ignoring branching mode. This is used e.g. to indicate the edge of
        interest, not the point on the attachment branch.
        """
        oldMode = self._attachmentMode

        # Calculate as if to edge, not branch
        if self._attachmentMode == ATTACHMENT_MODE_BRANCHING:
            self._attachmentMode = ATTACHMENT_MODE_EDGE
        res = self.GetAttachmentPosition(attachment, nth, no_arcs, line)
        self._attachmentMode = oldMode

        return res

    def PhysicalToLogicalAttachment(self, physicalAttachment):
        """ Rotate the standard attachment point from physical
        (0 is always North) to logical (0 -> 1 if rotated by 90 degrees)
        """
        if RoughlyEqual(self.GetRotation(), 0):
            i = physicalAttachment
        elif RoughlyEqual(self.GetRotation(), math.pi / 2.0):
            i = physicalAttachment - 1
        elif RoughlyEqual(self.GetRotation(), math.pi):
            i = physicalAttachment - 2
        elif RoughlyEqual(self.GetRotation(), 3 * math.pi / 2.0):
            i = physicalAttachment - 3
        else:
            # Can't handle -- assume the same
            return physicalAttachment

        if i < 0:
            i += 4

        return i

    def LogicalToPhysicalAttachment(self, logicalAttachment):
        """Rotate the standard attachment point from logical
        to physical (0 is always North).
        """
        if RoughlyEqual(self.GetRotation(), 0):
            i = logicalAttachment
        elif RoughlyEqual(self.GetRotation(), math.pi / 2.0):
            i = logicalAttachment + 1
        elif RoughlyEqual(self.GetRotation(), math.pi):
            i = logicalAttachment + 2
        elif RoughlyEqual(self.GetRotation(), 3 * math.pi / 2.0):
            i = logicalAttachment + 3
        else:
            return logicalAttachment

        if i > 3:
            i -= 4

        return i

    def Rotate(self, x, y, theta):
        """Rotate about the given axis by the given amount in radians."""
        self._rotation = theta
        if self._rotation < 0:
            self._rotation += 2 * math.pi
        elif self._rotation > 2 * math.pi:
            self._rotation -= 2 * math.pi

    def GetBackgroundPen(self):
        """Return pen of the right colour for the background."""
        if self.canvas:
            return wx.Pen(self.canvas.GetBackgroundColour(), 1, wx.SOLID)
        return WhiteBackgroundPen

    def GetBackgroundBrush(self):
        """Return brush of the right colour for the background."""
        if self.canvas:
            return wx.Brush(self.canvas.GetBackgroundColour(), wx.SOLID)
        return WhiteBackgroundBrush

    def GetParent(self):
        """Return the parent of this shape, if it is part of a composite."""
        return self._parent

    def SetParent(self, p):
        self._parent = p

    def GetChildren(self):
        """Return the list of children for this shape."""
        return self._children

    def GetDrawHandles(self):
        """Return the list of drawhandles."""
        return self._drawHandles

    def Recompute(self):
        """Recomputes any constraints associated with the shape.

        Normally applicable to CompositeShapes only, but harmless for
        other classes of Shape.
        """
        return True

    def IsHighlighted(self):
        """TRUE if the shape is highlighted. Shape highlighting is unimplemented."""
        return self._highlighted

    def GetSensitivityFilter(self):
        """Return the sensitivity filter, a bitlist of values.

        See Shape.SetSensitivityFilter.
        """
        return self._sensitivity

    def SetFixedSize(self, x, y):
        """Set the shape to be fixed size."""
        self._fixedWidth = x
        self._fixedHeight = y

    def GetFixedSize(self):
        """Return flags indicating whether the shape is of fixed size in
        either direction.
        """
        return self._fixedWidth, self._fixedHeight

    def GetFixedWidth(self):
        """TRUE if the shape cannot be resized in the horizontal plane."""
        return self._fixedWidth

    def GetFixedHeight(self):
        """TRUE if the shape cannot be resized in the vertical plane."""
        return self._fixedHeight
    
    def SetSpaceAttachments(self, sp):
        """Indicate whether lines should be spaced out evenly at the point
        they touch the node (sp = True), or whether they should join at a single
        point (sp = False).
        """
        self._spaceAttachments = sp

    def GetSpaceAttachments(self):
        """Return whether lines should be spaced out evenly at the point they
        touch the node (True), or whether they should join at a single point
        (False).
        """
        return self._spaceAttachments

    def SetCentreResize(self, cr):
        """Specify whether the shape is to be resized from the centre (the
        centre stands still) or from the corner or side being dragged (the
        other corner or side stands still).
        """
        self._centreResize = cr

    def GetCentreResize(self):
        """TRUE if the shape is to be resized from the centre (the centre stands
        still), or FALSE if from the corner or side being dragged (the other
        corner or side stands still)
        """
        return self._centreResize

    def SetMaintainAspectRatio(self, ar):
        """Set whether a shape that resizes should not change the aspect ratio
        (width and height should be in the original proportion).
        """
        self._maintainAspectRatio = ar

    def GetMaintainAspectRatio(self):
        """TRUE if shape keeps aspect ratio during resize."""
        return self._maintainAspectRatio

    def GetLines(self):
        """Return the list of lines connected to this shape."""
        return self._lines

    def SetDisableLabel(self, flag):
        """Set flag to TRUE to stop the default region being shown."""
        self._disableLabel = flag

    def GetDisableLabel(self):
        """TRUE if the default region will not be shown, FALSE otherwise."""
        return self._disableLabel

    def SetAttachmentMode(self, mode):
        """Set the attachment mode.

        If TRUE, attachment points will be significant when drawing lines to
        and from this shape.
        If FALSE, lines will be drawn as if to the centre of the shape.
        """
        self._attachmentMode = mode

    def GetAttachmentMode(self):
        """Return the attachment mode.

        See Shape.SetAttachmentMode.
        """
        return self._attachmentMode


    def IsShown(self):
        """TRUE if the shape is in a visible state, FALSE otherwise.

        Note that this has nothing to do with whether the window is hidden
        or the shape has scrolled off the canvas; it refers to the internal
        visibility flag.
        """
        return self._visible

    def GetPen(self):
        """Return the pen used for drawing the shape's outline."""
        return self._pen

    def GetBrush(self):
        """Return the brush used for filling the shape."""
        return self._brush

    def GetNumberOfTextRegions(self):
        """Return the number of text regions for this shape."""
        return len(self._regions)

    def GetRegions(self):
        """Return the list of ShapeRegions."""
        return self._regions

    # Control points ('handles') redirect control to the actual shape, to
    # make it easier to override sizing behaviour.
    def OnSizingDragLeft(self, pt, draw, x, y, keys = 0, attachment = 0):
        bound_x, bound_y = self.GetBoundingBoxMin()

        if self.GetCentreResize():
            # Maintain the same centre point
            new_width = 2.0 * abs(x - self.x)
            new_height = 2.0 * abs(y - self.y)

            # Constrain sizing according to what control point you're dragging
            if pt._type == CONTROL_POINT_HORIZONTAL:
                if self.GetMaintainAspectRatio():
                    new_height = bound_y * (new_width / bound_x)
                else:
                    new_height = bound_y
            elif pt._type == CONTROL_POINT_VERTICAL:
                if self.GetMaintainAspectRatio():
                    new_width = bound_x * (new_height / bound_y)
                else:
                    new_width = bound_x
            elif pt._type == CONTROL_POINT_DIAGONAL and (keys & KEY_SHIFT):
                new_height = bound_y * (new_width / bound_x)

            if self.GetFixedWidth():
                new_width = bound_x

            if self.GetFixedHeight():
                new_height = bound_y

            pt._controlPointDragEndWidth = new_width
            pt._controlPointDragEndHeight = new_height

            self.handler.OnDrawOutline(self.x, self.y, new_width, new_height)
        else:
            # Don't maintain the same centre point
            newX1 = min(pt._controlPointDragStartX, x)
            newY1 = min(pt._controlPointDragStartY, y)
            newX2 = max(pt._controlPointDragStartX, x)
            newY2 = max(pt._controlPointDragStartY, y)
            if pt._type == CONTROL_POINT_HORIZONTAL:
                newY1 = pt._controlPointDragStartY
                newY2 = newY1 + pt._controlPointDragStartHeight
            elif pt._type == CONTROL_POINT_VERTICAL:
                newX1 = pt._controlPointDragStartX
                newX2 = newX1 + pt._controlPointDragStartWidth
            elif pt._type == CONTROL_POINT_DIAGONAL and (keys & KEY_SHIFT or self.GetMaintainAspectRatio()):
                newH = (newX2 - newX1) * (float(pt._controlPointDragStartHeight) / pt._controlPointDragStartWidth)
                if self.y > pt._controlPointDragStartY:
                    newY2 = newY1 + newH
                else:
                    newY1 = newY2 - newH

            newWidth = float(newX2 - newX1)
            newHeight = float(newY2 - newY1)

            if pt._type == CONTROL_POINT_VERTICAL and self.GetMaintainAspectRatio():
                newWidth = bound_x * (newHeight / bound_y)

            if pt._type == CONTROL_POINT_HORIZONTAL and self.GetMaintainAspectRatio():
                newHeight = bound_y * (newWidth / bound_x)

            pt._controlPointDragPosX = newX1 + newWidth / 2.0
            pt._controlPointDragPosY = newY1 + newHeight / 2.0
            if self.GetFixedWidth():
                newWidth = bound_x

            if self.GetFixedHeight():
                newHeight = bound_y

            pt._controlPointDragEndWidth = newWidth
            pt._controlPointDragEndHeight = newHeight
            self.handler.OnDrawOutline(pt._controlPointDragPosX, pt._controlPointDragPosY, newWidth, newHeight)

    def OnSizingBeginDragLeft(self, pt, x, y, keys = 0, attachment = 0):
        self.canvas.CaptureMouse()

        bound_x, bound_y = self.GetBoundingBoxMin()
        self.handler.OnBeginSize(bound_x, bound_y)

        # Choose the 'opposite corner' of the object as the stationary
        # point in case this is non-centring resizing.
        if pt.x < self.x:
            pt._controlPointDragStartX = self.x + bound_x / 2.0
        else:
            pt._controlPointDragStartX = self.x - bound_x / 2.0

        if pt.y < self.y:
            pt._controlPointDragStartY = self.y + bound_y / 2.0
        else:
            pt._controlPointDragStartY = self.y - bound_y / 2.0

        if pt._type == CONTROL_POINT_HORIZONTAL:
            pt._controlPointDragStartY = self.y - bound_y / 2.0
        elif pt._type == CONTROL_POINT_VERTICAL:
            pt._controlPointDragStartX = self.x - bound_x / 2.0

        # We may require the old width and height
        pt._controlPointDragStartWidth = bound_x
        pt._controlPointDragStartHeight = bound_y

        if self.GetCentreResize():
            new_width = 2.0 * abs(x - self.x)
            new_height = 2.0 * abs(y - self.y)

            # Constrain sizing according to what control point you're dragging
            if pt._type == CONTROL_POINT_HORIZONTAL:
                if self.GetMaintainAspectRatio():
                    new_height = bound_y * (new_width / bound_x)
                else:
                    new_height = bound_y
            elif pt._type == CONTROL_POINT_VERTICAL:
                if self.GetMaintainAspectRatio():
                    new_width = bound_x * (new_height / bound_y)
                else:
                    new_width = bound_x
            elif pt._type == CONTROL_POINT_DIAGONAL and (keys & KEY_SHIFT):
                new_height = bound_y * (new_width / bound_x)

            if self.GetFixedWidth():
                new_width = bound_x

            if self.GetFixedHeight():
                new_height = bound_y

            pt._controlPointDragEndWidth = new_width
            pt._controlPointDragEndHeight = new_height
            self.handler.OnDrawOutline(self.x, self.y, new_width, new_height)
        else:
            # Don't maintain the same centre point
            newX1 = min(pt._controlPointDragStartX, x)
            newY1 = min(pt._controlPointDragStartY, y)
            newX2 = max(pt._controlPointDragStartX, x)
            newY2 = max(pt._controlPointDragStartY, y)
            if pt._type == CONTROL_POINT_HORIZONTAL:
                newY1 = pt._controlPointDragStartY
                newY2 = newY1 + pt._controlPointDragStartHeight
            elif pt._type == CONTROL_POINT_VERTICAL:
                newX1 = pt._controlPointDragStartX
                newX2 = newX1 + pt._controlPointDragStartWidth
            elif pt._type == CONTROL_POINT_DIAGONAL and (keys & KEY_SHIFT or self.GetMaintainAspectRatio()):
                newH = (newX2 - newX1) * (float(pt._controlPointDragStartHeight) / pt._controlPointDragStartWidth)
                if pt.y > pt._controlPointDragStartY:
                    newY2 = newY1 + newH
                else:
                    newY1 = newY2 - newH

            newWidth = float(newX2 - newX1)
            newHeight = float(newY2 - newY1)

            if pt._type == CONTROL_POINT_VERTICAL and self.GetMaintainAspectRatio():
                newWidth = bound_x * (newHeight / bound_y)

            if pt._type == CONTROL_POINT_HORIZONTAL and self.GetMaintainAspectRatio():
                newHeight = bound_y * (newWidth / bound_x)

            pt._controlPointDragPosX = newX1 + newWidth / 2.0
            pt._controlPointDragPosY = newY1 + newHeight / 2.0
            if self.GetFixedWidth():
                newWidth = bound_x

            if self.GetFixedHeight():
                newHeight = bound_y

            pt._controlPointDragEndWidth = newWidth
            pt._controlPointDragEndHeight = newHeight
            self.handler.OnDrawOutline(pt._controlPointDragPosX, pt._controlPointDragPosY, newWidth, newHeight)
            
    def OnSizingEndDragLeft(self, pt, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        if self.canvas.HasCapture():
            self.canvas.ReleaseMouse()
        dc.SetLogicalFunction(wx.COPY)
        self.Recompute()
        self.ResetControlPoints()

        self.Erase(dc)

        self.SetSize(pt._controlPointDragEndWidth, pt._controlPointDragEndHeight)

        # The next operation could destroy this control point (it does for
        # label objects, via formatting the text), so save all values we're
        # going to use, or we'll be accessing garbage.

        #return

        if self.GetCentreResize():
            self.Move(dc, self.x, self.y)
        else:
            self.Move(dc, pt._controlPointDragPosX, pt._controlPointDragPosY)

        # Recursively redraw links if we have a composite
        if len(self.GetChildren()):
            self.DrawLinks(dc, -1, True)

        width, height = self.GetBoundingBoxMax()
        self.handler.OnEndSize(width, height)

        if pt._eraseObject:
            self.canvas.quickRedraw(dc)


            
class RectangleShape(Shape):
    """
    The wxRectangleShape has rounded or square corners.

    Derived from:
      Shape
    """
    def __init__(self, w = 0.0, h = 0.0):
        Shape.__init__(self)
        self.w = w
        self.h = h
        self._cornerRadius = 0.0
        self.SetDefaultRegionSize()

    def OnDraw(self, dc):
        x1 = self.x - self.w / 2.0
        y1 = self.y - self.h / 2.0

        if self._shadowMode != SHADOW_NONE:
            if self._shadowBrush:
                dc.SetBrush(self._shadowBrush)
            dc.SetPen(TransparentPen)

            if self._cornerRadius:
                dc.DrawRoundedRectangle(x1 + self._shadowOffsetX, y1 + self._shadowOffsetY, self.w, self.h, self._cornerRadius)
            else:
                dc.DrawRectangle(x1 + self._shadowOffsetX,
                                 y1 + self._shadowOffsetY,
                                 self.w, self.h)

        if self._pen:
            if self._pen.GetWidth() == 0:
                dc.SetPen(TransparentPen)
            else:
                dc.SetPen(self._pen)
        if self._brush:
            dc.SetBrush(self._brush)

        if self._cornerRadius:
            dc.DrawRoundedRectangle(x1, y1, self.w, self.h, self._cornerRadius)
        else:
            dc.DrawRectangle(x1, y1, self.w, self.h)

    def GetBoundingBoxMin(self):
        return self.w, self.h

    def SetSize(self, x, y, recursive = False):
        self.SetAttachmentSize(x, y)
        self.w = max(x, 1)
        self.h = max(y, 1)
        self.SetDefaultRegionSize()

    def GetCornerRadius(self):
        """Get the radius of the rectangle's rounded corners."""
        return self._cornerRadius
    
    def SetCornerRadius(self, rad):
        """Set the radius of the rectangle's rounded corners.

        If the radius is zero, a non-rounded rectangle will be drawn.
        If the radius is negative, the value is the proportion of the smaller
        dimension of the rectangle.
        """
        self._cornerRadius = rad

    # Assume (x1, y1) is centre of box (most generally, line end at box)
    def GetPerimeterPoint(self, x1, y1, x2, y2):
        bound_x, bound_y = self.GetBoundingBoxMax()
        return FindEndForBox(bound_x, bound_y, self.x, self.y, x2, y2)

    def SetWidth(self, w):
        self.w = w

    def SetHeight(self, h):
        self.h = h


        
class PolygonShape(Shape):
    """A PolygonShape's shape is defined by a number of points passed to
    the object's constructor. It can be used to create new shapes such as
    diamonds and triangles.
    """
    def __init__(self):
        Shape.__init__(self)
        
        self._points = None
        self._originalPoints = None

    def Create(self, the_points = None):
        """Takes a list of wx.RealPoints or tuples; each point is an offset
        from the centre.
        """
        self.ClearPoints()

        if not the_points:
            self._originalPoints = []
            self._points = []
        else:
            self._originalPoints = the_points

            # Duplicate the list of points
            self._points = []
            for point in the_points:
                new_point = wx.Point(point[0], point[1])
                self._points.append(new_point)
            self.CalculateBoundingBox()
            self._originalWidth = self._boundWidth
            self._originalHeight = self._boundHeight
            self.SetDefaultRegionSize()

    def ClearPoints(self):
        self._points = []
        self._originalPoints = []

    # Width and height. Centre of object is centre of box
    def GetBoundingBoxMin(self):
        return self._boundWidth, self._boundHeight

    def GetPoints(self):
        """Return the internal list of polygon vertices."""
        return self._points

    def GetOriginalPoints(self):
        return self._originalPoints

    def GetOriginalWidth(self):
        return self._originalWidth

    def GetOriginalHeight(self):
        return self._originalHeight

    def SetOriginalWidth(self, w):
        self._originalWidth = w

    def SetOriginalHeight(self, h):
        self._originalHeight = h
        
    def CalculateBoundingBox(self):
        # Calculate bounding box at construction (and presumably resize) time
        left = 10000
        right = -10000
        top = 10000
        bottom = -10000

        for point in self._points:
            if point[0] < left:
                left = point[0]
            if point[0] > right:
                right = point[0]

            if point[1] < top:
                top = point[1]
            if point[1] > bottom:
                bottom = point[1]

        self._boundWidth = right - left
        self._boundHeight = bottom - top

    def CalculatePolygonCentre(self):
        """Recalculates the centre of the polygon, and
        readjusts the point offsets accordingly.
        Necessary since the centre of the polygon
        is expected to be the real centre of the bounding
        box.
        """
        left = 10000
        right = -10000
        top = 10000
        bottom = -10000

        for point in self._points:
            if point[0] < left:
                left = point[0]
            if point[0] > right:
                right = point[0]

            if point[1] < top:
                top = point[1]
            if point[1] > bottom:
                bottom = point[1]

        bwidth = right - left
        bheight = bottom - top

        newCentreX = left + bwidth / 2.0
        newCentreY = top + bheight / 2.0

        for i in range(len(self._points)):
            self._points[i] = self._points[i][0] - newCentreX, self._points[i][1] - newCentreY
        self.x += newCentreX
        self.y += newCentreY

    def HitTest(self, x, y):
        # Imagine four lines radiating from this point. If all of these lines
        # hit the polygon, we're inside it, otherwise we're not. Obviously
        # we'd need more radiating lines to be sure of correct results for
        # very strange (concave) shapes.
        endPointsX = [x, x + 1000, x, x - 1000]
        endPointsY = [y - 1000, y, y + 1000, y]

        xpoints = []
        ypoints = []

        for point in self._points:
            xpoints.append(point[0] + self.x)
            ypoints.append(point[1] + self.y)

        # We assume it's inside the polygon UNLESS one or more
        # lines don't hit the outline.
        isContained = True

        for i in range(4):
            if not PolylineHitTest(xpoints, ypoints, x, y, endPointsX[i], endPointsY[i]):
                isContained = False

        if not isContained:
            return False

        nearest_attachment = 0

        # If a hit, check the attachment points within the object
        nearest = 999999

        for i in range(self.GetNumberOfAttachments()):
            e = self.GetAttachmentPositionEdge(i)
            if e:
                xp, yp = e
                l = math.sqrt((xp - x) * (xp - x) + (yp - y) * (yp - y))
                if l < nearest:
                    nearest = l
                    nearest_attachment = i

        return nearest_attachment, nearest

    # Really need to be able to reset the shape! Otherwise, if the
    # points ever go to zero, we've lost it, and can't resize.
    def SetSize(self, new_width, new_height, recursive = True):
        self.SetAttachmentSize(new_width, new_height)

        # Multiply all points by proportion of new size to old size
        x_proportion = abs(float(new_width) / self._originalWidth)
        y_proportion = abs(float(new_height) / self._originalHeight)

        for i in range(max(len(self._points), len(self._originalPoints))):
            self._points[i] = wx.Point(self._originalPoints[i][0] * x_proportion, self._originalPoints[i][1] * y_proportion)

        self._boundWidth = abs(new_width)
        self._boundHeight = abs(new_height)
        self.SetDefaultRegionSize()

    # Make the original points the same as the working points
    def UpdateOriginalPoints(self):
        """If we've changed the shape, must make the original points match the
        working points with this function.
        """
        self._originalPoints = []

        for point in self._points:
            original_point = wx.RealPoint(point[0], point[1])
            self._originalPoints.append(original_point)

        self.CalculateBoundingBox()
        self._originalWidth = self._boundWidth
        self._originalHeight = self._boundHeight

    def AddPolygonPoint(self, pos):
        """Add a control point after the given point."""
        try:
            firstPoint = self._points[pos]
        except ValueError:
            firstPoint = self._points[0]

        try:
            secondPoint = self._points[pos + 1]
        except ValueError:
            secondPoint = self._points[0]

        x = (secondPoint[0] - firstPoint[0]) / 2.0 + firstPoint[0]
        y = (secondPoint[1] - firstPoint[1]) / 2.0 + firstPoint[1]
        point = wx.RealPoint(x, y)

        if pos >= len(self._points) - 1:
            self._points.append(point)
        else:
            self._points.insert(pos + 1, point)

        self.UpdateOriginalPoints()

        if self._selected:
            self.DeleteControlPoints()
            self.MakeControlPoints()

    def DeletePolygonPoint(self, pos):
        """Delete the given control point."""
        if pos < len(self._points):
            del self._points[pos]
            self.UpdateOriginalPoints()
            if self._selected:
                self.DeleteControlPoints()
                self.MakeControlPoints()

    # Assume (x1, y1) is centre of box (most generally, line end at box)
    def GetPerimeterPoint(self, x1, y1, x2, y2):
        # First check for situation where the line is vertical,
        # and we would want to connect to a point on that vertical --
        # oglFindEndForPolyline can't cope with this (the arrow
        # gets drawn to the wrong place).
        if self._attachmentMode == ATTACHMENT_MODE_NONE and x1 == x2:
            # Look for the point we'd be connecting to. This is
            # a heuristic...
            for point in self._points:
                if point[0] == 0:
                    if y2 > y1 and point[1] > 0:
                        return point[0] + self.x, point[1] + self.y
                    elif y2 < y1 and point[1] < 0:
                        return point[0] + self.x, point[1] + self.y

        xpoints = []
        ypoints = []
        for point in self._points:
            xpoints.append(point[0] + self.x)
            ypoints.append(point[1] + self.y)

        return FindEndForPolyline(xpoints, ypoints, x1, y1, x2, y2)

    def OnDraw(self, dc):
        if self._shadowMode != SHADOW_NONE:
            if self._shadowBrush:
                dc.SetBrush(self._shadowBrush)
            dc.SetPen(TransparentPen)
            dc.DrawPolygon(self._points, self.x + self._shadowOffsetX,
                           self.y, self._shadowOffsetY)
        if self._pen:
            if self._pen.GetWidth() == 0:
                dc.SetPen(TransparentPen)
            else:
                dc.SetPen(self._pen)
        if self._brush:
            dc.SetBrush(self._brush)
        dc.DrawPolygon(self._points, self.x, self.y)

    def draw(self, canvas):
        pass

    def OnDrawOutline(self, x, y, w, h):
        dc = self.buildOutlineDC()

        # Multiply all points by proportion of new size to old size
        x_proportion = abs(float(w) / self._originalWidth)
        y_proportion = abs(float(h) / self._originalHeight)

        intPoints = []
        for point in self._originalPoints:
            intPoints.append(wx.Point(x_proportion * point[0],
                                      y_proportion * point[1]))
        dc.DrawPolygon(intPoints, x, y)

    # Make as many control points as there are vertices
    def MakeControlPoints(self):
        for point in self._points:
            control = PolygonControlPoint(self.canvas, self,
                                          CONTROL_POINT_SIZE,
                                          point, point[0], point[1])
            self.canvas.AddShape(control)
            self._controlPoints.append(control)

    def ResetControlPoints(self):
        for i in range(min(len(self._points), len(self._controlPoints))):
            point = self._points[i]
            self._controlPoints[i].xoffset = point[0]
            self._controlPoints[i].yoffset = point[1]
            self._controlPoints[i].polygonVertex = point

    def GetNumberOfAttachments(self):
        maxN = max(len(self._points) - 1, 0)
        for point in self._attachmentPoints:
            if point.id > maxN:
                maxN = point.id
        return maxN + 1

    def GetAttachmentPosition(self, attachment, nth = 0, no_arcs = 1, line = None):
        if self._attachmentMode == ATTACHMENT_MODE_EDGE and self._points and attachment < len(self._points):
            point = self._points[0]
            return point[0] + self.x, point[1] + self.y
        return Shape.GetAttachmentPosition(self, attachment, nth, no_arcs, line)

    def AttachmentIsValid(self, attachment):
        if not self._points:
            return False

        if attachment >= 0 and attachment < len(self._points):
            return True

        for point in self._attachmentPoints:
            if point.id == attachment:
                return True

        return False

    # Rotate about the given axis by the given amount in radians
    def Rotate(self, x, y, theta):
        actualTheta = theta - self._rotation

        # Rotate attachment points
        sinTheta = math.sin(actualTheta)
        cosTheta = math.cos(actualTheta)

        for point in self._attachmentPoints:
            x1 = point.x
            y1 = point.y

            point.x = x1 * cosTheta - y1 * sinTheta + x * (1 - cosTheta) + y * sinTheta
            point.y = x1 * sinTheta + y1 * cosTheta + y * (1 - cosTheta) + x * sinTheta

        for i in range(len(self._points)):
            x1, y1 = self._points[i]

            self._points[i] = x1 * cosTheta - y1 * sinTheta + x * (1 - cosTheta) + y * sinTheta, x1 * sinTheta + y1 * cosTheta + y * (1 - cosTheta) + x * sinTheta

        for i in range(len(self._originalPoints)):
            x1, y1 = self._originalPoints[i]

            self._originalPoints[i] = x1 * cosTheta - y1 * sinTheta + x * (1 - cosTheta) + y * sinTheta, x1 * sinTheta + y1 * cosTheta + y * (1 - cosTheta) + x * sinTheta

        # Added by Pierre Hj�lm. If we don't do this the outline will be
        # the wrong size. Hopefully it won't have any ill effects.
        self.UpdateOriginalPoints()
        
        self._rotation = theta

        self.CalculatePolygonCentre()
        self.CalculateBoundingBox()
        self.ResetControlPoints()

    # Control points ('handles') redirect control to the actual shape, to
    # make it easier to override sizing behaviour.
    def OnSizingDragLeft(self, pt, draw, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        dc.SetLogicalFunction(OGLRBLF)

        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        # Code for CTRL-drag in C++ version commented out
        
        pt.CalculateNewSize(x, y)

        self.handler.OnDrawOutline(self.x, self.y, pt.GetNewSize()[0], pt.GetNewSize()[1])

    def OnSizingBeginDragLeft(self, pt, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        self.Erase(dc)
        
        dc.SetLogicalFunction(OGLRBLF)

        bound_x, bound_y = self.GetBoundingBoxMin()

        dist = math.sqrt((x - self.x) * (x - self.x) + (y - self.y) * (y - self.y))

        pt._originalDistance = dist
        pt._originalSize[0] = bound_x
        pt._originalSize[1] = bound_y

        if pt._originalDistance == 0:
            pt._originalDistance = 0.0001

        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        # Code for CTRL-drag in C++ version commented out

        pt.CalculateNewSize(x, y)

        self.handler.OnDrawOutline(self.x, self.y, pt.GetNewSize()[0], pt.GetNewSize()[1])

        self.canvas.CaptureMouse()

    def OnSizingEndDragLeft(self, pt, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        if self.canvas.HasCapture():
            self.canvas.ReleaseMouse()
        dc.SetLogicalFunction(wx.COPY)

        # If we're changing shape, must reset the original points
        if keys & KEY_CTRL:
            self.CalculateBoundingBox()
            self.CalculatePolygonCentre()
        else:
            self.SetSize(pt.GetNewSize()[0], pt.GetNewSize()[1])

        self.Recompute()
        self.ResetControlPoints()
        self.Move(dc, self.x, self.y)

        self.canvas.quickRedraw(dc)



class EllipseShape(Shape):
    """The EllipseShape behaves similarly to the RectangleShape but is
    elliptical.

    Derived from:
      wxShape
    """
    def __init__(self, w, h):
        Shape.__init__(self)
        self.w = w
        self.h = h
        self.SetDefaultRegionSize()

    def GetBoundingBoxMin(self):
        return self.w, self.h

    def GetPerimeterPoint(self, x1, y1, x2, y2):
        bound_x, bound_y = self.GetBoundingBoxMax()

        return DrawArcToEllipse(self.x, self.y, bound_x, bound_y, x2, y2, x1, y1)
    def SetWidth(self, w):
        self.w = w

    def SetHeight(self, h):
        self.h = h
        
    def OnDraw(self, dc):
                
        if self._shadowMode != SHADOW_NONE:
            if self._shadowBrush:
                dc.SetBrush(self._shadowBrush)
            dc.SetPen(TransparentPen)
            dc.DrawEllipse(self.x - self.w / 2.0 + self._shadowOffsetX,
                           self.y - self.h / 2.0 + self._shadowOffsetY,
                           self.w, self.h)

        if self._pen:
            if self._pen.GetWidth() == 0:
                dc.SetPen(TransparentPen)
            else:
                dc.SetPen(self._pen)
        if self._brush:
            dc.SetBrush(self._brush)
        dc.DrawEllipse(self.x - self.w / 2.0, self.y - self.h / 2.0, self.w
                       , self.h)

    def SetSize(self, x, y, recursive = True):
        self.SetAttachmentSize(x, y)
        self.w = x
        self.h = y
        self.SetDefaultRegionSize()

    def GetNumberOfAttachments(self):
        return Shape.GetNumberOfAttachments(self)

    # There are 4 attachment points on an ellipse - 0 = top, 1 = right,
    # 2 = bottom, 3 = left.
    def GetAttachmentPosition(self, attachment, nth = 0, no_arcs = 1, line = None):
        if self._attachmentMode == ATTACHMENT_MODE_BRANCHING:
            return Shape.GetAttachmentPosition(self, attachment, nth, no_arcs, line)

        if self._attachmentMode != ATTACHMENT_MODE_NONE:
            top = self.y + self.h / 2.0
            bottom = self.y - self.h / 2.0
            left = self.x - self.w / 2.0
            right = self.x + self.w / 2.0

            physicalAttachment = self.LogicalToPhysicalAttachment(attachment)

            if physicalAttachment == 0:
                if self._spaceAttachments:
                    x = left + (nth + 1) * self.w / (no_arcs + 1.0)
                else:
                    x = self.x
                y = top
                # We now have the point on the bounding box: but get the point
                # on the ellipse by imagining a vertical line from
                # (x, self.y - self.h - 500) to (x, self.y) intersecting
                # the ellipse.

                return DrawArcToEllipse(self.x, self.y, self.w, self.h, x, self.y - self.h - 500, x, self.y)
            elif physicalAttachment == 1:
                x = right
                if self._spaceAttachments:
                    y = bottom + (nth + 1) * self.h / (no_arcs + 1.0)
                else:
                    y = self.y
                return DrawArcToEllipse(self.x, self.y, self.w, self.h, self.x + self.w + 500, y, self.x, y)
            elif physicalAttachment == 2:
                if self._spaceAttachments:
                    x = left + (nth + 1) * self.w / (no_arcs + 1.0)
                else:
                    x = self.x
                y = bottom
                return DrawArcToEllipse(self.x, self.y, self.w, self.h, x, self.y + self.h + 500, x, self.y)
            elif physicalAttachment == 3:
                x = left
                if self._spaceAttachments:
                    y = bottom + (nth + 1) * self.h / (no_arcs + 1.0)
                else:
                    y = self.y
                return DrawArcToEllipse(self.x, self.y, self.w, self.h, self.x - self.w - 500, y, self.x, y)
            else:
                return Shape.GetAttachmentPosition(self, attachment, x, y, nth, no_arcs, line)
        else:
            return self.x, self.y



class CircleShape(EllipseShape):
    """An EllipseShape whose width and height are the same."""
    def __init__(self, diameter):
        EllipseShape.__init__(self, diameter, diameter)
        self.SetMaintainAspectRatio(True)

    def GetPerimeterPoint(self, x1, y1, x2, y2):
        return FindEndForCircle(self.w / 2.0, self.x, self.y, x2, y2)



class TextShape(RectangleShape):
    """As wxRectangleShape, but only the text is displayed."""
    def __init__(self, width, height):
        RectangleShape.__init__(self, width, height)

    def OnDraw(self, dc):
        pass



class ShapeRegion(object):
    """Object region."""
    def __init__(self, region = None):
        if region:
            self._regionText = region._regionText
            self._regionName = region._regionName
            self._textColour = region._textColour

            self._font = region._font
            self._minHeight = region._minHeight
            self._minWidth = region._minWidth
            self.w = region.w
            self.h = region.h
            self.x = region.x
            self.y = region.y

            self._regionProportionX = region._regionProportionX
            self._regionProportionY = region._regionProportionY
            self._formatMode = region._formatMode
            self._actualColourObject = region._actualColourObject
            self._actualPenObject = None
            self._penStyle = region._penStyle
            self._penColour = region._penColour

            self.ClearText()
            for line in region._formattedText:
                new_line = ShapeTextLine(line.x, line.y, line.GetText())
                self._formattedText.append(new_line)
        else:
            self._regionText = ""
            self._font = NormalFont
            self._minHeight = 5.0
            self._minWidth = 5.0
            self.w = 0.0
            self.h = 0.0
            self.x = 0.0
            self.y = 0.0

            self._regionProportionX = -1.0
            self._regionProportionY = -1.0
            self._formatMode = FORMAT_CENTRE_HORIZ | FORMAT_CENTRE_VERT
            self._regionName = ""
            self._textColour = "BLACK"
            self._penColour = "BLACK"
            self._penStyle = wx.SOLID
            self._actualColourObject = wx.TheColourDatabase.Find("BLACK")
            self._actualPenObject = None

        self._formattedText = []

    def ClearText(self):
        self._formattedText = []

    def SetFont(self, f):
        self._font = f

    def SetMinSize(self, w, h):
        self._minWidth = w
        self._minHeight = h

    def SetSize(self, w, h):
        self.w = w
        self.h = h

    def SetPosition(self, xp, yp):
        self.x = xp
        self.y = yp

    def SetProportions(self, xp, yp):
        self._regionProportionX = xp
        self._regionProportionY = yp

    def SetFormatMode(self, mode):
        self._formatMode = mode

    def SetColour(self, col):
        self._textColour = col
        self._actualColourObject = col

    def GetActualColourObject(self):
        self._actualColourObject = wx.TheColourDatabase.Find(self.GetColour())
        return self._actualColourObject

    def SetPenColour(self, col):
        self._penColour = col
        self._actualPenObject = None

    # Returns NULL if the pen is invisible
    # (different to pen being transparent; indicates that
    # region boundary should not be drawn.)
    def GetActualPen(self):
        if self._actualPenObject:
            return self._actualPenObject

        if not self._penColour:
            return None
        if self._penColour=="Invisible":
            return None
        self._actualPenObject = wx.Pen(self._penColour, 1, self._penStyle)
        return self._actualPenObject

    def SetText(self, s):
        self._regionText = s

    def SetName(self, s):
        self._regionName = s

    def GetText(self):
        return self._regionText

    def GetFont(self):
        return self._font

    def GetMinSize(self):
        return self._minWidth, self._minHeight

    def GetProportion(self):
        return self._regionProportionX, self._regionProportionY

    def GetSize(self):
        return self.w, self.h

    def GetPosition(self):
        return self.x, self.y

    def GetFormatMode(self):
        return self._formatMode

    def GetName(self):
        return self._regionName

    def GetColour(self):
        return self._textColour

    def GetFormattedText(self):
        return self._formattedText

    def GetPenColour(self):
        return self._penColour

    def GetPenStyle(self):
        return self._penStyle

    def SetPenStyle(self, style):
        self._penStyle = style
        self._actualPenObject = None


class ControlPoint(RectangleShape):
    def __init__(self, theCanvas, object, size, the_xoffset, the_yoffset, the_type):
        RectangleShape.__init__(self, size, size)

        self.canvas = theCanvas
        self._shape = object
        self.xoffset = the_xoffset
        self.yoffset = the_yoffset
        self._type = the_type
        self.SetPen(BlackForegroundPen)
        self.SetBrush(wx.BLACK_BRUSH)
        self._oldCursor = None
        self._visible = True
        self._eraseObject = True
        
    # Don't even attempt to draw any text - waste of time
    def OnDrawContents(self, dc):
        pass

    def OnDraw(self, dc):
        self.x = self._shape.x + self.xoffset
        self.y = self._shape.y + self.yoffset
        RectangleShape.OnDraw(self, dc)

    def OnErase(self, dc):
        RectangleShape.OnErase(self, dc)

    # Implement resizing of canvas object
    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        self._shape.handler.OnSizingDragLeft(self, draw, x, y, keys, attachment)

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        self._shape.handler.OnSizingBeginDragLeft(self, x, y, keys, attachment)

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        self._shape.handler.OnSizingEndDragLeft(self, x, y, keys, attachment)

    def GetNumberOfAttachments(self):
        return 1

    def GetAttachmentPosition(self, attachment, nth = 0, no_arcs = 1, line = None):
        return self.x, self.y

    def SetEraseObject(self, er):
        self._eraseObject = er

        
class PolygonControlPoint(ControlPoint):
    def __init__(self, theCanvas, object, size, vertex, the_xoffset, the_yoffset):
        ControlPoint.__init__(self, theCanvas, object, size, the_xoffset, the_yoffset, 0)
        self._polygonVertex = vertex
        self._originalDistance = 0.0
        self._newSize = wx.RealPoint()
        self._originalSize = wx.RealPoint()

    def GetNewSize(self):
        return self._newSize
    
    # Calculate what new size would be, at end of resize
    def CalculateNewSize(self, x, y):
        bound_x, bound_y = self.shape.GetBoundingBoxMax()
        dist = math.sqrt((x - self._shape.x) * (x - self._shape.x) + (y - self._shape.y) * (y - self._shape.y))

        self._newSize[0] = dist / self._originalDistance * self._originalSize[0]
        self._newSize[1] = dist / self._originalDistance * self._originalSize[1]

    # Implement resizing polygon or moving the vertex
    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        self._shape.handler.OnSizingDragLeft(self, draw, x, y, keys, attachment)

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        self._shape.handler.OnSizingBeginDragLeft(self, x, y, keys, attachment)

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        self._shape.handler.OnSizingEndDragLeft(self, x, y, keys, attachment)

from lines import *
from composit import *
from canvas import *
