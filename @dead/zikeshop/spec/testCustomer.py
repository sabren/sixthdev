
import unittest
import zikeshop

class CustomerTestCase(unittest.TestCase):

    def check_uid(self):
        cust = zikeshop.Customer()
        assert len(cust.uid) == 32, \
               "Customer doesn't get a unique ID"

        cust.username = "fred"
        cust.password = "rufus"
        cust.email = "fred@tempy.com"
        cust.save()

        same=zikeshop.Customer(ID=cust.ID)
        assert same.uid == cust.uid, \
               "customer.uid didn't save properly: %s != %s" \
               % (same.uid, cust.uid)

