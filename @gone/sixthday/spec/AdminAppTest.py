"""
test cases for AdminApp
"""
__ver__="$Id$"

import os
import unittest
import zikebase.test
from sixthday import AdminApp

class AdminAppTest(unittest.TestCase):

    def setUp(self):
        self.app = AdminApp(zikebase.test.dbc, {})

        # set up some templates to play with:
        tpl = open("test/frm_test.zb", "w")
        tpl.write("ID is {:ID:}")
        tpl.close()

        tpl = open("test/lst_test.zb", "w")
        tpl.write(
            "*# zebra to print a dot for each user:\n"
            "* for list:\n" 
            "    {:x:}\n")
        tpl.close()
        
    def check_generic_make(self):
        """
        generic_create should show a page with a view of a new object.
        """
        self.app.generic_make(zikebase.User, "test/frm_test")
        output = self.app.out.getvalue()
        assert output.startswith("ID is None"), \
               "generic_create didn't populate form correctly:\n%s" \
               % actual

    def check_generic_show(self):
        """
        generic_edit should show a form with a specific object's data
        """
        self.app.input["ID"]=1
        self.app.generic_show(zikebase.User, "test/frm_test")
        output = self.app.out.getvalue()
        assert output.startswith("ID is 1"), \
               "generic_edit didn't populate form correctly."

    def check_generic_list(self):
        view = [{"x":"a"}, {"x":"b"}]
        self.app.generic_list(view, "test/lst_test")
        output = self.app.out.getvalue()
        assert output.startswith("ab"), \
               "generic_list didn't populate the form correctly:\n%s" \
               % output

    def check_generic_save(self): #@TODO: write this test!
        pass

    def check_generic_kill(self): #@TODO: write this test!
        pass
   
    def tearDown(self):
        os.unlink("test/frm_test.zb")
        os.unlink("test/lst_test.zb")

