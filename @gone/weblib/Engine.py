"""
A wrapper object for running weblib scripts.

$Id$
"""

import weblib
import string

class Engine:

    """Engine - a wrapper class that runs a script in a custom environment.

    You should be able to run a weblib script as a regular cgi just by
    putting a #!/python line up top, and making it executable.. But,
    as an alternative, you can run it inside an Engine class. this is
    especially useful for testing or for restricted execution, etc..
    
    """

    globals = {'__name__':'__main__'}
    locals  = globals

    parts=("request", "response", "sess", "auth", "perm")

    script = None
    result = None
    
    traceback = None
    error     = None

    SUCCESS  = "* success *"
    FAILURE  = "* failure *"
    EXCEPTION = "* exception *"
      

    def __init__(self, script=None, pool=None, **kw):

        ### NOTE:
        ### I'm beginning to think that passing these things
        ### in as a parameter doesn't make much sense..
        ### especially, since auth checks in the session
        ### to find a session key (and thus requires an engine      
        ### just in the __init__)
        ###
        ### but maybe that's just a stupid way to do things,
        ### and I ought to give Auth a start() method just
        ### like sess... ? Probably same for Perm(), too.. (?)

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

            elif getattr(weblib, item, None):
                # use one in weblib (perhaps set up by .weblib.py
                _ = getattr(weblib, item)
                _.engine = self
                setattr(self, item, _)
                
            elif item=="sess":
                self.sess = weblib.Sess(pool, engine=self)

            else:
                # use a new copy of the default (eg, self.perm=weblib.Perm())
                setattr(self, item,
                        weblib.__dict__[string.capitalize(item)](engine=self))



    def interceptPrint(self):
        import sys
        self.stdout = sys.stdout
        sys.stdout = self.response
       

    
    def restorePrint(self):
        import sys
        sys.stdout = self.stdout


    def startParts(self):
        self.response.start()
        self.sess.start()
        self.auth.start()


    def stopParts(self):
        self.sess.stop()


    def injectParts(self):
        """Injects our parts into the weblib namespace"""

        self._oldParts = {}
       
        for part in Engine.parts:
            self._oldParts[part] = getattr(weblib, part, None)
            setattr(weblib, part, getattr(self, part, None))


    def restoreParts(self):
        """Restore the old weblib parts.."""

        for part in Engine.parts:
            if self._oldParts[part]:
                setattr(weblib, part, self._oldParts[part])
            else:
                # There was nothing there to begin with...
                # (This is usually the case.)
                # We have to do this because we don't want the
                # next engine that comes along to see our mess..
                delattr(weblib, part)


    def setPathInfo(self):
        if not self.request.environ.get("PATH_INFO"):        
            if (type(self.script) == type("")):
                self.request.environ["PATH_INFO"] = "UNKNOWN_SCRIPT.py"
            else:
                self.request.environ["PATH_INFO"] = self.script.name
        

    def setUp(self):
        self.startParts()
        self.injectParts()
        self.setPathInfo()
        self.interceptPrint()



    def tearDown(self):
        self.restorePrint()
        self.restoreParts()
        self.stopParts()
            


    def _execute(self, script):
        """This is so you can restrict execution in a subclass if you like."""
        exec(script, self.globals, self.locals)

    def execute(self, script):
        self.result = self.SUCCESS
        try:
            self._execute(script)
        except SystemExit:
            pass # don't really quit on response.end()
        except AssertionError, e:
            self.result = self.FAILURE
            self.error = e
        except:
            self.result = self.EXCEPTION
            import traceback, sys, string
            self.error = string.join(traceback.format_exception(
                sys.exc_type,
                sys.exc_value,
                sys.exc_traceback), '')

        

    def run(self):
        self.setUp()
        try:
            self.execute(self.script)
        finally:
            self.tearDown()
            
