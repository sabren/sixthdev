"""
A rantelope user
"""
__ver__="$Id$"

from strongbox import *
import crypt

class Author(Strongbox):
    ID = attr(long, default=None)
    username = attr(str)
    cryptpwd = attr(str)
    
    def set_password(self, value):
        #@TODO: randomize the crypt salt
        self.cryptpwd = crypt.crypt(value, "xx")
    def get_password(self, value):
        raise ValueError, "passwords are encrypted"
    def isPassword(self, value):
        return self.cryptpwd == crypt.crypt(value, self.cryptpwd[:2])
