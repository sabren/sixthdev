"""
A wrapper object for running weblib scripts.
"""
__ver__ = "$Id$"

import weblib
import string
import traceback
import sys
import os

class Engine(object):
    
    parts=("request", "response")

    script = None
    result = None
    
    traceback = None
    error     = None

    SUCCESS   = "* success *"
    FAILURE   = "* failure *"
    EXCEPTION = "* exception *"
    REDIRECT  = "* redirect *"
    EXIT      = "* exit *"
      

    def __init__(self, script=None, SITE_NAME=None, SITE_MAIL=None, **kw):
        """
        script can be a string with actual code or a file object.
        acceptable keyword arguments are 'request' and 'response',
        which should be weblib.Request and weblib.Response objects,
        respectively.
        """

        # set up internal namespaces..
        self.globals = {
            '__name__':'__main__',
            'SITE_NAME': SITE_NAME,
            'SITE_MAIL': SITE_MAIL,
        }
        self.locals  = self.globals
        self.script = script       
        self._exitstuff = []

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
            else:
                # use new copy as default (eg, self.request=weblib.Request())
                setattr(self, item, weblib.__dict__[string.capitalize(item)]())



    def injectParts(self):
        """
        Injects our parts into the weblib namespace.
        """
        self.globals["ENG"] = self
        self.globals["REQ"] = self.request
        self.globals["RES"] = self.response


    def setPathInfo(self):
        """
        This (technology/app server specific) routine sets the
        PATH_INFO CGI variable.
        """
        #@TODO: should this really be PATH_INFO? how about SCRIPT_NAME?
        if not self.request.environ.get("PATH_INFO"):        
            if (type(self.script) == type("")):
                self.request.environ["PATH_INFO"] = "UNKNOWN_SCRIPT.py"
            else:
                self.request.environ["PATH_INFO"] = self.script.name
        

    def start(self):
        """
        Start the Engine
        """
        self.response.start()
        self.injectParts()
        self.setPathInfo()

    def stop(self):
        """
        Stop the Engine
        """
        self._exit()

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
            self.script = script
            self.setPathInfo() 
            self._execute(script)
        except SystemExit:
            self.result = self.EXIT
        except AssertionError, e:
            self.result = self.FAILURE
            self.error = e
        except weblib.Redirect, e:
            self.result = self.REDIRECT
            try:
                where = str(e)
                if where[0]=="?":
                    self.response.redirect(
                        self.request.environ["PATH_INFO"] + where)
                else:
                    self.response.redirect(where)
            except SystemExit:
                pass
        except:
            self.result = self.EXCEPTION            
            self.error = string.join(traceback.format_exception(
                sys.exc_type,
                sys.exc_value,
                sys.exc_traceback), '')


    def setDir(self, directory):
        self.directory = directory
        if not directory in sys.path:
            sys.path.append(directory) # @TODO: Shouldn't chdir be enough?
        os.chdir(directory)            # @TODO: this should be elsewhere.

    def runDotWeblibPy(self):
        path = self.directory + os.sep + ".weblib.py"
        if os.path.exists(path):
            # we use execute instead of run because we only want
            # to run the setup once.
            self.execute(open(path))


    def getScriptName(self):
        return os.environ["PATH_TRANSLATED"]

    def runScript(self):
        eng = self
        # eng.result is None if nothing's been run yet
        # it would be error or exception if dotWeblibPy had a problem
        if (eng.result is None) or (eng.result == eng.SUCCESS):
            if os.path.exists(self.getScriptName()):
                eng.execute(open(self.getScriptName()))
            else:
                eng.stop()
                print "Status: 404"
                sys.exit()


    def run(self): # @TODO: is this ever actually used?
        self.start()
        try:
            self.execute(self.script)
        finally:
            self.stop()

    def printResponse(self):
        print self.response.getHeaders() + self.response.buffer


    ## ERROR HANDLING @TODO: test cases for these!
        
    def sendError(eng):
        assert self.SITE_MAIL, "must define SITE_MAIL first!"
        hr = "-" * 50 + "\n"
        msg = weblib.trim(
            """
            To: %s
            From: weblib.cgi <%s>
            Subject: uncaught exception in %s

            """ % (self.SITE_MAIL, self.SITE_MAIL, self.SITE_NAME))
        msg = msg + "uncaught exception in %s\n\n" % self.getScriptName()
        msg = msg + hr
        msg = msg + self.error
        msg = msg + hr
        msg = msg + "FORM: %s\n"  % self.request.form
        msg = msg + "QUERYSTRING: %s\n" % self.request.querystring
        msg = msg + "COOKIE: %s\n" % self.request.cookie
        msg = msg + "SESSION DATA:\n"
        for item in self.sess.keys():
            msg = msg + item + ': '
            try:
                msg = msg + self.sess[item] + "\n"
            except:
                msg = msg + "(can't unpickle)\n"
        msg = msg + hr
        msg = msg + "OUTPUT:\n\n"
        msg = msg + self.response.getHeaders() + "\n"
        msg = msg + self.response.buffer + "\n"
        msg = msg + hr

        from weblib.handy import sendmail
        sendmail(msg)

    def printException(self):
        print "<b>uncaught exception while running %s</b><br>" \
              % self.getScriptName()
        print '<pre class="traceback">' \
              + weblib.htmlEncode(self.error) + "</pre>"
        print "<b>script input:</b>"
        print '<ul>'
        print '<li>form: %s</li>' % self.request.form
        print '<li>querystring: %s</li>' % self.request.querystring
        print '<li>cookie: %s</li>' % self.request.cookie
        print '</ul>'

        if self.globals.has_key("SESS"):
            print '<b>session data:</b><br>'
            print '<ul>'

            for item in self.globals["SESS"].keys():
                print '<li>', item, ': '
                try:
                   print self.globals["SESS"][item]
                except:
                   print '(can\'t unpickle)'
                print '</li>'
            print '</ul>'

        print "<b>script output:</b>"
        print '<pre class="output">' + \
              weblib.htmlEncode(self.response.getHeaders()) + \
              weblib.htmlEncode(self.response.buffer) + \
              "</pre>"

    def errorPageHeader(self):
        print "Content-Type: text/html"
        print
        print weblib.trim(
            """
            <html>
            <head>
            <title>weblib.cgi exception</title>
            <style type="text/css">
                body, p {
                   background: #cccccc;
                   font-family: verdana, arial;
                   font-size: 75%;
                }
                pre { font-size: 120%; }
                pre.traceback { color: red; }
                pre.output{ color : green }
            </style>
            </head>
            <body>
            """)


    def printFooter(self):
        print "<hr>"
        print '<a href="http://www.sixthdev.com/wiki.cgi/weblib/">weblib</a>'
        print '(c) copyright 2000-2002 '
        print '<a href="http://www.sabren.com/">Sabren Enterprises, Inc</a>. '
        print 'All rights reserved.'
        print "</body>"
        print "</html>"

    def printFullResponse(self):        
        eng = self
        SITE_MAIL=eng.locals["SITE_MAIL"]
        SITE_NAME=eng.locals["SITE_NAME"]
        if eng.result in (eng.SUCCESS, eng.REDIRECT, eng.EXIT):
            eng.printResponse()
        else:
            eng.errorPageHeader()
            if eng.result == eng.FAILURE:
                print "<b>assertion failure:</b>", eng.error
            elif eng.result == eng.EXCEPTION:
                eng.printException()
            eng.printFooter()
            sys.stdout.flush()
            if (SITE_MAIL):
                self.sendError(eng, SITE_MAIL, SITE_NAME)
