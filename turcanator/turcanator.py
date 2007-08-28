#!/usr/bin/env python2.4
# STILL NEED PYTHON 2.4 UNTIL WE RECOMPILE PYREX AND INSTALL PYGAME
"""
turcanator: a (somewhat primitive) midi piano tutor


"""
import sys
global pygame
import clockwork
import readmidi
import keyboard
from keyboard import PRESS, HOLD, UNPRESSED
import anymidi
from anymidi import device
from colors import *


KEYH=10
KEY_RANGE=60

WINW=1024
WINH=700

# midi event numbers

NoteOn 	= 0x90
NoteOff	= 0x80

# custom abstract events:
# these add a layer of indirection, mapping system events
# to custom events. This will let the user remap keys
# at some point, but the main purpose is to ease the
# transition from pygame to wxpython.
EXIT, UP, DOWN, UPFAST, DOWNFAST, SETSTART, SETSTOP, TOSTART, PLAY = range(9)



def comparison(goals, actuals):
    return [compareOne(goal, actual) for (goal, actual) in zip(goals, actuals)]


def compareOne(goal, actual):
    if goal in (PRESS, HOLD):
        if actual in (PRESS, HOLD):
            return green
        else:
            return colormap[goal]
    else:
        if actual in (PRESS, HOLD):
            return red
        else:
            return None

def yPos(y):
    offset = y / 8 # add an extra line every 8 boxes (2:4 time sig)
    offset += 2 * (y / 16) # +2 every 16 (remeber 2/16 != 1/8 for ints!!)
    return offset + 10 + y * KEYH



class AutoPlayer(object):
    """
    I am the playback mechanism.
    """
    def __init__(self, score):
        self.score = score
        self.whereToStart = 0
        self.whereToStop  = len(score) - 1
        self.playing = None
        self.pos = 0
        
    def play(self):
        if self.playing:
            self.playing.stop()
        self.pos = self.whereToStart
        self.playing = clockwork.spawn(self.gen_notes())

    def gen_notes(self):

        prev = [0] * keyboard.numkeys # blank piano

        while self.pos < self.whereToStop:
            state = self.score[self.pos]
            for (e, (was, now)) in enumerate(zip(prev, state)):
                i = e + keyboard.leftmost_key
                if now == PRESS:
                    device.send(NoteOff, i, 0)
                    device.send(NoteOn, i, 32)
                elif (now == UNPRESSED) and (was != UNPRESSED):
                    device.send(NoteOff, i, 0)
            prev = state

            yield clockwork.sleep(0.50)
            self.pos += 1
            
        # now be quiet, even if selection cuts off mid-note:
        for i in range(keyboard.numkeys):
            device.send(NoteOff, i+keyboard.leftmost_key, 0)

        self.playing = False



def loopback(whereToStop, whereToStart, pos):
    if pos > whereToStop: return whereToStart
    return pos




class Cursor(object):
    def __init__(self, len, pos=0):
        self.len = len
        self.pos = pos
        self.checkBounds = self.constrain # vs wrap
        
    def up(self, by=1):
        self.pos -= by
        self.checkBounds()
        
    def down(self, by=1):
        self.pos += by
        self.checkBounds()
        
    def jump(self, pos):
        self.pos = pos
        self.checkBounds()

    def constrain(self):
        if self.pos >= self.len: self.pos = self.len -1
        if self.pos < 0 : self.pos = 0



class AbstractPianoArt(object):
    
    def drawScore(self, score):
        for i, row in enumerate(score):
            if i % 2: pal = dimA
            else: pal = dimB
            self.drawPiano(10, yPos(i), pal, colors(row))

    def clearBright(self, score, line):
        if line % 2: pal = dimA
        else: pal = dimB
        self.drawPiano(10, yPos(line), pal, colors(score[line]))

    def drawKey(self, x, y, w,h, color, highlightColor=None):

        borderColor = (50,50,50)

        # draw black outline:
        self.drawRect(borderColor, x, y, w, h)

        # draw square itself:
        self.drawRect(color, x+1, y, w-1, h)

        if highlightColor == blue2:
            
            # kludge for continued notes...
            self.drawRect(blue, x+2, y-3, w-3, h+2)

        elif highlightColor:
            self.drawRect(highlightColor, x+2, y+2, w-3, h-3)


    def drawPiano(self, x, y, palette, colors, keyw=16, keyh=KEYH):
        for k in range(KEY_RANGE):
            self.drawKey(x+keyw*k, y, keyw, keyh, keycolor(palette, k), colors[k])

    def drawBracket(self, top, bot):
        self.drawRect((0,0,0), 5, 0, 5, WINH)
        self.drawRect(brackcolor, 5, yPos(top), 5, yPos(bot-top))



    # this is all you have to Implement:
    def drawRect(self, color, x, y, w, h):
        raise NotImplementedError


    
