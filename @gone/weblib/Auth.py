"""
Auth.py - generic authentication framework for python cgi.
          loosely based on Auth.inc from PHPLIB...

@TODO: license, etc..
"""

from weblib import request, response, session


## messages ###################################

LOGINFAILED = 'Login failed.'
PLEASELOGIN = 'Please log in.'



## Auth class #################################

class Auth:

    count = 0
    
    ## constructor #############################
    
    def __init__(self):
        if self.__class__.count:
            raise "SingletonError"
        else:
            self.__class__.count = 1
            
            if session.has_key("auth_key") and session["auth_key"]:
                self.isLoggedIn = 1
            else:
                self.isLoggedIn = 0


    ## public methods #########################

    def check(self):
        """Makes sure the user is authenticated. If not, prompts for credentials."""
        
        if request.querystring['auth_logout_flag']:
            self.logout()

        if not self.isLoggedIn:
            if request.querystring['auth_check_flag']:
                if self._attemptLogin():
                    self.onLogin() # they're in!
                else:
                    self.prompt(LOGINFAILED, self._getAction(), self._getHidden())
                    response.end()
            else:
                self.prompt(PLEASELOGIN, self._getAction(), self._getHidden())
                response.end()

        else:
            self.fetch(session["auth_key"])

    

    def login(self, key):
        """Force a login with the specified key."""
        session["auth_key"] = key
        self.onLogin()



    def logout(self):
        """Logs out the current user."""
        self.onLogout()
        del session["auth_key"]



    ## abstract methods ########################
    
    def fetch(self, key):
        raise "Fetch is an abstract function. You need to subclass Auth."

    def validate(self, dict):
        raise

    def prompt(self, msg, action, hidden):
        raise

    def encode(self, field, value):
        pass

    ## events (overwritable) ##################

    def onLogin(self):
        pass

    def onLogout(self):
        pass
    
    ## internal methods #######################
    
    def _attemptLogin():
        pass


    def _getAction():
        """Returns a string with the current URL and coded querystring.

        This is used for the ACTION property of the login form.
        """

        # start with a basic url (no query string)
        res = request.environ["PATH_INFO"]

        # add in a query string of our own:
        res = res + "?auth_check_flag=1"

        for i in request.querystring:
            if i[:5] == "auth_":
                pass # IGNORE old auth stuff
            else:
                res = res + "&" + weblib.urlEncode(i) + \
                      "=" + weblib.urlEncode(request.querystring[i])
        
        return res

    

    def _getHidden():
        """This function builds a string containing hidden form fields.
        
        This is because the session could expire while someone is working
        on a form. If they post the form, they should get a login-box,
        but we want to remember their data while they're logging back in!
        """
        res = ""

        for i in request.form:
            if i[:5] == "auth_":
                pass # Ignore auth stuff here, too
            else:
                res = res + '<input type="hidden" name="' + \
                      weblib.htmlEncode(i) + '" value="' + \
                      weblib.htmlEncode(request.form[i]) + \
                      '">\n'

        return res


if __name__ == "__main__":
    pass
