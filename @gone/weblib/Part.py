"""
weblib.Part - this is really just an interface.. nothing actually
              uses it, though you could use it as a stub for sess,
              response, etc...
"""
__ver__="$Id$"

class Part:
    def start(self, *kw):
        pass

    def stop(self, *kw):
        pass

