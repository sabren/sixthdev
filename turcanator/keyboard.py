

leftmost_key = 36
numkeys = 61

PRESS = 1
HOLD = -1
UNPRESSED = 0

charmap = {PRESS:'X', HOLD:'x', UNPRESSED:'.'}

def format(state):
    return ''.join([charmap[x] for x in state])

def keychar(key):
    if key % 12 in (1, 3, 6, 8, 10): # black keys
        return "^"
    return "-"


class Keyboard(object):
    """
    I represent the state of a piano keyboard.
    """
    def __init__(self, size=61, leftmost=36):
        self.size = size
        self.leftmost = leftmost
        self.state = [UNPRESSED for x in range(size)]

    def __call__(self, event):
        code, key, velocity = event
        if code == 144: # gets sent when i press or release a note
            if velocity == 0:
                self.note_off(key)
            else:
                self.note_on(key)

    def note_off(self, note):
        self.state[note - self.leftmost]=UNPRESSED

    def note_on(self, note):
        self.state[note - self.leftmost]=PRESS

    def snapshot(self):
        return self.state[:]
    
    def format(self):
        return format(self.state)


if __name__ == '__main__':
    
    import CoreMIDI
    import time, sys
    
    mkb = Keyboard()
    CoreMIDI.pyCallback=mkb.__call__
    
    print "midi keyboard display. play notes and watch!"
    print "--------------------------------------------"
    while True:
        sys.stdout.write("  " + mkb.format() + "\r")
        sys.stdout.flush()
        time.sleep(0.01)
