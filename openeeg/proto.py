#!/usr/bin/python2.2
#
# python prototype of a mind-mirror style biofeedback machine
# Basically, this is just a spectral analysis program.
#
# This version only graphs random data, so it's not really
# much use yet. :)
#
# $Id$

## dependencies: ###############################################

try:
    import Numeric, FFT, RandomArray    # http://www.pfdubois.com/numpy/
    import pygame                       # http://www.pygame.org/
    from pygame.locals import *
except:
    raise SystemExit, "This program requries NumPy and pygame."

# the rest of these come with python:
import whrandom
import time

## support routines ############################################

def build_gradient():
    """
    Returns a 160*10 Surface showing green-yellow-red gradient.
    """
    colors = []
    for i in range(0, 0xff, 0x22):
        colors.append((i, 0xff, 0))
    colors.append((0xff, 0xff, 0))
    for i in range(0xcc, -1, -0x22):
        colors.append((0xff, i, 0))

    sprite = pygame.Surface((160, 10))
    for x in range(len(colors)):
        pygame.draw.rect(sprite, colors[x],
                         pygame.Rect(x*10, 0, 8, 10))
    return sprite



def init(winsize):
    pygame.init()
    pygame.display.set_caption("openEEG prototype")
    return pygame.display.set_mode(winsize, RESIZABLE, 0)


def main():
    #@TODO: un-hardcode all these numbers
    screen = init(winsize=(200, 400))
    grad = build_gradient()
    
    black = pygame.Surface((160,10))
    black.fill((0,0,0))

    done = 0
    while not done:

        data = RandomArray.randint(0, 16, (32,))
        for i in range(32):
            # draw the gradient, then cover part of it up:
            screen.blit(grad, (20,         20+i*11))
            screen.blit(black,(20+(data[i]*20), 20+i*11))
            
        # time.sleep(0.1) # if you want to slow it down

        pygame.display.update()
        for e in pygame.event.get():
            if (e.type == KEYUP and e.key == K_ESCAPE) \
            or (e.type == QUIT):
                done = 1
                

if __name__=="__main__":
    main()
