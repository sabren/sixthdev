
class Model: pass
model = Model()


def show():
    
    print "<h1>Billing Address</h1>"

    if model.addressbook:

        print '<form action="checkout.py" method="POST">'
        print '<h3>Select an address to bill to...</h3>'
        print '<select name="billAddressID">'
        for item in model.addressbook:
            print '<option value="%(ID)s">%(fname)s %(lname)s /' % item
            print ' %(address1)s /  %(city)s' % item
        print '</select>'
        print '<input type="hidden" name="action" value="update">'
        print '<input type="submit" value="submit">'
        print '</form>'
        
        print '<h3>... or enter a new address below:</h3>'
    else:
        print '<h3>enter a <b>billing</b> address below:</h3>'

    print '<form action="newaddress.py" method="post">'
    print '<b>name:</b> '
    print 'first: <input type="text" name="fname" value=""> '
    print 'last: <input type="text" name="lname" value=""><br>'
    print 'address 1: <input type="text" name="address1" value=""><br>'
    print 'address 2: <input type="text" name="address2" value=""><br>'
    print 'address 3: <input type="text" name="address3" value=""><br>'
    print 'city: <input type="text" name="city" value=""><br>'
    print 'state: <input type="text" size="2" name="stateCD" value=""><br>'
    print 'zip/postal code: <input type="text" name="postal" value=""> '
    print 'country: <input type="text" name="countryCD" value=""><br>'
    print 'phone: <input type="text" name="phone" value=""><br>'
    print '<input type="hidden" name="isPrimary" value="0">'
    print '<input type="hidden" name="context" value="checkout">'
    print '<input type="hidden" name="whichone" value="bill">'
    print '<input type="submit" name="action" value="save">'
    print '</form>'
    
