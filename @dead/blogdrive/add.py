#!/usr/home/sabren/bin/python

import zikebase
import weblib.script
import sqlTest

import sys
sys.stderr = sys.stdout # for debugging
weblib.response.contentType = 'text/plain'


################################################


print '<a href="list.py">back to list</a>'

if weblib.sess.has_key("counter"):
    weblib.sess["counter"] = weblib.sess["counter"] + 1
else:
    weblib.sess["counter"] = 0
    
print "<b>sess:</b>", weblib.sess
print "<hr>"

################################################


weblib.auth.check()


cont = zikebase.Content(sqlTest.dbc, key=weblib.request.get("ID", None))
if weblib.request.get("submit"):
    cont.title = weblib.request.get("title", '')
    cont.content = weblib.request.get("content", '')
    cont.save()



if weblib.request.get("ID"):
    print "<b>this is 'edit' mode</b>"
else:
    print "<b>this is 'add' mode</b>"
    cont.content = ''
    cont.title = ''

print '<form action="add.py">'
print 'title: <input type="text" name="title" value="%s"><br>' % cont.title
print 'content:<br>'
print '<textarea cols="30" rows="5" name="content">%s</textarea><br>' % cont.content
print '<input name="submit" value="submit" type="submit">'
print '</form>'



