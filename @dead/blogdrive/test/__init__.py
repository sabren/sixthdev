# test scripts for blogdrive

import unittest
import weblib

from sqlTest import dbc

filename = {
    "addPage" : 'add.py'
    }

class BlogDriveTestCase(unittest.TestCase):


    def setUp(self):
        cur = dbc.cursor()
        cur.execute("DELETE FROM base_content")


    def check_addContent(self):

        myRequest = weblib.Request(
            environ={"PATH_INFO":"add.py"},
            querystring={}
            form={
                "title":"testSubject",
                "content":"content",
                }
            )

        addPage = open(filename['addPage'], "r")
        
        weblib.Engine(script=addPage, request=myRequest).run()

        cur = dbc.cursor()
        cur.execute("select ID, title, content from base_content")
        row = cur.fetchone()

        assert row is not None, "addPage didn't add the content!"
        assert row[0] == 1, "ID should be 1, was: " + `row[0]`
        assert row[1] == "testSubject", "subject should be `testSubject`, was: " + `row[1]`
        assert row[2] == "content", "content should be 'content', got: " + `row[2]`
        


from weblib.test import suites
suites[ "blogdrive" ] = unittest.makeSuite(BlogDriveTestCase, "check_")


