
"""
This talks to whatever midi library
is available. Currently supports CoreMIDI
on mac (in and out) and pypm on win32
(output only at the moment)

@TODO: move everything to PyPortMidi
"""

import sys
if sys.platform == "darwin":
    import CoreMIDI
    device = CoreMIDI
    def tick(): pass
    
elif sys.platform == "win32":
    import pypm
    pypm.Initialize()

    class PyPortMidiDevice(object):

        def __init__(self):
            self.outd = pypm.Output(0,0)
            self.ind = pypm.Input(1) #@TODO: select from dropdown.
            self.pyCallback = lambda a,b,c : None # do nothing
            self.echo = True

        def tick(self):
            while self.ind.Poll():
                (a,b,c,d), time = self.ind.Read(1)[0]
                self.pyCallback((a,b,c))
                if self.echo:
                    self.send(a,b,c)
                
        def send(self, a, b, c):
            self.outd.WriteShort(a,b,c)
    device = PyPortMidiDevice()
    def tick(): device.tick()
else:
    raise ImportError("anymidi does not yet support this platform")

