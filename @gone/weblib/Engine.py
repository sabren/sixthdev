# weblib.Engine

import weblib
import string

class Engine:

    """Engine - a wrapper class that runs a script in a custom environment.

    You should be able to run a weblib script as a regular cgi just by putting
    a "#/python" line up top, and making it executable.. But, as an alternative,
    you can run it inside an Engine class. this is especially useful for testing
    or for restricted exection, etc..
    
    """

    parts=("request", "response", "sess", "auth", "perm")

    def __init__(self, script=None, pool=None, **kw):

        self.script = script       

        # first make sure they haven't passed us any bogus
        # keywords..
        
        for item in kw.keys():
            if item not in Engine.parts:
                raise TypeError, "unexpected keyword argument: " + item

        # Any of the singletons can be turned off by passing
        # None, or customized by passing an instance..

        for item in Engine.parts:
            
            if kw.has_key(item):
                # use the one they supplied
                setattr(self, item, kw[item])
                kw[item].engine = self
                
            elif item=="sess":
                self.sess = weblib.Sess(pool, engine=self)

            else:
                # use a new copy of the default (eg, self.perm=weblib.Perm())
                setattr(self, item, weblib.__dict__[string.capitalize(item)](engine=self))


    def interceptPrint(self):
        import sys
        self.stdout = sys.stdout
        sys.stdout = self.response
       

    
    def restorePrint(self):
        import sys
        sys.stdout = self.stdout



    def injectParts(self):
        """Injects our parts into the weblib namespace"""

        self._oldParts = {}
       
        for part in Engine.parts:
            self._oldParts[part] = getattr(weblib, part, None)
            setattr(weblib, part, getattr(self, part, None))



    def restoreParts(self):
        """Restore the old weblib parts.."""

        for part in Engine.parts:
            setattr(weblib, part, self._oldParts[part])



    def setUp(self):
        self.injectParts()
        self.interceptPrint()
        self.response.clear()



    def tearDown(self):
        self.restorePrint()
        self.restoreParts()
            


    def execute(self, script):
        """This is here so you can do restricted execution in a subclass if you like."""
        exec(script)


    def run(self):
        #@TODO: capture error messages; expose a result flag...
        self.setUp()
        try:
            try:
                self.execute(self.script)
            except SystemExit:
                pass # don't really quit on response.end()                
        finally:
            self.tearDown()

