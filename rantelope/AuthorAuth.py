"""
Authentication based on rantelope Author class
"""
__ver__="$Id$"

from sixthday import Auth
from rantelope import Author

class AuthorAuth(Auth):

    def __init__(self, sess, clerk):
        self.clerk = clerk
        Auth.__init__(self, sess, {})


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
    
