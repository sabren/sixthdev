#!c:\python20\python
#
# weblib.cgi : a wrapper script for weblib
# inspired by http://www.webtechniques.com/archives/1998/02/kuchling/
#
# USAGE:
#
# Either do #!/your_path/weblib.cgi at the top of your CGI script,
# or save this in your cgi-bin, and do this in your Apache .htaccess file:
#
# Action application/python-script /cgi-bin/weblib.cgi
# AddType application/python-script .py


## debugging help ################################################
## you can uncomment this temporarily if you need help 
## debugging Internal Server Errors..

## import sys
## print "content-type: text/plain"
## print
## sys.stderr = sys.stdout

## profiling #####################################################
## set this to 1 if you want profiling, 0 if you don't.
doProfile = 0

## email notifcation of errors ###################################
## If uncaught exceptions occur, email will be sent to SITE_MAIL
## with SITE_NAME in the subject line.
## You can redefine these in .weblib.py if you like.
##
SITE_MAIL = None # eg, webmaster@yoursite.com
SITE_NAME = None # eg, "bubbaCo intranet"


###############################################################
## you shouldn't have to edit anything below this line       ##
###############################################################

## import required modules #######################################
import os.path, sys, string, weblib, StringIO

## allow imports from script directory ###########################

path = os.environ["PATH_TRANSLATED"]
dir = string.join(string.split(path,os.sep)[:-1], os.sep)
sys.path.append(dir)
import os
os.chdir(dir)

## handle binary mode issues for stdio on win32:
import os, sys
if sys.platform=="win32":
    import msvcrt
    msvcrt.setmode(sys.__stdin__.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)

## build the engine ##############################################
if doProfile:
    class ProfileEngine(weblib.Engine):
        '''
        an engine that profiles your script (and .weblib.py)
        '''
        __super=weblib.Engine
        def __init__(self, script=None, pool=None, **kw):
            apply(self.__super.__init__, (self, script, pool), kw)
            import profile
            self.prof = profile.Profile()
        def _execute(self, script):
            self.prof.runctx("exec(script, self.globals, self.locals)",
                             globals(), locals())
        def stop(self):
            self.__super.stop(self)
            import sys, cStringIO, pstats
            stats = cStringIO.StringIO()
            oldout, sys.stdout = sys.stdout, stats
            p = pstats.Stats(self.prof)
            p.sort_stats('time').print_stats(50) # only 50 slowest ones
            p.print_callers(10) # who called the 10 slowest ones?
            p.print_callees(10) # what did the 10 slowest ones call?
            self.stats = stats.getvalue()
            sys.stdout = oldout
    eng = ProfileEngine()
else:
    eng = weblib.Engine()
eng.start()
eng.locals["SITE_MAIL"]=SITE_MAIL
eng.locals["SITE_NAME"]=SITE_NAME

## run .weblib.py ################################################

whichfile = dir+os.sep+".weblib.py"
if os.path.exists(whichfile):
    # we use execute instead of run because we only want
    # to run the setup once.
    eng.execute(open(whichfile))


## run the script ################################################

# eng.result is None if nothing's been run yet
if (eng.result is None) or (eng.result == eng.SUCCESS):
    whichfile = os.environ["PATH_TRANSLATED"]
    if os.path.exists(whichfile):
        eng.execute(open(whichfile))
    else:
        eng.stop()
        print "Status: 404"
        sys.exit()

## close down shop and show the results  ########################
eng.stop()
SITE_MAIL=eng.locals["SITE_MAIL"]
SITE_NAME=eng.locals["SITE_NAME"]

if eng.result in (eng.SUCCESS, eng.EXIT):
    ## print the results
    print eng.response.getHeaders() + eng.response.buffer
    if doProfile:
        print '<br/>'
        print '<pre style="color: black; background:#99ccff;' \
              'padding:5px;'\
              'font-size:90%;'\
              'font-family:lucida console,courier new,courier;' \
              'border:solid black 1px;">'
        print eng.stats
        print "</pre>"
else:
    ## print debug output
    print "Content-Type: text/html"
    print
    print weblib.trim("""
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

    if eng.result == eng.FAILURE:
        print "<b>assertion failure:</b>", eng.error
        print "</body>\n</html>"

    elif eng.result == eng.EXCEPTION:

        ## html error message #################################

        print "<b>uncaught exception while running %s</b><br>" \
              % whichfile
        print '<pre class="traceback">' \
              + weblib.htmlEncode(eng.error) + "</pre>"

        print "<b>script input:</b>"

        print '<ul>'
        print '<li>form: %s</li>' % eng.request.form
        print '<li>querystring: %s</li>' % eng.request.querystring
        print '<li>cookie: %s</li>' % eng.request.cookie
        print '</ul>'

	print '<b>session data:</b><br>'
        print '<ul>'

	for item in eng.sess.keys():
            print '<li>', item, ': '
            try:
               print eng.sess[item]
            except:
               print '(can\'t unpickle)'
	    print '</li>'
        print '</ul>'
	
        print "<b>script output:</b>"
        print '<pre class="output">' + \
              weblib.htmlEncode(eng.response.getHeaders()) + \
              weblib.htmlEncode(eng.response.buffer) + \
              "</pre>"

    print "<hr>"
    print '<a href="http://weblib.sourceforge.net/">weblib</a> ' + \
          '(c) copyright 2000-2001 ' + \
          '<a href="http://www.zike.net/">Zike Interactive</a>. ' + \
          'All rights reserved.'
    print "</body>"
    print "</html>"

    import sys
    sys.stdout.flush()

    ## email error message ################################
    if (SITE_MAIL) and (eng.result==eng.EXCEPTION):
        hr = "-" * 50 + "\n"
        msg = weblib.trim(
            """
            To: %s
            From: weblib.cgi <%s>
            Subject: uncaught exception in %s

            """ % (SITE_MAIL, SITE_MAIL, SITE_NAME))
        msg = msg + "uncaught exception in %s\n\n" % whichfile
        msg = msg + hr
        msg = msg + eng.error
        msg = msg + hr
        msg = msg + "FORM: %s\n"  % eng.request.form
        msg = msg + "QUERYSTRING: %s\n" % eng.request.querystring
        msg = msg + "COOKIE: %s\n" % eng.request.cookie
        msg = msg + "SESSION DATA:\n"
        for item in eng.sess.keys():
            msg = msg + item + ': '
            try:
                msg = msg + eng.sess[item] + "\n"
            except:
                msg = msg + "(can't unpickle)\n"
        msg = msg + hr
        msg = msg + "OUTPUT:\n\n"
        msg = msg + eng.response.getHeaders() + "\n"
        msg = msg + eng.response.buffer + "\n"
        msg = msg + hr

        from weblib.handy import sendmail
        sendmail(msg)
