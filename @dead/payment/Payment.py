"""
base class / interface definition for payment objects
"""
__ver__="$Id$"


class Payment:
    """A base class for Payment objects.."""

    card = "" # card number
    merchant = "" # merchant's ID
    expires = "" #

    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
            


