#!/usr/home/sabren/bin/python

import zikebase
import weblib
import sqlTest

weblib.auth.check()

print "you really shouldn't see this unless you put your password in"

cont = zikebase.Content(sqlTest.dbc)
cont.title = weblib.request.get("title")
cont.content = weblib.request.get("content")
cont.save()

