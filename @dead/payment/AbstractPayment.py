import urllib
from M2Crypto import httpslib, SSL ## only until python 2 comes out 

class AbstractPayment:
    """
    An Abstract base class for Payment objects.
    """
    __ver__="$Revision$"
    
    def __init__(self, **kwargs):
        """
        Your subclass should call this, and also set
        self._secureServer (https://_____________/)
        self._securePage (https://whatever/__________)
        """

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
            

    def _submit(self, dict, headers=[]):
        """
        Given a dict of form variables, make the HTTPS POST.
        """
        data = urllib.urlencode(dict)

        h = httpslib.HTTPS(self._secureServer)
        h.putrequest('POST', "/" + self._securePage)
        h.putheader('Content-type', 'application/x-www-form-urlencoded')
        h.putheader('Content-length', '%d' % len(data))
        for head in headers:
            h.putheader(*head)
        h.endheaders()
        h.send(data)

        errcode, errmsg, headers = h.getreply()
        assert errcode==200, \
               "problem reading from %s: %s, %s" \
               % (self._secureServer, errcode, errmsg)
        fp = h.getfile()

        content = ""
        chunk = "start"
        while len(chunk) != 0:
            chunk = fp.read()
            content += chunk
        fp.close()

        return content


    def charge(self, amount, description=""):
        """
        Abstract method: define this to charge customers
        """
        raise NotImplementedError

    def authorize(self):
        """
        Abstract method: define this to authorize charges
        """
        raise NotImplementedError

    def credit(self, amount, description=""):
        """
        Abstract method: define this to refund charges
        """
        raise NotImplementedError
        
