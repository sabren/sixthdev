"""
a simple hack to send an old password...
"""
__ver__="$Id$"

import weblib
import tpl_sslhead; tpl_sslhead.show()

if not weblib.request.form.get("email"):
    print weblib.trim(
        """
        <p>
        <b>enter your email address below</b> and we'll send you your password.
        </p>
        
        <form action="password.py" method="post">
        <input type="text" name="email">
        <input type="submit" value="submit">
        </form>
        
        """)
else:
    import zikeshop
    store = zikeshop.Store(siteID=zikeshop.siteID)
    cust = zikeshop.Customer(siteID=zikeshop.siteID,
                             email=weblib.request["email"])
    mail = weblib.trim(
        """
        To: %s
        From: passwordbot@zike.net
        Subject: your password
        
        
        Hello %s,

        Your password for %s
        at: (%s)
        is: %s

        """ \
        % (cust.email,
           cust.address.fname,
           store.name,
           store.homepage,
           cust.password.decrypt())
        )

    zikeshop.sendmail("passwordbot@zike.net",
                      cust.email, "your password",
                      mail)


    
    print "Your password has been sent to your email address. "
    print "When you receive it, "
    print '<a href="checkout.py">click here to login</a>.'
    
    
import tpl_sslfoot; tpl_sslfoot.show()
