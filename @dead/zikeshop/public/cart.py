
import weblib
import zikeshop
from zikeshop import dbc


cart = zikeshop.Cart()
cart.start()
cart.act()
cart.stop()

print "<h1>Cart Page</h1>"

if cart.contents:
    print "<h4>contents of cart:</h4>"
    print '<form action="cart.py" method="POST">'
    print "<ul>"
    for item in range(len(cart.contents)):
        prod = zikeshop.Product(code=cart.contents[item][0])
        print '<li>'
        print '<a href="product.py?code=%s">%s</a>' \
              % (prod.code, prod.product, )
        print '<input name="amt%s" size="3" value="%s">' \
              % (item, cart.contents[item][2])
    print '</ul>'
    print '<input type="submit" name="action" value="update">'
    print '</form>'

    
    print '<a href="checkout.py">checkout</a>'
    
else:
    print "<h4>your cart is empty</h4>"


print "<hr>"
print '<a href="category.py">top</a>'
print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
