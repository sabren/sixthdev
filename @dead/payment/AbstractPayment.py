import urllib

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
            

    def _submit(self, dict, page=None):
        """
        Given a dict of form variables, make the HTTPS POST.
        """
        if page:
            relurl = page
        else:
            relurl = self._securePage

        res = urllib.urlopen("https://%s/%s" % (self._secureServer, relurl),
                             urllib.urlencode(dict))
        return res.read()


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
        
