"""
Authentication based on rantelope Author class
"""
__ver__="$Id$"

from sixthday import Auth
from rantelope import Author
import zebra

class AuthorAuth(Auth):

    def __init__(self, sess, clerk):
        self.clerk = clerk
        Auth.__init__(self, sess, {})

    def prompt(self, message, action, hidden):
        model = {"message": message,
                 "action": action,
                 "hidden": hidden, }
        #@TODO: make this return a string
        self._sess._response.write(zebra.fetch("login", model))
        

    def fetch(self, key):
        #@TODO: need to define strict semantics for *Auth.fetch()
        self.user = self.clerk.fetch(Author, key)
        return self.user

    def validate(self, dict):
        res = None
        match = self.clerk.match(Author, username=dict.get("username"))
        assert len(match) < 2, "wtf? multiple Authors with this username!"
        if match and match[0].isPassword(dict.get("password")):
            res = match[0].ID
        return res
    
