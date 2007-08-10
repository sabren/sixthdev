import CoreMIDI
import time, sys

def keychar(key):
    if key % 12 in (1, 3, 6, 8, 10): # black keys
        return "^"
    return "-"


class MidiKeyboard(object):
    def __init__(self):
        self.state = [keychar(x) for x in range(61)]

    def __call__(self, event):
        code, key, velocity = event
        key -= 36 # leftmost note on my keyboard
        if code == 144: # gets sent when i press or release a note
            if velocity == 0:
                self.state[key]=keychar(key)
            else:
                self.state[key]="#"

            
def playNotes():
    kMidiMessage_NoteOn 			= 0x90
    kMidiMessage_NoteOff 			= 0x80
    midiChannelInUse = 0

    # play an octave
    for i in range(13):
        noteNum = i + 60;
        onVelocity = 64
        
			
        print ("Playing Note: Status: 0x%lX, Note: %ld, Vel: %ld"
               % (kMidiMessage_NoteOn, noteNum, onVelocity))

        CoreMIDI.send(kMidiMessage_NoteOn, noteNum, onVelocity)
        
        time.sleep(0.25)

        CoreMIDI.send(kMidiMessage_NoteOff, noteNum, 0)



if __name__ == '__main__':

    mkb = MidiKeyboard()
    CoreMIDI.pyCallback=mkb.__call__

    playNotes()
    
    print "midi keyboard display. play notes and watch!"
    print "--------------------------------------------"
    while True:
        sys.stdout.write("  " + "".join(mkb.state) + "\r")
        sys.stdout.flush()
        time.sleep(0.01)
