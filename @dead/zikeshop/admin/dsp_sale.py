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

print '<a href="index.py?action=list&what=sale">back to sales list</a><br><br>'
print '<DIV CLASS="adminheading">Sale #%s</DIV>' % int(sale.ID)


if sale.billAddress:
    rec = sale.billAddress._record

    if sale.billAddress.email:
        print """
        <p><b>customer: <A href="mailto:%(email)s">%(email)s</a></b></p>
        """ % sale.billAddress._record
        
    #@TODO: store organization? or should that be address line 1?
    #@TODO: logic for hiding state if not in US

    ## BILLING INFO
    rec = sale.billAddress._record
    import weblib
    print weblib.trim(
        """
        <pre class="contentcopy"><b>Billing Info</b>
        %(fname)s %(lname)s""" % rec)
        
        
    if sale.billAddress.company:
        print sale.billAddress.company      

    ## hide empty address lines
    for line in range(3):
        if string.strip(weblib.deNone(rec.get("address%i" % (line+1),""))) != "":
            print rec["address%i" % (line+1)]

    print weblib.trim(
        """
        %(city)s, %(stateCD)s, %(postal)s
        %(countryCD)s
        phone: %(phone)s</pre>
        """ % rec)

    if sale.shipAddress.isCompany:
       print 'Commercial Address'
    else:
       print 'Residential Address'


    ## SHIPPING INFO (cut and pasted from above)
    rec = sale.shipAddress._record
    print weblib.trim(
        """
        <pre class="contentcopy"><b>Shipping Info</b>
        %(fname)s %(lname)s""" % rec)

    ## hide empty address lines
    for line in range(3):
        if string.strip(weblib.deNone(rec.get("address%i" % (line+1),""))) != "":
            print rec["address%i" % (line+1)]

    if sale.shipAddress.company:
        print sale.shipAddress.company      

    print weblib.trim(
        """
        %(city)s, %(stateCD)s, %(postal)s
        %(countryCD)s
        phone: %(phone)s</pre>
        """ % rec)

    if sale.shipAddress.isCompany:
       print 'Commercial Address'
    else:
       print 'Residential Address'
   
    #@TODO: handle non-credit card sales

    print weblib.trim(
        """
        <pre class="contentcopy"><b>Credit Card:</b>
        name on card: %(name)s
        number: %(number)s
        expiration: %(expMonth)s/%(expYear)s</pre>
        """ % sale.card._record)

else:
    print '<h3>manual sale: %s EST</h3>' % sale.tsSold


## @TODO: abstract this into a "view" class
print '<table class="admintablebg" border="0"  CELLSPACING="1" CELLPADDING="2"><tr>'
print '<td class="admintablefield">code</td>'
print '<td class="admintablefield">item</td>'
print '<td class="admintablefield">quantity</td>'
print '<td class="admintablefield">price</td>'
print '<td class="admintablefield">subtotal</td>'
print '</tr>'


for det in sale.details:
    print '<tr>'
    print '<td class="admintablecellodd">%s</td>' % det.product.code
    print '<td class="admintablecellodd">%s</td>' % det.product.label
    print '<td class="admintablecellodd">%s</td>' % det.quantity
    print '<td class="admintablecellodd">%s</td>' % det.product.price # @TODO: olap for prices?
    print '<td class="admintablecellodd">%s</td>' % det.subtotal
    print '</tr>'
print '</table>'



print "<b>subtotal:</b> %s<br>" % sale.subtotal
print "<b>salestax:</b> %s<br>" % sale.salestax
print "<b>shipping:</b> %s<br>" % sale.shipping
print "<b>adjustment:</b> %s<br>" % sale.adjustment
print "<b>total:</b> %s<br>" % sale.total


print '''
<hr>
<form action="index.py" method="POST">
<input type="hidden" name="action" value="save"/>
<input type="hidden" name="what" value="sale"/>
<input type="hidden" name="ID" value="%s"/>
comments:<br/>
<textarea cols="40" name="comments" rows="10">%s</textarea><br/>
<input type="hidden" name="isFilled" value="0"/>
change <b>%s</b> status to:
<select name="status">
''' % (sale.ID, weblib.deNone(sale.comments), sale.status)

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
