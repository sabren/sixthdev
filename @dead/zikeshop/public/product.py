
import weblib
import zikeshop
from zikeshop import dbc

assert weblib.request.has_key('code'), "Must supply a product code."

prod = zikeshop.Product(code=weblib.request['code'])

print "<h1>%s</h1>" % prod.product
print "<p>%s</p>" % prod.descript

print '<A HREF="cart.py?action=add&code=%s">add to cart</a>' % prod.code

nodes = prod.getNodes()
if not nodes:
    print '<h2>this product is not categorized.</h2>'
else:
    print '<h2>this product is in these categories:</h2>'
    for node in nodes:
        print '<a href="category.py?nodeID=%s">%s</a><br>' % (node.ID, node.path)


print "<hr>"
print '<a href="cart.py">view cart</a>'
print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
