"""
UserAuth.py -- extends weblib.Auth to use User object.
"""

__ver__="$Id$"


import zikebase
import weblib

class UserAuth(weblib.Auth):

    zikebase.load("User")
    userClass = zikebase.User

    def __init__(self, sess):
        """
        usage: auth=UserAuth(sess)
        """
        self._sess = sess

    def fetch(self, key):
        if key:
            self.user = self.userClass(ID=key)
        else:
            self.user = None
    
    def validate(self, dict):
        key = None
        user = None

        if dict.has_key("username"):
            try:
                user = self.userClass(username=dict["username"])
            except:
                pass
        elif dict.has_key("email"):
            try:
                user = self.userClass(email=dict["email"])
            except:
                pass

        if user and (user.password == dict.get("password")):
            key = user.ID

        return key
