"""
manage single sales for zikeshop
"""
import string
import weblib
import zikebase
import zikeshop

weblib.auth.check()
saleID = weblib.request.get("saleID")

assert saleID is not None, \
       "Please specify a saleID."

try:
    sale = zikeshop.Sale(ID=saleID)
except:
    assert 0, "invalid saleID"

assert sale.siteID == weblib.auth.user.siteID, \
       "this is not your sale to view."


cur = zikeshop.dbc.cursor()

import header


# @TODO: move comments off into the content table. (??)
# @TODO: explicitly track partially filled orders.

if weblib.request.has_key("action"):
    ed = zikebase.ObjectEditor(zikeshop.Sale, ID=saleID)
    ed.act()
    sale = ed.object

print '<a href="sales.py">back to sales list</a>'
print '<h2>Sale #%(ID)s</h2>' % sale._record

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
            print (line+1), rec["address%i" % (line+1)]

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
            print (line+1), rec["address%i" % (line+1)]

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

    
cur.execute(
    """
    SELECT item, quantity, price, price * quantity AS subtotal
    FROM shop_sale_item
    WHERE saleID = %s
    """ \
    % saleID)



## @TODO: abstract this into a "view" class
print '<table border="1"><tr>'
for item in cur.description:
    print '<th>%s</th>' % item[0]
print '</tr>'
for row in cur.fetchall():
    print '<tr>'
    for item in row:
        print '<td>%s</td>' % item
    print '</tr>'
print '</table>'



print "<b>subtotal:</b> %s<br>" % sale.subtotal
print "<b>salestax:</b> %s<br>" % sale.salestax
print "<b>shipping:</b> %s<br>" % sale.shipping
print "<b>adjustment:</b> %s<br>" % sale.adjustment
print "<b>total:</b> %s<br>" % sale.total


"""
  print "TAX: "; 
  if ($db->f("useTax")) { print "yes"; } else { print "no"; } 
  print "<br>\n";
  print "shipping: " . $db->f("shipmeth") . "<br>\n";
  print "after taxes/shipping: " . $db->f("amount") . "<br>\n";

?>
"""

print """
<hr>
<form action="sale.py?saleID=%i" method="post">
comments:<br>
<textarea cols="40" name="comments" rows="10">%s</textarea><br>
<input type="hidden" name="isFilled" value="0">
change <b>%s</b> status to:
<select name="statusID">
""" % (sale.ID, weblib.deNone(sale.comments), sale.status)

cur.execute("SELECT ID, status FROM shop_status")
for row in cur.fetchall():
    if row[0] == sale.statusID:
        selected = " SELECTED"
    else:
        selected = ""
        
    print '<OPTION VALUE="%i"%s>%s</OPTION>' \
          % (row[0], selected, row[1])
    
print """
</select>
<input type="submit" name="action" value="save">
</form>
"""
