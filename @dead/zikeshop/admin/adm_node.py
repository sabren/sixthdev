
import zikebase
import weblib

import zikeshop.admin.header

import sys

if weblib.request.get("ID"):
    node = zikebase.Node(ID=weblib.request["ID"])
else:
    node = zikebase.Node()


if weblib.request.get("action")=='save':
    node.name = weblib.request.get("name", '')
    node.parentID = weblib.request.get("parentID", 0)
    node.descript = weblib.request.get("descript", '')
    node.save()
elif weblib.request.get("action")=='delete':
    print "<b>", node.name, "deleted.</b><br>"
    node.delete()
    node = zikebase.Node()


if node.ID:
    print "<b>this is 'edit' mode</b>"
else:
    print "<b>this is 'add' mode</b>"
    node.name = ''
    node.parentID = 0
    node.descript = ''


print '<form action="adm_node.py" method="POST">'
if node.ID:
    print '<input type="hidden" name="ID" value="%s">' % node.ID
print 'name: <input type="text" name="name" value="%s"><br>' % node.name


print 'parent:'
cur = zikeshop.dbc.cursor()
sql = "SELECT ID, path, "
if node.parentID:
    sql = sql + "ID=%s " % node.parentID
else:
    sql = sql + "0=1 "
sql = sql + "from base_node order by path"

cur.execute(sql)
print weblib.selectBox("parentID", cur.fetchall(), blank=0)

print 'description:<br>'
print '<textarea cols="30" rows="5" name="descript">%s</textarea><br>' % node.descript
print '<input name="action" value="save" type="submit">'
print '</form>'


print '<hr>'

cur = zikeshop.dbc.cursor()
cur.execute("SELECT ID, path FROM base_node order by path")

print '<b><a href="adm_node.py">add new</a></b><br>'

for row in cur.fetchall():
    print '<A HREF="adm_node.py?action=delete&ID=%s">[x]</a>' % (row[0],)
    print '<A HREF="adm_node.py?ID=%s">%s</a><br>' % (row[0], row[1])
    
print '<hr>'
print 'zikeshop alpha (c)2000 zike interactive, inc'

