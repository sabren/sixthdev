"""
Auth.py - generic authentication framework for python cgi.
          loosely based on Auth.inc from PHPLIB...

@TODO: license, etc..
"""

import weblib

## messages ###################################

LOGINFAILED = 'Login failed.'
PLEASELOGIN = 'Please log in.'


## Auth class #################################

class Auth:

    ## constructor #############################
    
    def __init__(self, authKey=None, engine=weblib):

        self.engine = engine
        
        if authKey:
            self.isLoggedIn = 1
        else:
            self.isLoggedIn = 0

        self.key = authKey


    ## public methods #########################

    def check(self):
        """Makes sure the user is authenticated. If not, prompts for credentials."""
        
        if request.querystring.has_key('auth_logout_flag'):
            self.logout()

        if not self.isLoggedIn:
            if request.querystring.has_key('auth_check_flag'):
                if self._attemptLogin():
                    self.onLogin() # they're in!
                else:
                    self.prompt(LOGINFAILED, self._getAction(), self._getHidden())
                    response.end()
            else:
                self.prompt(PLEASELOGIN, self._getAction(), self._getHidden())
                response.end()

        else:
            self.fetch(self.key)
    

    def login(self, key):
        """Force a login with the specified key."""
        self.key = key
        self.onLogin()



    def logout(self):
        """Logs out the current user."""
        self.onLogout()
        self.key = None



    ## abstract methods ########################
    ## see DBAuth.py for an implementation #
    
    def fetch(self, key):
        pass # raise AbstractError ?


    def validate(self, dict):
        """This should test whether the credentials in dict are valid,
        and if so, return a key, else return None"""

        # example implementation for testing, based on form below:

        authKey = None

        if (dict["name"] == "username") and (dict["pass"] == "password"):
            authKey = 1 # user's key = 1


        return authKey

    def prompt(self, message, action, hidden):
        """This should show an HTML prompt and call response.end().
        You should overwrite this!"""

        response.write("""
        <h1>%s</h1>
        <form action="%s" method="post">
        username: <input type="text" name="auth_name"><br>
        password: <input type="password" name="auth_pass"><br>
        <input type="submit">
        %s
        </form>
        """ % (message, action, hidden))
        
        response.end()


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
        
        for item in request.form.keys():
            if item[:5] == "auth_":
                dict[item[5:]] = self.transform(item[5:], request.form[item])


        # now pass it to validate() and see if we get in:
        self.key = self.validate(dict)

        if self.key is not None:
            # should I automatically add it to session, or leave it decoupled?
            res = 1
            self.fetch(self.key)
                
        return res


    def _getAction(self):
        """Returns a string with the current URL and coded querystring.

        This is used for the ACTION property of the login form.
        """

        import weblib

        # start with a basic url (no query string)
        res = request.environ["PATH_INFO"]

        # add in a query string of our own:
        res = res + "?auth_check_flag=1"

        for item in request.querystring.keys():
            if item[:5] == "auth_":
                pass # IGNORE old auth stuff
            else:
                res = res + "&" + weblib.urlEncode(item) + \
                      "=" + weblib.urlEncode(request.querystring[item])
        
        return res

    

    def _getHidden(self):
        """This function builds a string containing hidden form fields.
        
        This is because the session could expire while someone is working
        on a form. If they post the form, they should get a login-box,
        but we want to remember their data while they're logging back in!
        """
        res = ""

        for item in request.form.keys():  # form really ought to be an IdxDict..
            if item[:5] == "auth_":
                pass # Ignore auth stuff here, too
            else:
                res = res + '<input type="hidden" name="' + \
                      weblib.htmlEncode(item) + '" value="' + \
                      weblib.htmlEncode(request.form[item]) + \
                      '">\n'

        return res


if __name__ == "__main__":
    pass
