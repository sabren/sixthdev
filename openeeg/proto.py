#!/usr/bin/python2.2
#
# openEEG software prototype
# by michal wallace (sabren@manifestation.com)
#
# python prototype of a mind-mirror style biofeedback machine
# Basically, this is just a spectral analysis program.
#
# This version graphs fake data, but doesn't seem to be
# working right. The fakeSession() function explains what I
# think the graph should show, but it doesn't work out right.
# can anyone help?
#
# $Id$

## dependencies: #####################################################

try:
    import Numeric, FFT, RandomArray    # http://www.pfdubois.com/numpy/
    import pygame                       # http://www.pygame.org/
    from pygame.locals import *
except:
    raise SystemExit, "This program requries NumPy and pygame."

# the rest of these come with python:
import whrandom
import time

## graphic routines ##################################################

def makeGradient():
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


def makeWindow(winsize):
    pygame.init()
    pygame.display.set_caption("openEEG prototype")
    return pygame.display.set_mode(winsize, RESIZABLE, 0)


def keepLooping():
    pygame.display.update()
    for e in pygame.event.get():
        if (e.type == KEYUP and e.key == K_ESCAPE) \
        or (e.type == QUIT):
            return 0
    return 1



## data routines #####################################################

def wave(frequency, sampRate=256.0):
    """
    Returns a sampled wave at the given frequency and sample rate.

    This routine is generalized from Eric Hagemann's article at:
    http://www.onlamp.com/pub/a/python/2001/01/31/numerically.html
    """
    return Numeric.sin(2 * Numeric.pi
                         * (frequency/sampRate)
                         * Numeric.arange(sampRate))


def fakeSession():
    """
    Creates ten seconds of completely fake data.
    """
    pureAlpha = 10                      # alpha is 8-12hz
    pureBeta  = 20                      # beta is 13-30hz
    pureTheta = 6                       # theta is 4-8hz
    pureDelta = 2                       # delta is 0.5-4hz

    sec = [None] * 10                   # make an empty list
    
    # when animated, this should move right up the line:
    sec[0] = wave(pureDelta)
    sec[1] = wave(pureTheta)
    sec[2] = wave(pureAlpha)
    sec[3] = wave(pureBeta)

    # and this should move back down in pairs:
    sec[4] = wave(pureBeta)  + wave(pureAlpha)
    sec[5] = wave(pureAlpha) + wave(pureTheta)
    sec[6] = wave(pureTheta) + wave(pureDelta)
    sec[7] = wave(pureDelta) + wave(pureBeta)

    # all four at once:
    sec[8] = wave(pureDelta) + wave(pureTheta) \
             + wave(pureAlpha) + wave(pureBeta)

    # and then silence:
    sec[9] = wave(0)

    return Numeric.concatenate(sec)


def makeSpectrogram(slice):
    """
    Returns a list of length 32, with the FFT of the slice.
    We seem to need 64 samples to do this.
    If the sample rate is 256Hz, then we're talking about
    1/4th of a second's worth of data here.
    """
    assert len(slice)==64, "we want 32 bins, so we need 64 samples"

    res = abs(FFT.real_fft(slice))[:-1] # discard 33rd slot (is this okay?)
    res = Numeric.floor(res) # round off to integers
    
    assert len(res)==32, len(res)
    return res
    

## main program ######################################################

def main():
    #@TODO: make names for all these magic numbers...
    
    screen = makeWindow(winsize=(200, 400))
    grad = makeGradient()
    
    black = pygame.Surface((160,10))
    black.fill((0,0,0))

    session = fakeSession()
    t = 0

    while keepLooping():

        # simulate aquiring data for 1/4th of a second (64 samples):
        time.sleep(0.25) 
        data = makeSpectrogram(session[t:t+64])
        print data
        t += 64
        if t >= len(session):
            t = 0
        
        # draw the gradient, then cover part of it up:
        for i in range(32):
            screen.blit(grad, (20,         20+i*11))
            screen.blit(black,(20+(data[i]*20), 20+i*11))


if __name__=="__main__":
    main()
