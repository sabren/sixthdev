"""
adm_product.py - product administration for zikeshop

$Id$
"""

import zikeshop
import weblib
import sys


def fetchProduct():
    if weblib.request.get("ID"):
        return zikeshop.Product(ID=weblib.request["ID"])
    else:
        return zikeshop.Product()


def doAction(prod):
    if weblib.request.get("action")=='save':
        action_save(prod)
    elif weblib.request.get("action")=='delete':
        action_delete(prod)


def action_delete(prod):
    print "<b>", prod.code, "deleted.</b><br>"
    prod.delete()
    prod = zikeshop.Product()


def action_save(prod):
    prod.code = weblib.request.get("code", '')
    prod.product = weblib.request.get("product", '')
    prod.descriptLong = weblib.request.get("descriptLong", '')
    prod.save()


def showForm(prod):
    if prod.ID:
        print "<b>this is 'edit' mode</b>"
    else:
        print "<b>this is 'add' mode</b>"
        prod.descriptLong = ''
        prod.product = ''
        prod.code = ''

    print '<form action="adm_product.py" method="POST">'
    if prod.ID:
        print '<input type="hidden" name="ID" value="%s">' % prod.ID
    print 'code: <input type="text" name="code" value="%s"><br>' \
          % prod.code
    print 'product: <input type="text" name="product" value="%s"><br>' \
          % prod.product

    print 'categories:<br>'
    cur = zikeshop.dbc.cursor()
    sql = "SELECT ID, path, 0 from base_node order by path"
    cur.execute(sql)
    print weblib.selectBox("nodeIDs", cur.fetchall(), extra="MULTIPLE")
    print '<br>'

    print 'description:<br>'
    print '<textarea cols="30" rows="5" name="descriptLong">'
    print '%s</textarea><br>' % prod.descriptLong
    print '<input name="action" value="save" type="submit">'
    print '</form>'


def showProductLinks():
    cur = zikeshop.dbc.cursor()
    cur.execute(
        "SELECT ID, code, product FROM shop_product order by code")

    print '<b><a href="adm_product.py">add new</a></b><br>'
    for row in cur.fetchall():
        print '<A HREF="adm_product.py?action=delete&ID=%s">[x]</a>' \
              % (row[0],)
        print '<A HREF="adm_product.py?ID=%s">%s</a>' % (row[0], row[1]),
        print row[2], "<br>"


if __name__=="__main__":
    import zikeshop.admin.header
    prod = fetchProduct()
    doAction(prod)
    showForm(prod)
    print '<hr>'
    showProductLinks()
    print '<hr>'
    print 'zikeshop alpha (c)2000 zike interactive, inc'
