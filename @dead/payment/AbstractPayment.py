"""
base class / interface definition for payment objects
"""
__ver__="$Id$"


class AbstractPayment:
    """A base class for Payment objects.."""
    
    def __init__(self, **kwargs):

        self.card = "" # card number
        self.merchant = "" # merchant's ID
        self.expires = "" #
        self.name = ""
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.countryCD = "USA"
        self.phone = ""
        self.fax = ""

        self.test = 0

        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
            


