"""
test cases for AdminApp
"""
__ver__="$Id$"

import os
import unittest
import sixthday.spec
from arlo import Clerk
from sixthday import AdminApp
from sixthday import User
from storage import MockStorage

class AdminAppTest(unittest.TestCase):

    def setUp(self):

        self.storage = MockStorage()
        self.clerk = Clerk(self.storage)
        self.app = AdminApp(self.clerk, {})
        
        # set up some templates to play with:
        tpl = open("spec/frm_test.zb", "w")
        tpl.write("ID is {:ID:}")
        tpl.close()

        tpl = open("spec/lst_test.zb", "w")
        tpl.write(
            "*# zebra to print a dot for each user:\n"
            "* for each:\n" 
            "    {:x:}\n")
        tpl.close()
        
    def check_generic_create(self):
        """
        generic_create should show a page with a view of a new object.
        """
        self.app.generic_create(User, "spec/frm_test")
        output = self.app.out.getvalue()
        assert output.startswith("ID is None"), \
               "generic_create didn't populate form correctly:\n%s" \
               % output


    def check_generic_show(self):
        """
        generic_edit should show a form with a specific object's data
        """
        self.check_generic_save()
        self.app.input = {"ID":1}
        self.app.generic_show(User, "spec/frm_test")
        output = self.app.out.getvalue()
        assert output.startswith("ID is 1"), \
               "generic_show didn't populate the page correctly:\n%s" \
               % output

    def check_generic_list(self):
        #@TODO: this method should probably go away.
        view = [{"x":"a"}, {"x":"b"}]
        self.app.generic_list(view, "spec/lst_test")
        output = self.app.out.getvalue()
        assert output.startswith("a\nb"), \
               "generic_list didn't populate the form correctly:\n%s" \
               % output

    def check_generic_save(self):
        self.app.generic_save(User)
        obj = self.clerk.fetch(User, 1)

    def check_generic_delete(self):
        self.storage.store("User", username="fred")
        self.app.input = {"ID":1}
        self.app.generic_delete(User)
        assert self.storage.match("User") == []

   
    def tearDown(self):
        os.unlink("spec/frm_test.zb")
        os.unlink("spec/lst_test.zb")

