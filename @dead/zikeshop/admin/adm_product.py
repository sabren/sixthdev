"""
adm_product.py - product administration for zikeshop

$Id$
"""

import zikebase
import zikeshop
import weblib
import zdc
import sys
        

def showForm(prod):
    if prod.ID:
        print "<b>this is 'edit' mode</b>"
    else:
        print "<b>this is 'add' mode</b>"
        prod.descriptLong = ''
        prod.name = ''
        prod.code = ''

    print '<form action="adm_product.py" method="POST">'
    if prod.ID:
        print '<input type="hidden" name="ID" value="%s">' % prod.ID
    print 'code: <input type="text" name="code" value="%s"><br>' \
          % prod.code
    print 'name: <input type="text" name="name" value="%s"><br>' \
          % prod.name

    print 'categories:<br>'
    cur = zikeshop.dbc.cursor()
    if prod.nodeIDs:
        sql = "SELECT ID, path, ID in %s FROM base_node order by path" \
              % zdc.sqlSet(prod.nodeIDs)
    else:
        sql = "SELECT ID, path, 0 from base_node order by path"
    cur.execute(sql)
    print weblib.selectBox("nodeIDs", cur.fetchall(), extra="MULTIPLE")
    print '<br>'

    print 'description:<br>'
    print '<textarea cols="30" rows="5" name="descriptLong">'
    print '%s</textarea><br>' % prod.descriptLong
    print '<input name="action" value="save" type="submit">'
    print '</form>'


def showLinks():
    cur = zikeshop.dbc.cursor()
    cur.execute(
        "SELECT ID, code, name FROM shop_product order by code")

    print '<b><a href="adm_product.py">add new</a></b><br>'
    for row in cur.fetchall():
        print '<A HREF="adm_product.py?action=delete&ID=%s">[x]</a>' \
              % (row[0],)
        print '<A HREF="adm_product.py?ID=%s">%s</a>' % (row[0], row[1]),
        print row[2], "<br>"




if __name__=="__main__":
    import header

    if weblib.request.get("ID"):
        ed = zikebase.ObjectEditor(zikeshop.Product, ID=weblib.request["ID"])
    else:
        ed = zikebase.ObjectEditor(zikeshop.Product)

    ed.act(weblib.request)

    showForm(ed.object)
    print '<hr>'
    showLinks()
    print '<hr>'
    print 'zikeshop alpha (c)2000 zike interactive, inc'


