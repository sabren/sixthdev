#!/usr/bin/python
"""
weblib.cgi : a wrapper script for weblib
inspired by http://www.webtechniques.com/archives/1998/02/kuchling/

USAGE (Apache):
   Action application/python-script /cgi-bin/weblib.cgi
   AddType application/python-script .py
"""
## import sys
## sys.stderr = sys.stdout
## print "content-type: text/plain"
## print


## CONFIGURATION ############################
        
SITE_MAIL = None # eg, webmaster@yoursite.com
SITE_NAME = None # eg, "yoursite intranet"

## use this to add custom lib directories:
import sys
sys.path = ["/web/lib"] + sys.path

#############################################

import cgi
import os
import os.path
import string
import StringIO

    
def fixWin32BinaryIssue():
    if sys.platform=="win32":
        import msvcrt
        msvcrt.setmode(sys.__stdin__.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)

if __name__=="__main__":

    try:  
        import weblib
        fixWin32BinaryIssue()
        
        path, filename = os.path.split(os.environ["PATH_TRANSLATED"])
        os.chdir(path)
        script = open(filename).read()
        
        req = weblib.RequestBuilder().build()
        eng = weblib.Engine(script, req, SITE_MAIL, SITE_NAME)
        
        eng.start()
        eng.setDir(path)
        eng.runDotWeblibPy()
        eng.runScript()
        eng.stop()        
        eng.printFullResponse() # ick!
        

    except Exception, e:
        print "content-type: text/plain\n"
        cgi.print_exception()
