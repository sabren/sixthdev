#!/usr/home/sabren/bin/python

import zikeshop
import weblib.script
import sqlTest

import sys
sys.stderr = sys.stdout # for debugging
#weblib.response.contentType = 'text/plain'

prod = zikeshop.Product(sqlTest.dbc, key=weblib.request.get("ID", None))

if weblib.request.get("action")=='save':
    prod.code = weblib.request.get("code", '')
    prod.product = weblib.request.get("product", '')
    prod.descLong = weblib.request.get("descLong", '')
    prod.save()


if weblib.request.get("ID"):
    print "<b>this is 'edit' mode</b>"
else:
    print "<b>this is 'add' mode</b>"
    prod.descLong = ''
    prod.product = ''
    prod.code = ''

print '<form action="adm_product.py" method="POST">'
print '<input type="hidden" name="ID" value="%s"><br>' % prod.ID
print 'code: <input type="text" name="code" value="%s"><br>' % prod.code
print 'product: <input type="text" name="product" value="%s"><br>' % prod.product
print 'description:<br>'
print '<textarea cols="30" rows="5" name="descLong">%s</textarea><br>' % prod.descLong
print '<input name="action" value="save" type="submit">'
print '</form>'


print '<hr>'

cur = sqlTest.dbc.cursor()
cur.execute("SELECT ID, code, product FROM shop_product order by code")

print '<b><a href="adm_product.py">add new</a></b><br>'

for row in cur.fetchall():
    print '<A HREF="adm_product.py?ID=%s">%s</a>' % (row[0], row[1]),
    print row[2], "<br>"

print '<hr>'
print 'zikeshop alpha (c)2000 zike interactive, inc'




