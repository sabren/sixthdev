"""
checkout process for the cart (records the sale)

$Id$
"""
import zikeshop
import weblib

weblib.auth.check()

useTax = 0
isSubmitted = 1

cart = zikeshop.Cart()
# I don't think these are actually part of cart..
# I think I added them in to make the PHP3 port easier.
# @TODO: they probably ought to be part of Cashier or something.

if weblib.request.get("shipmeth"):
    cart.shipmeth = weblib.request.get("shipmeth")

if (useTax != ""):
    cart.useTax = useTax

for item in weblib.sess.keys():
    print item, ":", weblib.sess[item], "<br>"
print "<hr>"

cash = zikeshop.Cashier(cart, weblib.auth.user)
cash.act()


print "<hr>"
for item in weblib.sess.keys():
    print item, ":", weblib.sess[item], "<br>"
print "<hr>"


##-- validate the data ---
missingfields = ""
##    if ($b_fname=="") { $missingfields .= "Billing First Name<BR>"; }
##    if ($b_lname=="") { $missingfields .= "Billing Last Name<BR>"; }
##    if ($b_phone=="") { $missingfields .= "Billing Phone<BR>"; }
##    if ($b_email=="") { $missingfields .= "Billing Email<BR>"; }
##    if ($b_addr1=="") { $missingfields .= "Billing Address<BR>"; }
##    if ($b_city=="")  { $missingfields .= "Billing City<BR>"; }
##    if ($b_state=="") { $missingfields .= "Billing State<BR>"; }
##    if ($b_zip=="")   { $missingfields .= "Billing Zip<BR>"; }
##
##    if ($payType=="credit") {
##       if ($cardType=="") { $missingfields .= "Card Type<BR>"; }
##       if ($cardName=="") { $missingfields .= "Name on Card<BR>"; }
##       if ($cardNum=="")  { $missingfields .= "Card Number<BR>"; }
##       if ($cardExp=="")  { $missingfields .= "Card Expiration Date<BR>"; }
##    }



#-- show the appropriate screen --
if ((isSubmitted==1) and (not cart.isEmpty())):
	
    # validate data
    if (missingfields):
        pass
        
##         $errorMessage = '<font color="red" size="5">'
##             . 'Please Fill out All Required Fields</font>'
##             . "<br>\n"
##             . $missingfields;
##        
##         include "$incpath/orderform.hto";
        
    else:
    
        ### write the data to the database

        r = zikeshop.Sale()
    
        # @TODO: #r->base_fields["orderdate"] = "initialtimestamp";
        #r->parseform();
        #r->values["affiliateID"] = $cart->ref_affiliateID;
        #r->values["shipmeth"] = $cart->shipmeth;
        #r->values["useTax"] = $cart->useTax;
        #r->insert();
        ##
        ##         $cart->save_order($r->ID);

        import receipt
    
else:
    import orderform
