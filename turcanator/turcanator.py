#!/usr/bin/env python2.4
"""
turcanator: a (somewhat primitive) midi piano tutor


"""
import sys, pygame
import clockwork
import readmidi
import keyboard
from keyboard import PRESS, HOLD, UNPRESSED
from anymidi import device
from colors import *

class Rectangle(object):
    def __init__(self, w,h, color, highlight, x=0,y=0):
        self.rect = (x,y,w,h)
        self.color = color
        self.border = (50,50,50)
        self.highlight = highlight
    def translate(self, dx,dy):
        x,y,w,h = self.rect
        return self.__class__(w, h, self.color, self.highlight, x+dx, y+dy)
    def draw(self, surface):
        x,y,w,h = self.rect
        # draw black outline:
        pygame.draw.rect(surface, self.border, pygame.Rect(*self.rect), 1)
        # draw square itself:
        pygame.draw.rect(surface, self.color,
                         pygame.Rect(x+1,y,w-1,h))
        if self.highlight:
            
            if self.highlight == blue2:
                # kludge for continued notes...
                pygame.draw.rect(surface, blue,
                         pygame.Rect(x+2,y-3,w-3,h+2))
            else:
                pygame.draw.rect(surface, self.highlight,
                         pygame.Rect(x+2,y+2,w-3,h-3))
        

keyh=5
def drawPiano(x, y, palette, colors, keyw=8, keyh=keyh):
    for k in range(60):
        (Rectangle(keyw,keyh,keycolor(palette, k),colors.get(k))
         .translate(x+keyw*k, y)
         .draw(screen))

def drawScore(score, x):
    for i, row in enumerate(score):
        drawPiano(x, yPos(i), dim, colors(row))
        



def comparison(goals, actuals):
    res = {}
    for k, (goal, actual) in enumerate(zip(goals, actuals)):
        res[k] = compareOne(goal, actual)
    return res

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
    return offset + 10 + y * keyh

WINH=700

def drawbracket(screen, top, bot):
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(5, 0, 5, WINH))
    pygame.draw.rect(screen, brackcolor,
                     pygame.Rect(5, yPos(top), 5, yPos(bot-top)))



# midi event numbers

NoteOn 	= 0x90
NoteOff	= 0x80

class Player(object):
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
            state = score[self.pos]
            for (e, (was, now)) in enumerate(zip(prev, state)):
                i = e + keyboard.leftmost_key
                if now == PRESS:
                    print "note 0x", hex(i), "=", i, "on"
                    device.send(NoteOff, i, 0)
                    device.send(NoteOn, i, 32)
                elif (now == UNPRESSED) and (was != UNPRESSED):
                    print "note 0x", hex(i), "=", i, "off"
                    device.send(NoteOff, i, 0)
            prev = state

            yield clockwork.sleep(0.50)
            self.pos += 1
            
        # now be quiet, even if selection cuts off mid-note:
        for i in range(keyboard.numkeys):
            device.send(NoteOff, i+keyboard.leftmost_key, 0)

        self.playing = False


def clearbright(line):
    drawPiano(10, yPos(line), dim, colors(score[line]))

def loopback(pos):
    if pos > player.whereToStop: return player.whereToStart
    return pos
    


if __name__ == '__main__':


    
    if len(sys.argv) > 1:
        midifile = sys.argv[1]
    else:
        midifile = 'rondo-alla-turca-a.mid'


    score = readmidi.buildScore(midifile) 
    player = Player(score)
    liveKeyboard = keyboard.Keyboard()
    device.pyCallback = liveKeyboard

    
    # set up the screen
    
    pygame.init()   
    screen = pygame.display.set_mode([620, WINH])
    pygame.display.set_caption("turcanator 0.1")

    screen.fill([0,0,0])
    drawScore(score, 10)
    drawbracket(screen, player.whereToStart, player.whereToStop)
    pygame.display.flip()
    
    # -----
   
    pos = 0
    while True:

        clearbright(pos)
        clearbright(player.pos)
        
        clockwork.tick()
               
        event = pygame.event.poll()
        if event.type == pygame.QUIT: break
        elif event.type == pygame.KEYDOWN:

            
            if event.key == pygame.K_ESCAPE:
                break
            elif event.key == pygame.K_DOWN:
                pos += 1
            elif event.key == pygame.K_UP:
                pos -= 1
            elif event.key == pygame.K_PAGEDOWN:
                pos += 8
            elif event.key == pygame.K_PAGEUP:
                pos -= 8

            # loopback support:

            elif event.key == pygame.K_LEFTBRACKET:
                player.whereToStart = pos
                drawbracket(screen, player.whereToStart, player.whereToStop)
            elif event.key == pygame.K_RIGHTBRACKET:
                player.whereToStop = pos
                drawbracket(screen, player.whereToStart, player.whereToStop)
            elif event.key == pygame.K_SPACE:
                pos = player.whereToStart

            # player support:
            elif event.key == pygame.K_p:
                player.play()
                
            # bounds checking:
            if pos >= len(score): pos = len(score)-1
            if pos < 0 : pos = 0
    
        snap = liveKeyboard.snapshot()
        if snap==[n*n for n in score[pos]]:
            clearbright(pos)
            pos = loopback(pos + 1)
        else:
            pass

        # draw the computer's cursor first,
        # so that the user's cursor covers it.
        if player.playing:
            drawPiano(10, yPos(player.pos), playing,
                      colors(score[player.pos]))
        
        drawPiano(10, yPos(pos), bright,
                  comparison(score[pos],snap))

        pygame.display.flip()

    pygame.display.quit()
