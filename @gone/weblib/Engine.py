"""
A wrapper object for running weblib scripts.
"""
__ver__ = "$Id$"

import weblib
import string
import traceback
import sys
import os
import handy
from weblib import Finished

class Engine(object):

    SUCCESS   = "* success *"
    FAILURE   = "* failure *"
    EXCEPTION = "* exception *"
    REDIRECT  = "* redirect *"
    EXIT      = "* exit *"

    def __init__(self, script=None, request=None,
                 SITE_NAME=None, SITE_MAIL=None, **kw):
        """
        script can be a string with actual code or a file object.
        """
        self.script = script
        self.request = request or weblib.Request()
        self.response = None # until run()
        self.result = None
        self.error = None

        # set up internal namespaces..
        self.globals = {
            '__name__':'__main__',
            'SITE_NAME': SITE_NAME,
            'SITE_MAIL': SITE_MAIL,
        }
        self.locals  = self.globals

        # stuff to do at exit:
        self._exitstuff = []


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
        self.response = weblib.Response()
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
        This is in its own method so a subclass can restrict execution.
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
        except Finished:
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
            except Finished:
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
        # self.result is None if nothing's been run yet
        # it would be error or exception if dotWeblibPy had a problem
        if (self.result is None) or (self.result == self.SUCCESS):
            if os.path.exists(self.getScriptName()):
                self.execute(open(self.getScriptName()))
            else:
                self.stop()
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
        
    def sendError(self):
        SITE_MAIL = self.locals["SITE_MAIL"]
        SITE_NAME = self.locals["SITE_NAME"]
        assert SITE_MAIL is not None, "must define SITE_MAIL first!"
        hr = "-" * 50 + "\n"
        msg = weblib.trim(
            """
            To: %s
            From: weblib.cgi <%s>
            Subject: uncaught exception in %s

            """ % (SITE_MAIL, SITE_MAIL, SITE_NAME))
        msg += "uncaught exception in %s\n\n" % self.getScriptName()
        msg += hr
        msg += self.error
        msg += hr
        msg += "FORM: %s\n"  % self.request.form
        msg += "QUERYSTRING: %s\n" % self.request.querystring
        msg += "COOKIE: %s\n" % self.request.cookie

        if hasattr(self, "sess"):
            msg = msg + "SESSION DATA:\n"
            for item in self.sess.keys():
                msg += item + ': '
                try:
                    msg += self.sess[item] + "\n"
                except:
                    msg += "(can't unpickle)\n"
        else:
            msg += "NO SESSION DATA\n"
        msg += hr
        msg += "OUTPUT:\n\n"
        msg += self.response.getHeaders() + "\n"
        msg += self.response.buffer + "\n"
        msg += hr

        handy.sendmail(msg)

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
        if self.result in (self.SUCCESS, self.REDIRECT, self.EXIT):
            self.printResponse()
        else:
            self.errorPageHeader()
            if self.result == self.FAILURE:
                print "<b>assertion failure:</b>", self.error
            elif self.result == self.EXCEPTION:
                self.printException()
            self.printFooter()
            sys.stdout.flush()
            if self.locals["SITE_MAIL"]:
                self.sendError()
