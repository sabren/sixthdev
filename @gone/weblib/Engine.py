"""
A wrapper object for running weblib scripts.
"""
__ver__ = "$Id$"

import weblib
import string

#@TODO: a lot of these methods could be consolidated!

class Engine:
    """
    Engine - a wrapper class that runs a script in a custom environment.

    You should be able to run a weblib script as a regular cgi just by
    putting a #!/python line up top, and making it executable.. But,
    as an alternative, you can run it inside an Engine class. this is
    especially useful for testing or for restricted execution, etc..
    """

    globals = {'__name__':'__main__'}
    locals  = globals

    parts=("request", "response")

    script = None
    result = None
    
    traceback = None
    error     = None

    SUCCESS   = "* success *"
    FAILURE   = "* failure *"
    EXCEPTION = "* exception *"
    EXIT      = "* exit *"
      

    def __init__(self, script=None, **kw):
        """
        script can be a string with actual code or a file object.
        acceptable keyword arguments are 'request' and 'response',
        which should be weblib.Request and weblib.Response objects,
        respectively.
        """

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
                
            else:
                # use a new copy of the default (eg, self.auth=weblib.Auth())
                setattr(self, item,
                        weblib.__dict__[string.capitalize(item)](engine=self))



    def interceptPrint(self):
        """
        This replaces sys.stdout with the engine's response object.
        """
        import sys
        self.stdout = sys.stdout
        sys.stdout = self.response
       

    
    def restorePrint(self):
        """
        This restores sys.stdout after a call to interceptPrint.
        """
        import sys
        sys.stdout = self.stdout


    def startParts(self):
        """
        Starts all the internal parts.
        """
        self.response.start()


    def stopParts(self):
        """
        Calls stop for all the internal parts.
        """


    def injectParts(self):
        """
        Injects our parts into the weblib namespace.
        """
        self.globals["ENG"] = self
        self.globals["REQ"] = self.request
        self.globals["RES"] = self.response


    def restoreParts(self):
        """
        Restore the old weblib parts..
        """
        #@TODO: do I still need this now that weblib is out of the picture?

    def setPathInfo(self):
        if not self.request.environ.get("PATH_INFO"):        
            if (type(self.script) == type("")):
                self.request.environ["PATH_INFO"] = "UNKNOWN_SCRIPT.py"
            else:
                self.request.environ["PATH_INFO"] = self.script.name
        

    def start(self):
        self._exitstuff = []
        self.startParts()
        self.injectParts()
        self.setPathInfo()
        #self.interceptPrint()



    def stop(self):
        self._exit()
        #self.restorePrint()
        self.restoreParts()
        self.stopParts()


    def do_on_exit(self, func, *targs, **kargs):
        self._exitstuff.append((func, targs, kargs))

    def _exit(self):
        """
        run exit stuff.. based on python 2.0's atexit._run_exitfuncs()
        """
        while self._exitstuff:
            func, targs, kargs = self._exitstuff[-1]
            apply(func, targs, kargs)
            self._exitstuff.remove(self._exitstuff[-1])

    def _execute(self, script):
        """
        This is so you can restrict execution in a subclass if you like.
        """
        exec(script, self.globals, self.locals)

    def execute(self, script):
        """
        Call this to execute a chunk of code.
        """
        self.result = self.SUCCESS
        try:
            self._execute(script)
        except SystemExit:
            self.result = self.EXIT
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
        """
        Run the engine!
        """
        self.start()
        try:
            self.execute(self.script)
        finally:
            self.stop()
            
