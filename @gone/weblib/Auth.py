"""
Auth.py - generic authentication framework for python cgi.
          loosely based on Auth.inc from PHPLIB...

@TODO: license, etc..
"""

class Auth:
    
    ## attributes #############################
    
    def __init__(self):
        self.isLoggedIn = 0
        pass

    ## public methods #########################

    def check(self):
        """Makes sure the user is authenticated. If not, prompts for credentials."""
        pass
    
    def login(self, key):
        """Force a login with the specified key."""
        pass

    def logout(self):
        """Logs out the current user."""
        pass

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
        pass

    def _getHidden():
        pass


if __name__ == "__main__":
    pass
