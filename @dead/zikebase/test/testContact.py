"""
test routines for zikebase.Contact
"""
__ver__="$Id$"

import unittest
import zikebase.test
import zikebase

class ContactTestCase(unittest.TestCase):

    def check_email(self):
        ctact = zikebase.Contact()
        try:
            ctact.email="@sadf@@"
            gotError =0
        except ValueError:
            gotError =1 
        assert gotError, "didn't get error assigning invalid email."

        ctact.email = "michal@zike.net"
        assert ctact.email=="michal@zike.net", \
               "setting the email didn't work!"
