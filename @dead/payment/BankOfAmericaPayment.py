import payment

class BankOfAmericaPayment(payment.AbstractPayment):
    """
    a Payment class for talking to Bank of America's Settle Up service.
    http://www.estoressolutions.com/developersguide/
    """
    __ver__="$Revision$"
    __super = payment.AbstractPayment

    def __init__(self, **kwargs):
        
        self.customerid = ""
        self.username = ""
        self.password = ""
        self.orderid = "" # unique order id, to prevent duplicates
        self.address2 = ""
        self.email = ""
        self.referer = "" # only certain sites can post..
        self.handshake = "" # another unique id... sheesh
        self.fname = ""
        self.lname = ""
        
        self.__super.__init__(self, **kwargs)
        self._secureServer = "cart.bamart.com"
        self._securePage = "payment.mart"


    def _parse(self, content):
        resdict = {}
        # result is key=value pairs..
        # there's a <BR> after each line, including the last, so...
        for item in content.split("<BR>")[:-1]:
            key, val = item.split("=", 1)
            resdict[key.lower()]=val
        return resdict

        

    def authorize(self, amount):
        values = {

            "ioc_merchant_id": self.merchant,
            "ioc_order_total_amount": amount,
            "ioc_merchant_shopper_id": self.customerid,
            "ioc_merchant_order_id": self.orderid,
            
            "ecom_payment_card_name": self.name,
            "ecom_payment_card_number": self.card,
            "ecom_payment_card_expdate_month": self.expires[:2],
            "ecom_payment_card_expdate_year": self.expires[3:],

            "ecom_billto_postal_name_first": self.fname,
            "ecom_billto_postal_name_last": self.lname,

            "ecom_billto_postal_street_line1": self.address,
            "ecom_billto_postal_street_line2": self.address2,
            "ecom_billto_postal_city": self.city,
            "ecom_billto_postal_stateprov": self.state,
            "ecom_billto_postal_postalcode": self.zip,
            "ecom_billto_postal_countrycode": self.countryCD,

            "ecom_billto_telecom_phone_number": self.phone,
            "ecom_billto_online_email" : self.email,
            
            }


        try:
            gotError = 0
            content = self._submit(values,
                                   headers=[("Referer", self.referer)])
        except:
            gotError = 1


        if gotError:
            self.result = payment.ERROR
            self.error = "error connecting to merchant account"

        else:
            resdict = self._parse(content)

            # authorization succeeded if response code was 0
            if resdict["ioc_response_code"]=="0":
                self.result = payment.APPROVED
                self.authcode = resdict["ioc_authorization_code"]
                self.error = None
            elif resdict.has_key("ioc_invalid_fields"):
                self.result = payment.ERROR
                self.error = resdict["ioc_reject_description"]
            else:
                self.result = payment.DENIED
                self.error = resdict["ioc_reject_description"]



    def charge(self, amount, description=""):
        self.authorize(amount)
        if self.result != payment.APPROVED:
            pass # authorize values just pass through...
        else:
            values = {
                "IOC_Handshake_ID": self.handshakeid,
                "IOC_merchant_ID": self.merchant,
                "IOC_User_Name": self.username,
                "IOC_Password": self.password,
                "IOC_order_number": self.orderid,
                "IOC_indicator": "S", # settlement
                "IOC_settlement_amount": self.amount,
                "IOC_authorization_code": self.authcode,
                "IOC_close_flag": "Yes",
                "IOC_invoice_notes": description,
                }

            try:
                content = self._submit(values, page="Settlement.mart",
                                       headers=[("Referer", self.referer)])
            except:
                self.result = payment.ERROR
                self.error = "Unable to charge. (Unknown Error)"
                content = None

            if content:
                resdict = self._parse(content)
                


## @TODO: fix this:
## test in here because sdunit isn't set up for custome python (threads)
if __name__=="__main__":
    from bofacfg import kwargs
    pay = BankOfAmericaPayment(**kwargs)
    pay.authorize("1.00")

    print pay.result
    print "........"
    print pay.error


