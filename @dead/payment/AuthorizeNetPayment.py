"""
a Payment class for talking to Authorize.net servers
"""
__ver__="$Id$"

import payment
import urllib
import string
from M2Crypto import httpslib, SSL ## only until python 2 comes out 

class AuthorizeNetPayment(payment.Payment):

    def _submit(self, dict):
        """Given a dict of form variables, makes the HTTP POST..."""
        data = urllib.urlencode(dict)

        h = httpslib.HTTPS(SSL.Context("sslv3"), "secure.authorize.net")
        h.putrequest('POST',"/gateway/transact.dll") 
        h.putheader('Content-type', 'application/x-www-form-urlencoded')
        h.putheader('Content-length', '%d' % len(data))
        h.endheaders()
        h.send(data)

        errcode, errmsg, headers = h.getreply()
        assert errcode==200, \
               "problem reading from authorize.net: %s, %s" \
               % (errcode, errmsg)
        fp = h.getfile()

        content = fp.read()
        fp.close()

        return content


        

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
            "x_Exp_date": "0101",
            

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
            
         
        
