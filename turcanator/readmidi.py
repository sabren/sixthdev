from midi.MidiOutStream import MidiOutStream
from midi.MidiInFile import MidiInFile
from keyboard import PRESS, HOLD, UNPRESSED, Keyboard
import keyboard
import logging

eighth_note = 240 # why?


def continued(s):
    if s == keyboard.PRESS: return keyboard.HOLD
    else: return s

class ScoreBuilder(MidiOutStream):

    def __init__(self):
        MidiOutStream.__init__(self)
        self._last_time = 0
        self.keyboard = Keyboard()
        self._last_status = None
        self.score = []

    def note_on(self, channel=0, note=0x40, velocity=0x40):
        #print ("note_on: %s" % note)
        self.keyboard.note_on(note)

    def note_off(self, channel=0, note=0x40, velocity=0x40):
        #print ("note_off:    %s" % note)
        self.keyboard.note_off(note)

    def update_time(self, new_time=0, relative=1):
        #print ("new_time:         %s" % new_time)
        
        
        MidiOutStream.update_time(self, new_time, relative)
        if self._absolute_time != self._last_time:
            diff = self._absolute_time - self._last_time

            #print keyboard.format(self.keyboard.snapshot())
            self.score.append(self.keyboard.snapshot())

            self._last_status = [continued(x) for x in self.keyboard.snapshot()]
            for tick in range((diff/eighth_note)-1):
                #print keyboard.format(self._last_status)
                self.score.append(self._last_status)
            
            self._last_time = self._absolute_time
            

def buildScore(in_file):
    event_handler = ScoreBuilder()
    midi_in = MidiInFile(event_handler, in_file)
    midi_in.read()
    return event_handler.score

if __name__=="__main__":
    for row in buildScore('rondo-alla-turca-a.mid'):
        #break
        #pass
        print keyboard.format(row)
