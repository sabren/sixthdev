#!/usr/home/sabren/bin/python

import zikebase
import weblib.script
import sqlTest

import sys
sys.stderr = sys.stdout

weblib.auth.check()

weblib.response.contentType = 'text/plain'

if weblib.request.has_key("ID"):
    cont = zikebase.Content(sqlTest.dbc, key=weblib.request.get("ID", None))
    cont.delete()
    print "<b>deleted.</b>"
else:
    print "<b>nothing to delete</b>"


print "<br>"
print '<a href="list.py">back to list</a><hr>'
