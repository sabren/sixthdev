import unittest
from basic import ShapeEvtHandler
from narrative import testcase

"""
In wxOGL, the ShapeEvtHandler, which is the
parent class of Shape, had a zillion methods
that all looked about like this:

    def OnDraw(self, dc):
        if self._previousHandler:
            self._previousHandler.OnDraw(dc)

I believe this is so deeply nested shapes
can allow interaction to be handled by parent
shapes, and perhaps also it's meant to let you
chain or mix in event handlers.

I'm not sure I want to keep this scheme or not,
but I definitely want to get rid of all that
duplicate code, and replace it with a generic
proxy.

The first thing is to write some tests for the
current behavior. 
"""
@testcase
def test_previous_handlers(test):

    class EventEcho:
        def __init__(self):
            self.echo = []
        def __getattr__(self, method_name):
            """
            return a closure that looks like
            a method. when it gets called, it
            just records its arguments.
            """
            def f(*args, **kw):
                self.echo = [method_name, args, kw]
            return f

    def test_event(handler, event_name, *args, **kw):
        echo = EventEcho()
        handler_onEvent = getattr(handler, event_name)

        # Before setting previousHandler, firing off
        # an event should do nothing. But since I'm
        # replacing those ifs with NullEventHandler,
        # call the event anyway just to make sure it
        # doesn't crash.
        handler_onEvent(*args, **kw)

        # Once we set the previousHandler, though,
        # the handler should pass the event to it.
        handler.SetPreviousHandler(echo)
        handler_onEvent(*args, **kw)
        assert echo.echo == [event_name, args, kw], echo.echo

    hand = ShapeEvtHandler()
    dc = "dc"
    x = "x"
    y = "y"
    draw = "draw"
    test_event(hand, "OnDraw", dc)
    test_event(hand, "OnMoveLinks", dc)
    test_event(hand, "OnMoveLink", dc, moveControlPoints=True)
    test_event(hand, "OnDrawContents", dc)
    test_event(hand, "OnDrawBranches", dc, erase = False)
    test_event(hand, "OnSize", x, y)
    old_x = "old_x"
    old_y = "old_y"
    test_event(hand, "OnMovePre", dc, x, y, old_x, old_y, display = True)
    test_event(hand, "OnMovePost", dc, x, y, old_x, old_y, display = True)
    test_event(hand, "OnErase", dc)
    test_event(hand, "OnEraseContents", dc)
    test_event(hand, "OnHighlight", dc)
    keys = "keys"
    attachment = "attachment"
    test_event(hand, "OnLeftClick", x, y, keys, attachment)
    test_event(hand, "OnLeftDoubleClick", x, y, keys = 0, attachment = 0)
    test_event(hand, "OnRightClick", x, y, keys = 0, attachment = 0)
    test_event(hand, "OnDragLeft", draw, x, y, keys = 0, attachment = 0)
    test_event(hand, "OnBeginDragLeft", x, y, keys = 0, attachment = 0)
    test_event(hand, "OnEndDragLeft", x, y, keys = 0, attachment = 0)
    test_event(hand, "OnDragRight", draw, x, y, keys = 0, attachment = 0)
    test_event(hand, "OnBeginDragRight", x, y, keys = 0, attachment = 0)
    test_event(hand, "OnEndDragRight", x, y, keys = 0, attachment = 0)
    pt = "pt"
    test_event(hand, "OnSizingDragLeft", pt, draw, x, y, keys = 0, attachment = 0)
    test_event(hand, "OnSizingBeginDragLeft", pt, x, y, keys = 0, attachment = 0)
    test_event(hand, "OnSizingEndDragLeft", pt, x, y, keys = 0, attachment = 0)
    w = "w"
    h = "h"
    ## @TODO: why don't Begin/EndSize work like the others? 
    # test_event(hand, "OnBeginSize", w, h)
    # test_event(hand, "OnEndSize", w, h)
    test_event(hand, "OnDrawOutline", dc, x, y, w, h)
    test_event(hand, "OnDrawControlPoints", dc)
    test_event(hand, "OnEraseControlPoints", dc)


if __name__=="__main__":
    unittest.main()
