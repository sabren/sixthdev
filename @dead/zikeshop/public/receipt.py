print "(STILL IN PHP3... convert..)"

"""
        ### and show the receipt
        
        print "<html><head><title>Thanks for your Order!</title></head>\n";
        print '<BODY BGCOLOR="#FEFEEF" LINK="#800000" VLINK="#808040" '
            . 'TEXT="#000000">';
        print '<img src="images/welogo4.gif" width="200" height="88">';
        print "<h2>Thanks for your Order!</h2>\n";
    
        print "<table width=600 border=0><tr><td>\n";
    
        print "Order #WE-" . date("Ymd") . "-" . $r->ID . "<br>\n";
    
        $cart->readonly = 1;
        $cart->show_all();
    
        print "<pre>";
		     
        print "Billing Information\n";
        print "-----------------------\n";
        print "$b_lname, $b_fname $b_mname\n";
        if (! $s_name) {
            if ($b_org) { print "$b_org\n"; }
            print "$b_addr1\n";
            if ($b_addr2) { print "$b_addr2\n"; }
            print "$b_city, $b_state $b_zip\n";
            print "$b_country\n";
        }
    
        print "\n";
    
        print "Payment Information\n";
        print "-------------------\n";
        print "Payment Type: <b>$payType</b>\n";
        if ($payType == "credit") {
            print "Card Type: <b>$cardType</b>\n";
            print "Name on Card: <b>$cardName</b>\n";
            print "Expires: <b>$cardExp</b>\n";
        }
    
        print "\n";
    
        if ($s_name) { 
            print "Shipping Information\n";
            print "-----------------------\n";
            print "$s_name\n";
            if ($s_org) { print "$s_org\n"; }
            print "$s_phone\n";
            print "$s_addr1\n";
            if ($s_addr2) { print "$s_addr2\n"; }
            print "$s_city, $s_state $s_zip\n";
            print "$s_country\n";
            print "$s_email\n";
        }
    
        print "\n";
    
        print "</pre>\n";
    
        if ($comments) {
            print "Your Comments:<br>\n";
            print "<p>$comments</p>\n";
        }
    
        print "<p><i>Please save or print this page for your records.</i></p>\n";
        print "<p><a href=\"http://www.wholesome-essentials.com/index.php3\">Back to Home Page.</a></p>\n";
        print "</td></tr></table></body></html>\n";
        
        # empty the cart... this also prevents against refresh
        # causing duplicate orders.
    
        $cart->remove_all();
    
    }
"""
