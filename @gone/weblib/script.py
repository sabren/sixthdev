"""
weblib.script - import this so that print = weblib.response.write()

$Id$
"""
import weblib

####### special classes that replace Engine ############

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


class ScriptSess(weblib.Sess):

    def __setitem__(self, name, value):

        """ We can't freeze once at the end, because
        garbage collection tends to cause all sorts
        of problems with freeze().. So, the only other
        alternative seems to be freezing every time
        we add something to the session... This is
        just another reason NOT to use CGI mode."""
        
        weblib.Sess.__setitem__(self, name, value)
        self.freeze()


### and now, the herd of singletons ##########################

weblib.request = weblib.Request()
weblib.response = ScriptResponse()

weblib.sess = ScriptSess(weblib.pool)
weblib.sess.start()

weblib.auth = weblib.Auth()
weblib.auth.start()

