"""
adm_node.py - node administration for zikebase/zikeshop

$Id$
"""

import zikeshop
import zikebase
import weblib
import sys


def showForm(node):

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

    print 'subcategory of:'
    cur = zikeshop.dbc.cursor()
    if not node.ID:
        node.ID = 0
    sql = "SELECT ID, path, ID=%s FROM base_node WHERE ID!=%s ORDER BY path" \
          % (node.parentID, node.ID)
    cur.execute(sql)
    print weblib.selectBox("parentID", cur.fetchall(), blank=0)
    print '(optional) <br>'

    print 'description:<br>'
    print '<textarea cols="30" rows="5" name="descript">%s</textarea><br>' % node.descript
    print '<input name="action" value="save" type="submit">'
    print '</form>'
    


def showLinks():
    cur = zikeshop.dbc.cursor()
    cur.execute("SELECT ID, path FROM base_node order by path")
    print '<b><a href="adm_node.py">add new</a></b><br>'

    for row in cur.fetchall():
        print '<A HREF="adm_node.py?action=delete&ID=%s">[x]</a>' % (row[0],)
        print '<A HREF="adm_node.py?ID=%s">%s</a><br>' % (row[0], row[1])
        
    


if __name__=="__main__":
    
    import header

    if weblib.request.get("ID"):
        ed = zikebase.ObjectEditor(zikebase.Node, ID=weblib.request["ID"])
    else:
        ed = zikebase.ObjectEditor(zikebase.Node)
    ed.act(weblib.request)

    showForm(ed.object)
    print '<hr>'
    showLinks()
    print '<hr>'
    print 'zikeshop alpha (c)2000 zike interactive, inc'


