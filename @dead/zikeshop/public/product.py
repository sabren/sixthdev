
import weblib
import zikeshop
from zikeshop import dbc

assert weblib.request.has_key('code'), "Must supply a product code."

prod = zikeshop.Product(code=weblib.request['code'])

print "<h1>Product:%s</h1>" % prod.product
print "<p>%s</p>" % prod.descLong

print '<A HREF="cart.py?action=add&code=%s">add to cart</a>' % prod.code

print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
