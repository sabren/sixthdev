#!/usr/home/sabren/bin/python


import weblib #.script
from zikeshop import dbc

# for now just show a list of products

cur = dbc.cursor()
cur.execute("select code, product from shop_product order by code")

print "<h1>Products</h1>"


for row in cur.fetchall():
    print '<A href="product.py?code=%s">%s</A><br>' % (row[0], row[1])

print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
