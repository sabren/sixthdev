__ver__="$Id$"

import unittest
from zikeshop import Contact

class ContactTest(unittest.TestCase):

    def test_email(self):
        ctact = Contact()
        try:
            ctact.email="@sadf@@"
            gotError =0
        except TypeError:
            gotError =1 
        assert gotError, "didn't get error assigning invalid email."

        ctact.email = "michal@zike.net"
        self.assertEquals(ctact.email, "michal@zike.net")

if __name__=="__main__":
    unittest.main()
