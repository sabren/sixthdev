"""
test cases for AdminApp
"""
__ver__="$Id$"

import os
import unittest
import sixthday.spec
from sixthday import AdminApp
from sixthday import User

class AdminAppTest(unittest.TestCase):

    def setUp(self):
        self.app = AdminApp(sixthday.spec.dbc, {})

        # set up some templates to play with:
        tpl = open("spec/frm_test.zb", "w")
        tpl.write("ID is {:ID:}")
        tpl.close()

        tpl = open("spec/lst_test.zb", "w")
        tpl.write(
            "*# zebra to print a dot for each user:\n"
            "* for list:\n" 
            "    {:x:}\n")
        tpl.close()
        
    def check_generic_create(self):
        """
        generic_create should show a page with a view of a new object.
        """
        #@TODO: generic_make?
        self.app.generic_create(User, "spec/frm_test")
        output = self.app.out.getvalue()
        assert output.startswith("ID is None"), \
               "generic_create didn't populate form correctly:\n%s" \
               % actual

    def check_generic_show(self):
        """
        generic_edit should show a form with a specific object's data
        """
        self.app.input["ID"]=1
        self.app.generic_show(User, "spec/frm_test")
        output = self.app.out.getvalue()
        assert output.startswith("ID is 1"), \
               "generic_edit didn't populate form correctly."

    def check_generic_list(self):
        view = [{"x":"a"}, {"x":"b"}]
        self.app.generic_list(view, "spec/lst_test")
        output = self.app.out.getvalue()
        assert output.startswith("ab"), \
               "generic_list didn't populate the form correctly:\n%s" \
               % output

    def check_generic_save(self): #@TODO: write this test!
        pass

    def check_generic_kill(self): #@TODO: write this test!
        pass
   
    def tearDown(self):
        os.unlink("spec/frm_test.zb")
        os.unlink("spec/lst_test.zb")