class PyGameUI(AbstractPianoArt):
    def __init__(self):
        global pygame
        import pygame
        
        # set up the screen
        pygame.init()
        pygame.key.set_repeat(100, 10)
        self.screen = pygame.display.set_mode([WINW, WINH])
        pygame.display.set_caption("the turcanator v0.2")
        self.screen.fill([0,0,0])
        self.setupEventMap()

    def flip(self):
        pygame.display.flip()

    def quit(self):
        pygame.display.quit()


    def drawRect(self, color, x, y, w, h):
        pygame.draw.rect(self.screen, color, pygame.Rect(x,y,w,h))


    def setupEventMap(self):
        self.eventMap = {
            pygame.K_ESCAPE: EXIT,
            pygame.K_DOWN : DOWN,
            pygame.K_UP : UP,
            pygame.K_PAGEDOWN: DOWNFAST,
            pygame.K_PAGEUP : UPFAST,
            pygame.K_LEFTBRACKET: SETSTART,
            pygame.K_RIGHTBRACKET: SETSTOP,
            pygame.K_SPACE: TOSTART,
            pygame.K_p : PLAY,
        }


    def getEvent(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT: return EXIT
        elif event.type == pygame.KEYDOWN:
            return self.eventMap.get(event.key)

        


import wx
NEEDBLIT = 55555555555555

class PianoRollFrame(wx.Frame, AbstractPianoArt):
    def __init__(self, parent, id, title, queue, *a, **kw):
        wx.Frame.__init__(self, parent, id, title, *a, **kw)
        self.queue = queue
##         self.Bind(wx.EVT_PAINT, self.OnPaint)

##     def OnPaint(self, e):
##         self.queue.put(NEEDBLIT)


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
            if e == NEEDBLIT:
                self.blit()
            else:
                return e
        except Queue.Empty:
            pass


def main(ui):

    if len(sys.argv) > 1:
        midifile = sys.argv[1]
    else:
        midifile = 'rondo-alla-turca-a.mid'


    score = readmidi.buildScore(midifile)

    
    player = AutoPlayer(score)
    liveKeyboard = keyboard.Keyboard()
    device.pyCallback = liveKeyboard
    


    ui.drawScore(score)
    ui.drawBracket(player.whereToStart, player.whereToStop)
    ui.flip()
    
    # -----
   
    cursor = Cursor(len(score))
    while True:

        ui.clearBright(score, cursor.pos)
        ui.clearBright(score, player.pos)
        
        clockwork.tick()
        anymidi.tick()
               
        e = ui.getEvent()
        if e: print e

        if e == EXIT:        break
        elif e == DOWN:      cursor.down()
        elif e == UP:        cursor.up()
        elif e == DOWNFAST:  cursor.down(8)
        elif e == UPFAST:    cursor.up(8)

        # loopback support:

        elif e == SETSTART:
            player.whereToStart = cursor.pos
            ui.drawBracket(player.whereToStart, player.whereToStop)

        elif e == SETSTOP:
            player.whereToStop = cursor.pos
            ui.drawBracket(player.whereToStart, player.whereToStop)

        elif e == TOSTART:
            cursor.jump(player.whereToStart)

        # player support:
        elif e == PLAY:
            player.play()

        snap = liveKeyboard.snapshot()

        # if input matches the goal, move forward one line
        if snap == map(abs,score[cursor.pos]):
            cursor.jump(loopback(player.whereToStop,
                                 player.whereToStart, cursor.pos + 1))

        # always draw the computer's cursor first...
        if player.playing:
            ui.drawPiano(10, yPos(player.pos), computerCursor,
                              colors(score[player.pos]))
            
        # so that the user's cursor covers it:
        ui.drawPiano(10, yPos(cursor.pos), midiCursor,
                          comparison(score[cursor.pos],snap))

        ui.flip()
    ui.quit()




if __name__ == '__main__':
    USE_PYGAME = True # False

    if USE_PYGAME:
        main(PyGameUI())
    else:
        import wx
        import threading
        import Queue

        queue = Queue.Queue(0)

        app = wx.App(redirect = False)
        frame = PianoRollFrame(None, -1, "turcanator", queue, size=(WINW,WINH))
        frame.Show(True)
        
        t = threading.Thread(target=main, args=(WxUI(frame, queue),))
        t.start()

        app.MainLoop()
        queue.put(EXIT)

