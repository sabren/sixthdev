__ver__="$Id$"

import unittest
import zikeshop.test
from zikeshop import Contact

class ContactTestCase(unittest.TestCase):

    def check_email(self):
        ctact = Contact(zikeshop.test.dbc)
        try:
            ctact.email="@sadf@@"
            gotError =0
        except ValueError:
            gotError =1 
        assert gotError, "didn't get error assigning invalid email."

        ctact.email = "michal@zike.net"
        assert ctact.email=="michal@zike.net", \
               "setting the email didn't work!"
