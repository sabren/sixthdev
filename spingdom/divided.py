# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------------
# Name:         divided.py
# Purpose:      DividedShape class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# RCS-ID:       $Id$
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
#----------------------------------------------------------------------------

import sys
import wx

from basic import ControlPoint, RectangleShape, Shape
from oglmisc import *



class DividedShapeControlPoint(ControlPoint):
    def __init__(self, the_canvas, object, region, size, the_m_xoffset, the_m_yoffset, the_type):
        ControlPoint.__init__(self, the_canvas, object, size, the_m_xoffset, the_m_yoffset, the_type)
        self.regionId = region

    # Implement resizing of divided object division
    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        dc.SetLogicalFunction(OGLRBLF)
        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dividedObject = self._shape
        x1 = dividedObject.x - dividedObject.w / 2.0
        y1 = y
        x2 = dividedObject.x + dividedObject.w / 2.0
        y2 = y

        dc.DrawLine(x1, y1, x2, y2)

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        dc.SetLogicalFunction(OGLRBLF)
        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dividedObject = self._shape
        
        x1 = dividedObject.x - dividedObject.w / 2.0
        y1 = y
        x2 = dividedObject.x + dividedObject.w / 2.0
        y2 = y

        dc.DrawLine(x1, y1, x2, y2)
        self.canvas.CaptureMouse()

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        dividedObject = self._shape
        if not dividedObject.GetRegions()[self.regionId]:
            return
        
        thisRegion = dividedObject.GetRegions()[self.regionId]
        nextRegion = None

        dc.SetLogicalFunction(wx.COPY)

        if self.canvas.HasCapture():
            self.canvas.ReleaseMouse()

        # Find the old top and bottom of this region,
        # and calculate the new proportion for this region
        # if legal.
        currentY = dividedObject.y - dividedObject.h / 2.0
        maxY = dividedObject.y + dividedObject.h / 2.0

        # Save values
        theRegionTop = 0
        nextRegionBottom = 0
        
        for i in range(len(dividedObject.GetRegions())):
            region = dividedObject.GetRegions()[i]
            proportion = region._regionProportionY
            yy = currentY + dividedObject.h * proportion
            actualY = min(maxY, yy)

            if region == thisRegion:
                thisRegionTop = currentY
                
                if i + 1 < len(dividedObject.GetRegions()):
                    nextRegion = dividedObject.GetRegions()[i + 1]
            if region == nextRegion:
                nextRegionBottom = actualY

            currentY = actualY

        if not nextRegion:
            return

        # Check that we haven't gone above this region or below
        # next region.
        if y <= thisRegionTop or y >= nextRegionBottom:
            return

        dividedObject.EraseLinks(dc)

        # Now calculate the new proportions of this region and the next region
        thisProportion = float(y - thisRegionTop) / dividedObject.h
        nextProportion = float(nextRegionBottom - y) / dividedObject.h

        thisRegion.SetProportions(0, thisProportion)
        nextRegion.SetProportions(0, nextProportion)
        self.yoffset = y - dividedObject.y

        # Now reformat text
        for i, region in enumerate(dividedObject.GetRegions()):
            if region.GetText():
                s = region.GetText()
                dividedObject.FormatText(dc, s, i)

        dividedObject.SetRegionSizes()
        dividedObject.Draw(dc)
        dividedObject.handler.OnMoveLinks(dc)


