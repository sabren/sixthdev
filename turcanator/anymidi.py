
"""
This talks to whatever midi library
is available. Currently supports CoreMIDI
on mac (in and out) and pypm on win32
(output only at the moment)

"""

import sys
if sys.platform == "darwin":
    import CoreMIDI
    device = CoreMIDI

    
elif sys.platform == "win32":
    import pypm
    pypm.Initialize()
    class PyProMidiDevice(object):
        def __init__(self):
            self.out = pypm.Output(0,0)
        def send(self, a, b, c):
            self.out.WriteShort(a,b,c)
    device = PyProMidiDevice()
    
else:
    raise ImportError("anymidi does not yet support this platform")

