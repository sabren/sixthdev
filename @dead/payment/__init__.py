"""
python payment module
"""
__ver__="$Id$"

from Payment import *
from AuthorizeNetPayment import *

def create(which, **kwargs):
    """Factory routine for creating objects that implement the
    Payment interface. Given an account type (as a string),
    and various keyword args, creates an Payment object which
    can be used to charge, credit, etc a credit card....

    eg:

    >>> payment.create("AuthorizeNet",
    ...                card = "444444444444442")

    """

    import payment # grab this module's namespace
    
    if hasattr(payment, which + "Payment"):
        return apply(getattr(payment, which + "Payment"), (), kwargs)
    else:
        raise NameError, "No class named payment.%sPayment" % which
