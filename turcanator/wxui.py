
import wx


class PianoRollFrame(wx.Frame, AbstractPianoArt):
    def __init__(self, parent, id, title, queue, *a, **kw):
        wx.Frame.__init__(self, parent, id, title, *a, **kw)
        self.queue = queue
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.setupEventMap()
            
    def setupEventMap(self):
        self.eventMap = {
            wx.WXK_ESCAPE: STOP,
            wx.WXK_DOWN: DOWN,
            wx.WXK_UP : UP,
            wx.WXK_PAGEDOWN : DOWNFAST,
            wx.WXK_PAGEUP : UPFAST,
            wx.WXK_SUBTRACT: TOSTART,
            wx.WXK_SPACE: TOEND,
            wx.WXK_TAB: ROTATE_HANDS,
            wx.WXK_F2 : SLOWER,
            wx.WXK_F3: FASTER,
            ord('P'): PLAY,
            ord('M'): METRONOME,
            ord('['): SETSTART,
            ord(']'): SETSTOP,
        }

    def OnKeyPress(self, e):
        turcEvent = self.eventMap.get(e.GetKeyCode())
        if turcEvent:
            self.queue.put(turcEvent)


class WxUI(AbstractPianoArt):
    """
    This class drives the PianoRollFrame.

    It talks to us by putting events into the queue.
    
    We talk to it by using wx.CallAfter()
    
    """

    def __init__(self, win, queue):
        self.queue = queue
        self.win = win
        self.dc = wx.MemoryDC()
        self.dc.SelectObject(wx.EmptyBitmap(WINW, WINH))

    def flip(self):
        wx.ClientDC(self.win).Blit(0,0,WINW,WINH, self.dc, 0,0)

    def drawRect(self, color, x, y, w, h):
        c = wx.Colour(*color)
        self.dc.SetBrush(wx.Brush(c))
        self.dc.SetPen(wx.Pen(c))
        self.dc.DrawRectangle(x, y, w, h)

    def quit(self):
        print "quitting..."

    def putEvent(self, e):
        self.queue.append(e)
        
    def getEvent(self):
        try:
            e = self.queue.get(False)
            self.queue.task_done()
            return e
        except Queue.Empty:
            pass
