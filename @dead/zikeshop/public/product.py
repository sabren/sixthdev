
import weblib
import zikeshop
from zikeshop import dbc


prod = zikeshop.Product(dbc, key={'code': weblib.request.get('code')})

print "<h1>Product:%s</h1>" % prod.product
print "<p>%s</p>" % prod.descLong

print '<A HREF="cart.py?action=add&code=%s">add to cart</a>' % prod.code

print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
