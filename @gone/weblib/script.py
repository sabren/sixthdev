"""
weblib.script - import this so that print = weblib.response.write()

$Id$
"""
import weblib

class ScriptResponse(weblib.Response):
    """In CGI-mode, we want to insert headers automatically..."""

    def __init__(self):
        import sys
        weblib.Response.__init__(self, out=sys.stdout)
        sys.stdout = self


    def __del__(self):
        self.flush()
        import sys
        sys.stdout = self.out


### and now, the herd of singletons ##########################

weblib.request = weblib.Request()
weblib.response = ScriptResponse()

weblib.sess = weblib.Sess(weblib.pool)
weblib.auth = weblib.Auth()
weblib.perm = weblib.Perm()
