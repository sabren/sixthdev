"""
customer authentication...

$Id$
"""
import zikeshop
import zikebase
zikebase.load("UserAuth")

class CustomerAuth(zikebase.UserAuth):
    userClass = zikeshop.Customer


    def prompt(self, message, action, hidden):

        print '<h1>%s</h1>' % message

        print "<h3>You may enter existing account info:</h3>"
        print '<form action="%s" method="post">' % action
        print hidden
        print 'email: <input type="text" name="auth_email"><br>'
        print 'password: <input type="password" name="auth_password"><br>'
        print '<input type="submit">'
        print '</form>'
                        

        print "<h3>...or create a new account:</h3>"
        
        print '<form action="newcustomer.py" method="post">'
        print 'email: <input type="text" name="email" value=""><br>'
        print 'create a password:'
        print '<input type="password" name="password" value=""><br>'
        print '<hr>'
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
        print '<input type="hidden" name="isPrimary" value="1">'
        print '<input type="submit" name="action" value="save">'      
        
        print '</form>'

    
