"""
UserAuth.py -- extends weblib.Auth to use User object.

$Id$
"""

import zikebase
import weblib.Auth

class UserAuth(weblib.Auth):

    def fetch(self, key):
        if key:
            self.user = zikebase.User(ID=key)
        else:
            self.user = None


    def prompt(self, message, action, hidden):
        """This should show an HTML prompt and call response.end().
        You should overwrite this!"""

        self.engine.response.write("""
        <h1>%s</h1>
        <form action="%s" method="post">
        username: <input type="text" name="auth_username"><br>
        password: <input type="password" name="auth_password"><br>
        <input type="submit">
        %s
        </form>
        """ % (message, action, hidden))

    
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


    


