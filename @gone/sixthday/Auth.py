"""
Auth.py - generic authentication framework for python cgi.
"""
__ver__ = "$Id$"

#@TODO: license, etc..
import weblib

## Auth class #################################

class Auth:
    """
    Generic Authentication class for the web. This is loosely
    based on Auth.inc from PHPLIB.
    """

    LOGINFAILED = 'Login failed.'
    PLEASELOGIN = 'Please log in.'

    _isStarted = 0

    ## constructor #############################
    
    def __init__(self, sess, userdict):
        """
        usage: auth=Auth(sess, userdict)
        where userdict is like {'usr1':'pwd1','usr2':'pwd2'...}
        """
        self._sess = sess
        self._users = userdict


    ## public methods #########################

    def start(self, key=None):
        #@TODO: is there any reason why this shouldn't be in __init__?

        self._isStarted = 1
        self.isLoggedIn = 1 # assume the best

        if key:
            self.key = key
        elif self._sess.has_key('__auth_key'):
            self.key = self._sess['__auth_key']
        else:
            self.isLoggedIn = 0 # oh well.

    def check(self):
        """
        Make sure the user is authenticated.
        If not, prompt for credentials.
        """

        if not self._isStarted:
            self.start()
        
        if self._sess._request.query.has_key('auth_logout_flag'):
            self.logout()

        if not self.isLoggedIn:
            if self._sess._request.query.has_key('auth_check_flag'):
                if self._attemptLogin():
                    self.onLogin() # they're in!
                else:
                    self.prompt(Auth.LOGINFAILED, self._getAction(),
                                self._getHidden())
                    self._sess._response.end()
            else:
                self.prompt(Auth.PLEASELOGIN, self._getAction(),
                            self._getHidden())
                self._sess._response.end()
        else:
            self.login(self.key) 
    

    def login(self, key):
        """
        Force a login with the specified key.
        """
        self.key = key
        self.fetch(self.key)
        self._sess['__auth_key'] = self.key
        self.onLogin()

                
    def logout(self):
        """
        Logs out the current user.
        """
        self.onLogout()
        self.isLoggedIn = 0
        self.key = None
        if self._sess.has_key('__auth_key'):
            del self._sess['__auth_key']
                    


    ## abstract methods ########################
    
    def fetch(self, key):
        pass # raise AbstractError ?


    def validate(self, dict):
        """
        This should test whether the credentials in dict are valid,
        and if so, return a key, else return None
        """

        # example implementation for testing, based on form below:

        authKey = None
        if (dict.get("username") in self._users.keys()) \
           and (dict.get("password") == self._users[dict["username"]]):
            authKey = dict["username"]
        return authKey


    def prompt(self, message, action, hidden):
        """
        This should show an HTML prompt and call response.end().
        You should overwrite this!
        """

        self._sess._response.write("""
        <h1>%s: %s</h1>
        <form action="%s" method="post">
        username: <input type="text" name="auth_username"><br>
        password: <input type="password" name="auth_password"><br>
        <input type="submit">
        %s
        </form>
        """ % (self.__class__.__name__, message, action, hidden))
        


    def transform(self, field, value):
        """
        Overwrite this if you want to eg, encode/encrypt credentials
        before passing to validate()
        """

        return value



    ## events (overwritable) ##################

    def onLogin(self):
        """
        overwritable onLogin event.
        """
        pass

    def onLogout(self):
        """
        overwritable onLogout event.
        """
        pass

    
    ## internal methods #######################
    
    def _attemptLogin(self):
        """
        Gets stuff from the login form and passes it to validate..
        """

        dict = {}
        res = 0

        # first move all the auth_* variables into a hash,
        # transforming them along the way.
        
        for item in self._sess._request.keys():
            if item[:5] == "auth_":
                dict[item[5:]] = self.transform(item[5:],
                                                self._sess._request[item])

        # now pass it to validate() and see if we get in:
        self.key = self.validate(dict)
        if self.key is not None:
            self.login(self.key)
            res = 1

        return res


    def _getAction(self):
        """
        Returns a string with the current URL and coded querystring.
        This is used for the ACTION property of the login form.
        """
        import weblib
        res = self._sess._request.path + "?auth_check_flag=1"
        for item in self._sess._request.query.keys():
            if item[:5] == "auth_":
                pass # IGNORE old auth stuff
            else:
                res = res + "&" + weblib.urlEncode(item) + \
                      "=" + weblib.urlEncode(self._sess._request.query[item])
        return res

    

    def _getHidden(self):
        """
        This function builds a string containing hidden form fields.
        
        This is because the session could expire while someone is working
        on a form. If they post the form, they should get a login-box,
        but we want to remember their data while they're logging back in!
        """
        res = ""
        for item in self._sess._request.keys():
            # form should be an IdxDict..
            if item[:5] == "auth_":
                pass # Ignore auth stuff here, too
            else:
                # value should either be a string or a tuple
                # of strings. (for multi-select boxes or whatever)
                if type(self._sess._request[item]) == type(()):
                    # for tuples, loop through all the values:
                    for subitem in self._sess._request[item]:
                        res = res + '<input type="hidden" name="' + \
                              weblib.htmlEncode(item) + '" value="' + \
                              weblib.htmlEncode(subitem) + \
                              '">\n'
                elif item != 'weblib.Sess': #@TODO: is this right?
                    # only one value:
                    res += '<input type="hidden" name="'
                    res += weblib.htmlEncode(item) + '" value="'
                    res += weblib.htmlEncode(str(self._sess._request[item]))
                    res += '">\n'
                else:
                    pass

        return res
