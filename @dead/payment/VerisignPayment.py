"""
a Payment class for talking to Verisign (formerly signio)
"""
__ver__="$Id$"

import payment
import urllib
import string
from M2Crypto import httpslib, SSL ## only until python 2 comes out 

class VerisignPayment(payment.AbstractPayment):
    __super = payment.AbstractPayment
    
    def __init__(self, **kwargs):
        self.__super.__init__(self, **kwargs)
        self._secureServer = "payflowlink.verisign.com"
        self._securePage = "payflowlink.cfm"
        

    def charge(self, amount, description=""):
        """
        Charge the card...
        """

        assert type(self.merchant) == type(()), \
               "merchant should be a tuple of (login, partner) for verisign"

        assert not self.test, \
               "to test verisign, log into its managner and turn on test mode"

        values = {

            ## first the standard Verisign stuff:
            "TYPE": "S", # sale (not an authorization, which would be "A")
            "METHOD": "CC",
            "ORDERFORM": "False",
            "SHOWCONFIRM":"False",

            "NAME": self.name,
            "ADDRESS": self.address,
            "CITY": self.city,
            "STATE": self.state,
            "ZIP": self.zip,
            "COUNTRY": self.countryCD,
            "PHONE": self.phone,
            "FAX": self.fax,
            
            "LOGIN": self.merchant[0],
            "PARTNER": self.merchant[1],
            "CARDNUM": self.card,
            "EXPDATE": self.expires[:2] + self.expires[3:], # strip "/"
            
            ## finally, the amount:
            "AMOUNT": amount,
            "DESCRIPTION": description,
            }

        content = self._submit(values)
        open("vs.out","w").write(content)
        if content.find("<title>Declined") > -1:
            self.result = payment.DENIED
            self.error = "Unknown Reason" #@TODO: can I fix this?
        elif content.find("<title>Transaction Approved") > -1:
            self.result = payment.APPROVED
            self.error = None
        else:
            self.result = payment.ERROR
            self.error = "Unexpected results!"
