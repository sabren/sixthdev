"""
python payment module
"""
__ver__="$Id$"

from Payment import *
from AuthorizeNetPayment import *

## result codes (constants)

APPROVED = "approved"
DENIED = "denied"
ERROR = "error"



## utility functions

def create(which, **kwargs):
    """Factory routine for creating objects that implement the
    Payment interface. Given an account type (as a string
    corresponding to a classname without the -Payment suffix),
    and various keyword arguments, creates an Payment object which
    can be used to charge, credit, etc a credit card....

    eg:

    >>> payment.create("AuthorizeNet",
    ...                card = "4222222222222")

    """

    import payment # grab this module's namespace
    
    if hasattr(payment, which + "Payment"):
        return apply(getattr(payment, which + "Payment"), (), kwargs)
    else:
        raise NameError, "No class named payment.%sPayment" % which
