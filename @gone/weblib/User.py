"""
User.py - emulate PHPLIB's user-session support in python.

$Id$

@TODO: license
"""

from weblib import Sess

class User(Sess.Sess):

    ## attributes #############################
    
    def __init__(self):
        Sess.__init__(self)

    ## public methods #########################
    
    ## internal methods #######################


if __name__ == "__main__":
    pass

