#!/usr/home/sabren/bin/python

import zikebase
import weblib.script
from sqlTest import dbc

cur = dbc.cursor()
cur.execute("select ID, title, content from base_content")

print '<b>note:</b> when asked to login, the user="username" and pass="password".<br>'
print 'Also: <i>this is a <b>test environment</b>. Anything you post will get wiped out'
print 'the next time I run the test suite.</i> Don\'t be surprised if things disappear!'
print '- michal [<a href="http://www.linkwatcher.com/metalog/">back to metalog</a>]'
print '<hr>'

print '<table border="0" width="75%">'
print '<tr><td><h1>BlogDrive 0.0!</h1></td>'
print '<td align="right"><a href="add.py">add</a></tr>'
print '<tr><td colspan="2"><hr></td></tr>'

for row in cur.fetchall():
    ID, title, content = row

    print '<tr><td><b>' + title + '</b></td>'
    print '<td align="right">'
    print '<a href="add.py?ID=%s">edit</a>' % ID
    print '<a href="del.py?ID=%s">delete</a>' % ID
    print '</td></tr>'
    print '<tr><td colspan="2">'
    print content
    print '</td></tr>'
    print '<tr><td colspan="2"><hr></td></tr>'


print '</table>'
