"""
User.py - user object for zikebase

$Id$
"""

import zikebase
zikebase.load("Password")
import zdc

class User(zdc.RecordObject):
    _table = zdc.Table(zikebase.dbc, "base_user")
    _defaults = {}

    passwordClass = zikebase.Password


    # we want to encrypt the passwords transparently.

    def get_password(self):
        """returns a zikebase.Password object for testing against plaintext."""
        return self.passwordClass(self.__dict__["cryptedpass"])
    
    def set_password(self, value):
        "user.password = 'whatever'  # Transparently encrypt the password"
        pw = self.passwordClass()
        pw.set(value)
        self.__dict__["cryptedpass"] = pw.crypted
        
