"""
A wrapper object for running weblib scripts.
"""
__ver__ = "$Id$"

import weblib
import traceback
import sys
import os
import handy

class Engine(object):

    SUCCESS   = "* success *"
    FAILURE   = "* failure *"
    EXCEPTION = "* exception *"
    REDIRECT  = "* redirect *"
    EXIT      = "* exit *"

    def __init__(self, script=None,  request=None, path="."):
        """
        script should be a string with actual code.
        """
        self.script = script
        self.request = request or weblib.RequestBuilder().build()
        self.response = self.makeResponse()

        self.result = None
        self.error = None
        self.path = path
        self.makeGlobals()
        
        # stuff to do at exit:
        self._exitstuff = []
        self.setPathInfo()

    def makeGlobals(self):
        self.globals = {}
        self.globals['__name__']='__main__'
        self.globals['SITE_NAME']= None
        self.globals['SITE_MAIL']= None
        self.globals["ENG"] = self
        self.globals["REQ"] = self.request
        self.globals["RES"] = self.response

    def setPathInfo(self):
        """
        This (technology/app server specific) routine sets the
        PATH_INFO CGI variable.
        """
        #@TODO: should this really be PATH_INFO? how about SCRIPT_NAME?
        if not getattr(self.request, "pathInfo", None):
            if (type(self.script) == type("")):
                self.request.pathInfo = "UNKNOWN_SCRIPT.py"
            else:
                self.request.pathInfo = self.script.name


    def makeResponse(self):
        return weblib.Response()
    

    def do_on_exit(self, func, *targs, **kargs):
        """
        Register a callback for the end of page.
        """
        self._exitstuff.append((func, targs, kargs))

    def _exit(self):
        """
        run exit stuff.. based on python 2.0's atexit._run_exitfuncs()
        """
        while self._exitstuff:
            func, targs, kargs = self._exitstuff[-1]
            apply(func, targs, kargs)
            self._exitstuff.remove(self._exitstuff[-1])

    def _exec(self, script):
        """
        This is in its own method so a subclass can restrict execution.
        """
        exec(script, self.globals)

    def execute(self, script):
        """
        Call this to execute a chunk of code.
        """
        self.result = self.SUCCESS
        try:
            self.script = script
            self.setPathInfo() 
            self._exec(script)
        except weblib.Finished:
            self.result = self.EXIT
        except AssertionError, e:
            self.result = self.FAILURE
            self.error = e
        except weblib.Redirect, e:
            #@TODO: get rid of weblib.Redirect (gotta fix App first)
            self.result = self.REDIRECT
            try:
                where = str(e)
                if where[0]=="?":
                    raise Exception("can't redirect to ?xxx (%s)" % where)
                self.response.redirect(where)
            except weblib.Finished:
                pass
        except Exception, e:
            self.result = self.EXCEPTION
            self.exception = e
            self.error = "".join(traceback.format_exception(
                sys.exc_type,
                sys.exc_value,
                sys.exc_traceback))

    def chdir(self):
        os.chdir(self.path)

    def runDotWeblibPy(self):
        path = self.path + os.sep + ".weblib.py"
        if os.path.exists(path):
            # we use execute instead of run because we only want
            # to run the setup once.
            self.execute(open(path))

    def runScript(self):
        # self.result is None if nothing's been run yet
        # it would be error or exception if dotWeblibPy had a problem
        if (self.result is None) or (self.result == self.SUCCESS):
            self.execute(self.script)               

    def run(self):
        assert not self.result, "can't use an Engine more than once"
        self.chdir()
        self.runDotWeblibPy()
        self.runScript()
        self._exit()

    def hadProblem(self):
        assert self.result
        return self.result in (Engine.FAILURE, Engine.EXCEPTION)
