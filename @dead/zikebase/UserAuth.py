"""
UserAuth.py -- extends weblib.Auth to use User object.

$Id$
"""

import zikebase
import weblib

class UserAuth(weblib.Auth):

    def fetch(self, key):
        if key:
            self.user = zikebase.User(ID=key)
        else:
            self.user = None
    
    def validate(self, dict):
        key = None
        user = None

        if dict.has_key("username"):
            try:
                user = zikebase.User(username=dict["username"])
            except:
                pass
        elif dict.has_key("email"):
            try:
                user = zikebase.User(email=dict["email"])
            except:
                pass

        if user and (user.password == dict.get("password")):
            key = user.ID

        return key


    


