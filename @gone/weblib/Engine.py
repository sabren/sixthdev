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

    def __init__(self, script=None, pool=None, **kw):

        self.script = script       

        # first make sure they haven't passed us any bogus
        # keywords..
        
        acceptable = ["request", "response", "sess", "auth", "perm"]
        for item in kw.keys():
            if item not in acceptable:
                raise TypeError, "unexpected keyword argument: " + item

        # Any of the singletons can be turned off by passing
        # None, or customized by passing an instance..

        for item in acceptable:
            
            if kw.has_key(item):
                # use the one they supplied
                setattr(self, item, kw[item])
                kw[item].engine = self
                
            elif item=="sess":
                self.sess = weblib.Sess(pool, engine=self)

            else:
                # use the default (eg, self.perm=weblib.Perm())
                setattr(self, item, weblib.__dict__[string.capitalize(item)](engine=self))



    def setUp(self):
        import sys
        self.stdout = sys.stdout
        sys.stdout = self.response


    def tearDown(self):
        import sys
        sys.stdout = self.stdout



    def execute(self, script):
        """This is here so you can do restricted execution in a subclass if you like."""
        exec(script)



    def run(self):
        self.setUp()
        try:
            try:
                self.execute(self.script)
            except SystemExit:
                pass # don't really quit on response.end()                
        finally:
            self.tearDown()

