"""
Wildcard - a simple class that is always equal to X for all X's
"""

class Wildcard:
    def __cmp__(self,other):
        return 0


