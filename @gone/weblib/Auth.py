"""
Auth.py - generic authentication framework for python cgi.
          loosely based on Auth.inc from PHPLIB...

$Id$

@TODO: license, etc..
"""

import weblib


## Auth class #################################

class Auth:

    LOGINFAILED = 'Login failed.'
    PLEASELOGIN = 'Please log in.'

    _isStarted = 0

    ## constructor #############################
    
    def __init__(self, engine=weblib):
        self.engine = engine
        self.engine.auth = self  #@TODO: ???????


    ## public methods #########################

    def start(self, key=None):
        """Must be called after the engine's session has started"""

        self._isStarted = 1
        self.isLoggedIn = 1 # assume the best

        if key:
            self.key = key
        elif self.engine.sess.has_key('__auth_key'):
            self.key = self.engine.sess['__auth_key']
        else:
            self.isLoggedIn = 0 # oh well.



    def check(self):
        """Makes sure the user is authenticated. If not, prompts for credentials."""

        if not self._isStarted:
            self.start()
        
        if self.engine.request.query.has_key('auth_logout_flag'):
            self.logout()

        if not self.isLoggedIn:
            if self.engine.request.query.has_key('auth_check_flag'):
                if self._attemptLogin():
                    self.onLogin() # they're in!
                else:
                    self.prompt(Auth.LOGINFAILED, self._getAction(), self._getHidden())
                    self.engine.response.end()
            else:
                self.prompt(Auth.PLEASELOGIN, self._getAction(), self._getHidden())
                self.engine.response.end()
        else:
            self.fetch(self.key) 
    

    def login(self, key):
        """Force a login with the specified key."""
        self.key = key
        self.onLogin()



    def logout(self):
        """Logs out the current user."""
        self.onLogout()
        self.isLoggedIn = 0
        self.key = None
        if self.engine.sess.has_key('__auth_key'):
            del self.engine.sess['__auth_key']
                    


    ## abstract methods ########################
    
    def fetch(self, key):
        pass # raise AbstractError ?


    def validate(self, dict):
        """This should test whether the credentials in dict are valid,
        and if so, return a key, else return None"""

        # example implementation for testing, based on form below:

        authKey = None
        if (dict.get("username") == "username") and (dict.get("password") == "password"):
            authKey = 1 # user's key = 1
        return authKey


    def prompt(self, message, action, hidden):
        """This should show an HTML prompt and call response.end().
        You should overwrite this!"""

        self.engine.response.write("""
        <h1>%s: %s</h1>
        <form action="%s" method="post">
        username: <input type="text" name="auth_username"><br>
        password: <input type="password" name="auth_password"><br>
        <input type="submit">
        %s
        </form>
        """ % (self.__class__.__name__, message, action, hidden))
        


    def transform(self, field, value):
        """Overwrite this if you want to eg, encode/encrypt credentials
        before passing to validate()"""

        return value



    ## events (overwritable) ##################

    def onLogin(self):
        pass

    def onLogout(self):
        pass
    
    ## internal methods #######################
    
    def _attemptLogin(self):
        """Gets stuff from the login form and passes it to validate.."""

        dict = {}
        res = 0

        # first move all the auth_* variables into a hash,
        # transforming them along the way.
        
        for item in self.engine.request.keys():
            if item[:5] == "auth_":
                dict[item[5:]] = self.transform(item[5:], self.engine.request[item])

        # now pass it to validate() and see if we get in:
        self.key = self.validate(dict)
        if self.key is not None:
            self.engine.sess['__auth_key'] = self.key
            self.fetch(self.key)
            res = 1
                
        return res


    def _getAction(self):
        """Returns a string with the current URL and coded querystring.

        This is used for the ACTION property of the login form.
        """

        import weblib

        # start with a basic url (no query string)
        # Either PATH_INFO (for wrapper) or SCRIPT_NAME (for CGI)
        # MUST be here. if it's not, you need to build it
        # into the environ for the current Engine.
        # can't even use a blank as default, because it'll
        # screw up in some browsers.. (eg, lynx)
        #
        # note: SCRIPT_NAME should always be there, but if you use the
        # wrapper, it will be the path to the wrapper, in which
        # case you want PATH_INFO...

        res = self.engine.request.environ.get("PATH_INFO", 
            self.engine.request.environ.get("SCRIPT_NAME", None))

        assert res is not None, \
               "You must set SCRIPT_NAME or PATH_INFO in the environment to use Auth."
        

        # add in a query string of our own:
        res = res + "?auth_check_flag=1"

        for item in self.engine.request.query.keys():
            if item[:5] == "auth_":
                pass # IGNORE old auth stuff
            else:
                res = res + "&" + weblib.urlEncode(item) + \
                      "=" + weblib.urlEncode(self.engine.request.query[item])
        
        return res

    

    def _getHidden(self):
        """This function builds a string containing hidden form fields.
        
        This is because the session could expire while someone is working
        on a form. If they post the form, they should get a login-box,
        but we want to remember their data while they're logging back in!
        """
        res = ""
        for item in self.engine.request.form.keys():  # form should be an IdxDict..
            if item[:5] == "auth_":
                pass # Ignore auth stuff here, too
            else:
                res = res + '<input type="hidden" name="' + \
                      weblib.htmlEncode(item) + '" value="' + \
                      weblib.htmlEncode(self.engine.request.form[item]) + \
                      '">\n'

        return res


if __name__ == "__main__":
    pass
