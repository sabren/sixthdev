#/usr/home/sabren/bin/python

import zikebase
import weblib
import sqlTest

weblib.auth.check()

cont = zikebase.Content(sqlTest.dbc)
cont.title = weblib.request.get("title")
cont.content = weblib.request.get("content")
cont.save()

