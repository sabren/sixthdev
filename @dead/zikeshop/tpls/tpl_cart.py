
import zikeshop

class Model: pass
model = Model()

def show():
    
    print "<h1>Your Shopping Cart</h1>"

    if model.contents:
        print "<h4>contents of cart:</h4>"
        print '<form action="cart.py" method="POST">'
        print "<ul>"
        line = 0
        for item in model.contents:
            print '<li>'
            print '<a href="%s">%s</a>' \
                  % (item["link"], item["label"])
            print '<input name="quantity_%s" size="3" value="%s">' \
                  % (line, item["quantity"])
            line = line + 1
        print '</ul>'
        print '<input type="submit" name="action" value="update">'
        print '</form>'

        print '<a href="checkout.py">checkout</a>'

    else:
        print "<h4>your cart is empty</h4>"


    print "<hr>"
    print '<a href="%s/category/">top</a>' % zikeshop.basehref
    print "<hr>"
    print "zikeshop alpha (c)2000 zike interactive, inc"

