"""
Perm.py - emulate PHPLIB's permission support in python.

@TODO: license
"""

import weblib

class Perm:

    ## attributes #############################
    
    def __init__(self, engine=weblib):
        self.engine = engine
        if self.engine is weblib:
            weblib.perm = self
            
        self.perms = {}

    ## public methods #########################

    def check(required):
        pass

    def hasPerm(required):
        pass

    def perm_sel(): #@TODO: wtf?        
        pass
    
    ## internal methods #######################

    def _permsum(rights):
        pass

    def _perm_invalid(doeshave, musthave):
        pass


if __name__ == "__main__":
    pass
