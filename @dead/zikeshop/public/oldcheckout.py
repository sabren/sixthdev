
import weblib
import zikeshop
from zikeshop import dbc



def showCheckoutPage():
    print weblib.trim(
        """
        <h1>check out</h1>
        <form action="checkout.py" method="POST">
        your  name: <input type="text" name="cus_name"><br>
        your other info: <i>(coming soon)</i><br>
        <br>
        <input type="submit" name="action" value="submit">
        </form>
        """)
    

def showReceipt():
    print '<h1>receipt</h1>'
    print '<b>you just bought the following products:</b><br>'
    print '<table border="1">'
    print '<tr><th>code</th><th>product</th><th>amount</th></tr>'
    for item in cart.contents:
        prod = zikeshop.Product(code=item[0])
        print "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" \
              % (prod.code, prod.product, item[2])
    print '</table>'
    

    













if __name__=="__main__":
    cart = zikeshop.Cart()
    cart.start()
    
    if weblib.request.get("action")=="submit":
        showReceipt()
    else:
        showCheckoutPage()
        
    cart.stop()
        
    print "<hr>"
    print '<a href="category.py">back to top</a>'
    print "<hr>"
    print "zikeshop alpha (c)2000 zike interactive, inc"
        

