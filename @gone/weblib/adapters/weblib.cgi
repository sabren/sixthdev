#!c:/python22/python
"""
weblib.cgi : a wrapper script for weblib
inspired by http://www.webtechniques.com/archives/1998/02/kuchling/

USAGE (Apache):
   Action application/python-script /cgi-bin/weblib.cgi
   AddType application/python-script .py
"""

## CONFIGURATION ############################
        
SITE_MAIL = None # eg, webmaster@yoursite.com
SITE_NAME = None # eg, "yoursite intranet"

#############################################

import cgi
import os
import os.path
import string
import StringIO
import sys

def scriptDir():
    res = os.environ["PATH_TRANSLATED"] # full path to script
    res = res.split(os.sep)[:-1]        # split to remove filename
    res = os.sep.join(res)              # put back together
    return res
    
   
def fixWin32BinaryIssue():
    if sys.platform=="win32":
        import msvcrt
        msvcrt.setmode(sys.__stdin__.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)

if __name__=="__main__":

    try:
        import weblib
        fixWin32BinaryIssue()
        eng = weblib.Engine(SITE_MAIL=SITE_MAIL, SITE_NAME=SITE_NAME)
        eng.start()
        eng.setDir(scriptDir())
        eng.runDotWeblibPy()
        eng.runScript()
        eng.stop()        
        eng.printFullResponse()

    except Exception, e:
        print "content-type: text/plain\n"
        cgi.print_exception()