class DividedShape(RectangleShape):
    """A DividedShape is a rectangle with a number of vertical divisions.
    Each division may have its text formatted with independent characteristics,
    and the size of each division relative to the whole image may be specified.

    Derived from:
      RectangleShape
    """
    def __init__(self, w, h):
        RectangleShape.__init__(self, w, h)
        self.ClearRegions()

    def OnDraw(self, dc):
        RectangleShape.OnDraw(self, dc)

    def OnDrawContents(self, dc):
        if self.GetRegions():
            defaultProportion = 1.0 / len(self.GetRegions())
        else:
            defaultProportion = 0.0
        currentY = self.y - self.h / 2.0
        maxY = self.y + self.h / 2.0

        leftX = self.x - self.w / 2.0
        rightX = self.x + self.w / 2.0

        if self._pen:
            dc.SetPen(self._pen)

        dc.SetTextForeground(self._textColour)

        # For efficiency, don't do this under X - doesn't make
        # any visible difference for our purposes.
        if sys.platform[:3] == "win":
            dc.SetTextBackground(self._brush.GetColour())

        if self.GetDisableLabel():
            return

        xMargin = 2
        yMargin = 2

        dc.SetBackgroundMode(wx.TRANSPARENT)

        for region in self.GetRegions():
            dc.SetFont(region.GetFont())
            dc.SetTextForeground(region.GetActualColourObject())

            if region._regionProportionY < 0:
                proportion = defaultProportion
            else:
                proportion = region._regionProportionY

            y = currentY + self.h * proportion
            actualY = min(maxY, y)

            centreX = self.x
            centreY = currentY + (actualY - currentY) / 2.0

            DrawFormattedText(dc, region._formattedText, centreX, centreY, self.w - 2 * xMargin, actualY - currentY - 2 * yMargin, region._formatMode)

            if y <= maxY and region != self.GetRegions()[-1]:
                regionPen = region.GetActualPen()
                if regionPen:
                    dc.SetPen(regionPen)
                    dc.DrawLine(leftX, y, rightX, y)

            currentY = actualY

    def SetSize(self, w, h, recursive = True):
        self.SetAttachmentSize(w, h)
        self.w = w
        self.h = h
        self.SetRegionSizes()

    def SetRegionSizes(self):
        """Set all region sizes according to proportions and this object
        total size.
        """
        if not self.GetRegions():
            return

        if self.GetRegions():
            defaultProportion = 1.0 / len(self.GetRegions())
        else:
            defaultProportion = 0.0
        currentY = self.y - self.h / 2.0
        maxY = self.y + self.h / 2.0
        
        for region in self.GetRegions():
            if region._regionProportionY <= 0:
                proportion = defaultProportion
            else:
                proportion = region._regionProportionY

            sizeY = proportion * self.h
            y = currentY + sizeY
            actualY = min(maxY, y)

            centreY = currentY + (actualY - currentY) / 2.0

            region.SetSize(self.w, sizeY)
            region.SetPosition(0, centreY - self.y)

            currentY = actualY

    # Attachment points correspond to regions in the divided box
    def GetAttachmentPosition(self, attachment, nth = 0, no_arcs = 1, line = None):
        totalNumberAttachments = len(self.GetRegions()) * 2 + 2
        if self.GetAttachmentMode() == ATTACHMENT_MODE_NONE or attachment >= totalNumberAttachments:
            return Shape.GetAttachmentPosition(self, attachment, nth, no_arcs)

        n = len(self.GetRegions())
        isEnd = line and line.IsEnd(self)

        left = self.x - self.w / 2.0
        right = self.x + self.w / 2.0
        top = self.y - self.h / 2.0
        bottom = self.y + self.h / 2.0

        # Zero is top, n + 1 is bottom
        if attachment == 0:
            y = top
            if self._spaceAttachments:
                if line and line.GetAlignmentType(isEnd) == LINE_ALIGNMENT_TO_NEXT_HANDLE:
                    # Align line according to the next handle along
                    point = line.GetNextControlPoint(self)
                    if point[0] < left:
                        x = left
                    elif point[0] > right:
                        x = right
                    else:
                        x = point[0]
                else:
                    x = left + (nth + 1) * self.w / (no_arcs + 1.0)
            else:
                x = self.x
        elif attachment == n + 1:
            y = bottom
            if self._spaceAttachments:
                if line and line.GetAlignmentType(isEnd) == LINE_ALIGNMENT_TO_NEXT_HANDLE:
                    # Align line according to the next handle along
                    point = line.GetNextControlPoint(self)
                    if point[0] < left:
                        x = left
                    elif point[0] > right:
                        x = right
                    else:
                        x = point[0]
                else:
                    x = left + (nth + 1) * self.w / (no_arcs + 1.0)
            else:
                x = self.x
        else: # Left or right
            isLeft = not attachment < (n + 1)
            if isLeft:
                i = totalNumberAttachments - attachment - 1
            else:
                i = attachment - 1

            region = self.GetRegions()[i]
            if region:
                if isLeft:
                    x = left
                else:
                    x = right

                # Calculate top and bottom of region
                top = self.y + region.y - region.h / 2.0
                bottom = self.y + region.y + region.h / 2.0

                # Assuming we can trust the absolute size and
                # position of these regions
                if self._spaceAttachments:
                    if line and line.GetAlignmentType(isEnd) == LINE_ALIGNMENT_TO_NEXT_HANDLE:
                        # Align line according to the next handle along
                        point = line.GetNextControlPoint(self)
                        if point[1] < bottom:
                            y = bottom
                        elif point[1] > top:
                            y = top
                        else:
                            y = point[1]
                    else:
                        y = top + (nth + 1) * region.h / (no_arcs + 1.0)
                else:
                    y = self.y + region.y
            else:
                return False
        return x, y

    def GetNumberOfAttachments(self):
        # There are two attachments for each region (left and right),
        # plus one on the top and one on the bottom.
        n = len(self.GetRegions()) * 2 + 2

        maxN = n - 1
        for point in self._attachmentPoints:
            if point._id > maxN:
                maxN = point._id

        return maxN + 1

    def AttachmentIsValid(self, attachment):
        totalNumberAttachments = len(self.GetRegions()) * 2 + 2
        if attachment >= totalNumberAttachments:
            return Shape.AttachmentIsValid(self, attachment)
        else:
            return attachment >= 0

    def MakeControlPoints(self):
        RectangleShape.MakeControlPoints(self)
        self.MakeMandatoryControlPoints()

    def MakeMandatoryControlPoints(self):
        currentY = self.y - self.h / 2.0
        maxY = self.y + self.h / 2.0

        for i, region in enumerate(self.GetRegions()):
            proportion = region._regionProportionY

            y = currentY + self.h * proportion
            actualY = min(maxY, y)

            if region != self.GetRegions()[-1]:
                controlPoint = DividedShapeControlPoint(self.canvas, self, i, CONTROL_POINT_SIZE, 0, actualY - self.y, 0)
                self.canvas.AddShape(controlPoint)
                self._controlPoints.append(controlPoint)

            currentY = actualY

    def ResetControlPoints(self):
        # May only have the region handles, (n - 1) of them
        if len(self._controlPoints) > len(self.GetRegions()) - 1:
            RectangleShape.ResetControlPoints(self)

        self.ResetMandatoryControlPoints()

    def ResetMandatoryControlPoints(self):
        currentY = self.y - self.h / 2.0
        maxY = self.y + self.h / 2.0

        i = 0
        for controlPoint in self._controlPoints:
            if isinstance(controlPoint, DividedShapeControlPoint):
                region = self.GetRegions()[i]
                proportion = region._regionProportionY

                y = currentY + self.h * proportion
                actualY = min(maxY, y)

                controlPoint.xoffset = 0
                controlPoint.yoffset = actualY - self.y

                currentY = actualY

                i += 1
                
    def EditRegions(self):
        """Edit the region colours and styles. Not implemented."""
        print "EditRegions() is unimplemented"
        
    def OnRightClick(self, x, y, keys = 0, attachment = 0):
        if keys & KEY_CTRL:
            self.EditRegions()
        else:
            RectangleShape.OnRightClick(self, x, y, keys, attachment)
