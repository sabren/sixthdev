import payment
import urllib
import string
from M2Crypto import httpslib, SSL ## only until python 2 comes out 

class AuthorizeNetPayment(payment.AbstractPayment):
    """
    a Payment class for talking to Authorize.net servers
    """
    __super = payment.AbstractPayment
    __ver__="$Revision$"
    
    def __init__(self, **kwargs):
        self.__super.__init__(self, **kwargs)
        self._secureServer = "secure.authorize.net"
        self._securePage = "gateway/transact.dll"
        

    def charge(self, amount, description=""):
        """Charge the card..."""
        
        values = {

            ## first the AuthNet-required stuff:
            "x_Version": "3.0",
            "x_ADC_Delim_Data": "TRUE",
            "x_ADC_URL": "FALSE",
            
            ## then the Payment stuff:
            "x_login": self.merchant,
            "x_Card_Num": self.card,
            "x_Exp_date": self.expires,

            ## finally, the amount:
            "x_Amount": amount,
            "x_Description": description,
            }

        if self.test:
            values["x_Test_Request"] = "TRUE"

        content = self._submit(values)

        # now parse the results
        (responseCode,
         responseSubCode,
         responseReasonCode,
         responseReasonText,
         authCode,
         avsCode,
         transID) = string.split(content, ",")[:7]

        if responseCode == "1":
            self.result = payment.APPROVED
            self.error = None
        elif responseCode == "2":
            self.result = payment.DENIED
            self.error = responseReasonText
        else:
            self.result = payment.ERROR
            self.error = responseReasonText
            
