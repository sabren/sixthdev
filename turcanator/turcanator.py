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
(EXIT, UP, DOWN, UPFAST, DOWNFAST, SETSTART, SETSTOP, TOSTART, TOEND,
 PLAY, STOP, ROTATE_HANDS, FASTER, SLOWER, METRONOME, SEPRIGHT, SEPLEFT
 )= range(17)



def comparison(goals, actuals):
    return [compareOne(goal, actual) for (goal, actual) in zip(goals, actuals)]



def compareOne(goal, actual):
    if goal in (PRESS, HOLD):
        if actual in (PRESS, HOLD):
            return HIT
        else:
            return goal
    else:
        if actual in (PRESS, HOLD):
            return MISS
        else:
            return None

def yPos(y):
    offset = y / 4 # add an extra line every 4 boxes (2:4 time sig)
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
        self.tickSpeed = 0.2
        self.beat = -1
        self.visible = False

    def faster(self):
        self.tickSpeed -= 0.1
        if self.tickSpeed < 0:
            self.tickSpeed = 0

    def slower(self):
        self.tickSpeed += 0.1


    def stop(self):
        if self.playing:
            self.playing.stop()
        self.beat = -1
        
    def play(self):
        self.stop()
        self.pos = self.whereToStart
        self.playing = clockwork.spawn(self.gen_notes())

    def metronome(self):
        self.stop()
        self.playing = clockwork.spawn(self.gen_metro())

    def do_metro(self):
        self.beat += 1
        if self.beat % 16 == 0:
            device.send(NoteOn + 9, 35, 60)
        elif self.beat % 4 == 0:
            # 10th channel is percussion
            device.send(NoteOn + 9, 37, 40)

    def gen_metro(self):
        while True:
            yield clockwork.sleep(self.tickSpeed)
            self.do_metro()

    def gen_notes(self):

        prev = [0] * keyboard.numkeys # blank piano

        for x in range(16):
            yield clockwork.sleep(self.tickSpeed)
            self.do_metro()

        self.visible = True
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

            yield clockwork.sleep(self.tickSpeed)
            self.do_metro()

            
            self.pos += 1
            
        # now be quiet, even if selection cuts off mid-note:
        for i in range(keyboard.numkeys):
            device.send(NoteOff, i+keyboard.leftmost_key, 0)

        self.visible = False
        self.playing = None


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

    sep = None
    
    
    def drawScore(self, score):
        for i, row in enumerate(score):
            if i % 2: pal = dimA
            else: pal = dimB
            self.drawPiano(10, yPos(i), pal, row)

    def clearBright(self, score, line):
        if line % 2: pal = dimA
        else: pal = dimB
        self.drawPiano(10, yPos(line), pal, score[line])

    def drawKey(self, x, y, w,h, color, mark=None):

        borderColor = (50,50,50)
        highlightColor = colormap.get(mark)

        # draw black outline:
        self.drawRect(borderColor, x, y, w, h)

        # draw square itself:
        self.drawRect(color, x+1, y, w-1, h)

        if mark == HOLD:
            
            # kludge for continued notes...
            self.drawRect(highlightColor, x+2, y-3, w-3, h+2)

        elif highlightColor:
            self.drawRect(highlightColor, x+2, y+2, w-3, h-3)


    def drawPiano(self, x, y, palette, marks, keyw=16, keyh=KEYH):
        
        for k in range(KEY_RANGE):
            fade = False
            if (self.sep and k > self.sep):
                shift = 2
                if self.hand == LEFT_HAND: fade = True
            else:
                shift = 0
                if self.hand == RIGHT_HAND: fade = True
            self.drawKey(x+keyw*k+shift, y, keyw, keyh,
                         keycolor(palette, k, fade), marks[k])

    def drawBracket(self, top, bot):
        self.drawRect((0,0,0), 5, 0, 5, WINH)
        self.drawRect(brackcolor, 5, yPos(top), 5, yPos(bot-top))


    def separate(self, where):
        self.sep = where
            

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
            pygame.K_ESCAPE: STOP,
            pygame.K_DOWN : DOWN,
            pygame.K_UP : UP,
            pygame.K_PAGEDOWN: DOWNFAST,
            pygame.K_PAGEUP : UPFAST,
            pygame.K_LEFTBRACKET: SETSTART,
            pygame.K_RIGHTBRACKET: SETSTOP,
            pygame.K_MINUS: TOSTART,
            pygame.K_SPACE: TOEND,
            pygame.K_p : PLAY,
            pygame.K_m : METRONOME,
            pygame.K_TAB: ROTATE_HANDS,
            pygame.K_F2: FASTER,
            pygame.K_F3: SLOWER,
            pygame.K_LEFT: SEPLEFT,
            pygame.K_RIGHT: SEPRIGHT,
        }


    def getEvent(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT: return EXIT
        elif event.type == pygame.KEYDOWN:
            return self.eventMap.get(event.key)



LEFT_HAND  = -1
BOTH_HANDS = 0
RIGHT_HAND = +1

def main(ui):

    if len(sys.argv) > 1:
        midifile = sys.argv[1]
    else:
        midifile = 'rondo-alla-turca-a.mid'


    score = readmidi.buildScore(midifile)
    
    player = AutoPlayer(score)
    liveKeyboard = keyboard.Keyboard()
    device.pyCallback = liveKeyboard
    

    ui.hand = BOTH_HANDS
    ui.separate(30)
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

        if e == EXIT:        break
        elif e == DOWN:      cursor.down()
        elif e == UP:        cursor.up()
        elif e == DOWNFAST:  cursor.down(8)
        elif e == UPFAST:    cursor.up(8)
        elif e == FASTER :   player.faster()
        elif e == SLOWER :   player.slower()
        elif e == METRONOME : player.metronome()

        # loopback support:

        elif e == SETSTART:
            player.whereToStart = cursor.pos
            ui.drawBracket(player.whereToStart, player.whereToStop)

        elif e == SETSTOP:
            player.whereToStop = cursor.pos
            ui.drawBracket(player.whereToStart, player.whereToStop)

        elif e == TOSTART:
            cursor.jump(player.whereToStart)

        elif e == TOEND:
            cursor.jump(player.whereToStop)

        elif e == ROTATE_HANDS:
            if ui.hand == LEFT_HAND: ui.hand = BOTH_HANDS
            elif ui.hand == RIGHT_HAND: ui.hand = LEFT_HAND
            else: ui.hand = RIGHT_HAND
            ui.drawScore(score)

        elif e == SEPLEFT:
            ui.sep -= 1
            if ui.sep <= 0 : ui.sep = 0
            ui.drawScore(score)
        elif e == SEPRIGHT:
            maxsep = 80 # @TODO: FIX!
            ui.sep += 1
            if ui.sep >= maxsep : ui.sep = maxsep
            ui.drawScore(score)
            
        # player support:
        elif e == PLAY:
            player.play()
        elif e == STOP:
            player.stop()

        snap = liveKeyboard.snapshot()

        # if input matches the goal, move forward one line

        if ui.hand == LEFT_HAND: r = None, ui.sep
        elif ui.hand == RIGHT_HAND: r = ui.sep, None
        else: r = None, None
        
        if snap[r[0]:r[1]] == map(abs,score[cursor.pos][r[0]:r[1]]):
            cursor.jump(loopback(player.whereToStop,
                                 player.whereToStart, cursor.pos + 1))

        # always draw the computer's cursor first...
        if player.visible:
            ui.drawPiano(10, yPos(player.pos), computerCursor,
                              score[player.pos])
            
        # so that the user's cursor covers it:
        ui.drawPiano(10, yPos(cursor.pos), midiCursor,
                          comparison(score[cursor.pos],snap))

        ui.flip()
    ui.quit()




if __name__ == '__main__':
    USE_PYGAME = False # True

    if USE_PYGAME:
        main(PyGameUI())
    else:
        import wx
        import threading
        import Queue
        exec open('wxui.py')

        queue = Queue.Queue(0)

        app = wx.App(redirect = False)
        frame = PianoRollFrame(None, -1, "turcanator", queue, size=(WINW,WINH))
        frame.Show(True)
        
        t = threading.Thread(target=main, args=(WxUI(frame, queue),))
        t.start()

        app.MainLoop()
        queue.put(EXIT)

