"""
display a single sale for zikeshop

this should be in zebra, but it isn't because of bad stuff...

"""
import string
import weblib
import zikebase
import zikeshop

saleID = weblib.request.get("ID")

assert saleID is not None, \
       "Please specify a saleID."

sale = zikeshop.Sale(ID=saleID)

# @TODO: move comments off into the content table. (??)
# @TODO: explicitly track partially filled orders.

print '<a href="index.py?action=lst_sale">back to sales list</a>'
print '<h2>Sale #%s</h2>' % int(sale.ID)

if sale.customerID != 0:

    print """
    <p><b>customer: <A href="mailto:%(email)s">%(email)s</a></b></p>
    """ % sale.customer._record

    #@TODO: store organization? or should that be address line 1?
    #@TODO: logic for hiding state if not in US

    ## BILLING INFO
    rec = sale.billAddress._record
    print """
    <pre><b>Billing Info</b>
    %(fname)s %(lname)s""" % rec

    ## hide empty address lines
    for line in range(3):
        if string.strip(rec["address%i" % (line+1)]) != "":
            print rec["address%i" % (line+1)]

    print """%(city)s, %(stateCD)s, %(postal)s
    %(countryCD)s
    phone: %(phone)s
    </pre>
    """ % rec

    ## SHIPPING INFO (cut and pasted from above)
    rec = sale.billAddress._record
    print """
    <pre><b>Shipping Info</b>
    %(fname)s %(lname)s""" % rec

    ## hide empty address lines
    for line in range(3):
        if string.strip(rec["address%i" % (line+1)]) != "":
            print rec["address%i" % (line+1)]

    print """%(city)s, %(stateCD)s, %(postal)s
    %(countryCD)s
    phone: %(phone)s
    </pre>
    """ % rec


    #@TODO: handle non-credit card sales

    print """
    <pre><b>Credit Card:</b>
    name on card: %(name)s
    number: %(number)s
    expiration: %(expMonth)02i/%(expYear)04i</pre>
    """ % sale.card._record

else:
    print '<h3>manual sale: %s EST</h3>' % sale.tsSold


## @TODO: abstract this into a "view" class
print '<table border="1"><tr>'
print '<td>item</td>'
print '<td>quantity</td>'
print '<td>price</td>'
print '<td>subtotal</td>'
print '</tr>'


for det in sale.details:
    print '<tr>'
    print '<td>%s</td>' % det.product.name
    print '<td>%s</td>' % det.quantity
    print '<td>%s</td>' % det.product.price # @TODO: olap for prices?
    print '<td>%s</td>' % det.subtotal
    print '</tr>'
print '</table>'



print "<b>subtotal:</b> %s<br>" % sale.subtotal
print "<b>salestax:</b> %s<br>" % sale.salestax
print "<b>shipping:</b> %s<br>" % sale.shipping
print "<b>adjustment:</b> %s<br>" % sale.adjustment
print "<b>total:</b> %s<br>" % sale.total


print """
<hr>
<form action="index.py?action=save&what=sale" method="post">
<input type="hidden" name="ID" value="%s">
comments:<br>
<textarea cols="40" name="comments" rows="10">%s</textarea><br>
<input type="hidden" name="isFilled" value="0">
change <b>%s</b> status to:
<select name="status">
""" % (sale.ID, weblib.deNone(sale.comments), sale.status)

#@TODO: fix this duplicate status information!!!!!
for row in ["new", "cancelled", "complete", "pending"]:
    if row == sale.status:
        selected = " SELECTED"
    else:
        selected = ""
        
    print '<OPTION %s>%s</OPTION>' \
          % (selected, row)
    
print """
</select>
<input type="submit" value="save">
</form>
"""
