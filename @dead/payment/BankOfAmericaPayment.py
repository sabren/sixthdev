import payment

class BankOfAmericaPayment(payment.AbstractPayment):
    """
    a Payment class for talking to Bank of America's Settle Up service.
    """
    __ver__="$Revision$"
    __super = payment.AbstractPayment

    def __init__(self, **kwargs):
        
        self.customerid = ""
        self.orderid = "" # unique order id, to prevent duplicates
        self.address2 = ""
        self.email = ""
        self.referer = "" # only certain sites can post..
        
        self.__super.__init__(self, **kwargs)
        self._secureServer = "cart.bamart.com"
        self._securePage = "payment.mart"
        

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

            "ecom_billto_postal_street_line1": self.address,
            "ecom_billto_postal_street_line2": self.address2,
            "ecom_billto_postal_city": self.city,
            "ecom_billto_postal_stateprov": self.state,
            "ecom_billto_postal_postalcode": self.zip,
            "ecom_billto_postal_countrycode": self.countryCD,

            "ecom_billto_telecom_phone_number": self.phone,
            "ecom_billto_online_email" : self.email,
            
            }

        content = self._submit(values,
                               [("Referer", self.referer)])

        resdict = {}
        # result is key=value pairs..
        # there's a <BR> after each line, including the last, so...
        for item in content.split("<BR>")[:-1]:
            key, val = item.split("=", 1)
            resdict[key.lower()]=val


        # authorization succeeded if response code was 0
        if resdict["ioc_response_code"]=="0":
            self.result = payment.APPROVED
            self.error = None
        elif resdict.has_key("ioc_invalid_fields"):
            self.result = payment.ERROR
            self.error = resdict["ioc_reject_description"]
        else:
            self.result = payment.DENIED
            self.error = resdict["ioc_reject_description"]



## @TODO: fix this:
## test in here because sdunit isn't set up for custome python (threads)
if __name__=="__main__":
    from bofacfg import kwargs
    pay = BankOfAmericaPayment(**kwargs)
    pay.authorize("1.00")

    print pay.result
    print "........"
    print pay.error


