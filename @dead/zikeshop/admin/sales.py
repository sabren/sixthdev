"""
list sales in zikeshop
"""
__ver__="$Id$"
import header
import weblib
import zikeshop
import zdc

cur = zikeshop.dbc.cursor()

dmin = weblib.request.get("dmin", "")
dmax = weblib.request.get("dmax", "")
## affiliateID = 0
includeFilled = weblib.request.get("includeFilled") == "on"
name = weblib.request.get("name", "")
isSearch = weblib.request.get("action") == "search"

print '''
<h2>Sales</h2>

<form action="sales.py" method="post">
<input type="hidden" name="isSubmission" value="1">
<table border="0" cellspacing="0" cellpadding="2">
  <tr><th align="left" colspan="2" style="color:white; background:#666">
      Search
      </th></tr>
  <!-- date -- >
  <tr><td bgcolor="#eeeeee">dates (y/m/d)</td>
      <td bgcolor="#eeeeee">
      <input type="text" name="dmin" size="10" maxlength="10"
'''

print 'value="%s"> - ' % dmin
print '<input type="text" name="dmax" size="10" maxlength="10"',
print 'value="%s">' % dmax

print '''
  </td></tr>
  <!-- name -- >
  <tr><td bgcolor="#eeeeee">customer name:</td>
      <td bgcolor="#eeeeee">
         <input type="text" name="name" value="%s"></td></tr>
''' % name

############### AFFILIATE STUFF @TODO: (later) #################
## <!-- affiliate -- >
##   <tr><td bgcolor="#eeeeee">affiliate:</td>
##       <td bgcolor="#eeeeee">
##          <select name="affiliateID">
##             <option value=""> </option>
##             <option value="0"
## '''
## if (affiliateID==0):
##     print " CHECKED"
## print '>[none]</option>'
#############PHP##########33333
##             <? $db = new ShopDB;
##                $db->query("select * from affiliate order by affiliate");
##                while ($db->next_record()) {
##                  print '<option value="' . $db->f("ID") . '"';
##                  if ($db->f("ID") == $affiliateID) { print ' SELECTED'; }
##                  print '>' . $db->f("affiliate") . "</option>\n";
##                }
##             ?>
##          </select>
##       </td></tr>
################################################################

print '''
  <!-- search -- >
  <tr><td colspan="2" align="right">
      <table border="0" width="100%" cellpading="2" cellspacing="0">
      <tr><td><input type="checkbox" name="includeFilled"
'''

if (includeFilled):
    print " CHECKED"

print '''> include filled orders </td>
          <td align="right">
              <input type="submit" name="action" value="search"></td></tr>
      </table></td></tr>
</table>
</form>

<form action="sale.py" method="get">
Jump to order #: <input type="text" name="saleID" size="5">
<input type="submit" value="submit">
</form>
'''


if not isSearch:
    print "<h2>unfilled orders</h2>"
else:
    print "<h2>search results</h2>"


sql = "SELECT s.ID, s.tsSold, ba.fname, ba.lname, s.subtotal, s.total " \
      "FROM shop_sale s, shop_address ba, shop_address sa, shop_status st " \
      "WHERE s.bill_addressID=ba.ID AND s.ship_addressID=sa.ID AND " \
      "      s.statusID=st.ID AND "


## build the where clause

if (dmin): sql = sql + "s.tsSold >= '%s' AND " % dmin
if (dmax): sql = sql + "s.tsSold <= '%s' AND " % dmax
if (name): sql = sql + "(ba.fname LIKE '%%%s%%' OR " \
                 " ba.lname LIKE '%%%s%%' OR " \
                 " sa.fname LIKE '%%%s%%' OR " \
                 " sa.lname LIKE '%%%s%%') AND " \
                 % (name, name, name, name)


####### AFFILIATE STUFF ##################
##    if ($affiliateID !="")
##        { $sql = $sql . "affiliateID = $affiliateID and "; }

if not includeFilled:
    sql = sql + "(st.status!='complete') AND "


# the 1=1 is so we don't have to test for and strip out the last "and.."
sql = sql + "1=1 ORDER BY s.tsSold ASC"

cur.execute(sql)
sales = zdc.toListDict(cur)

print '''
<table border="1">
<tr><th>ID</th>
    <th>Date</th>
    <th align="left">customer</th>
    <th>subtotal</th>
    <th>total</th></tr>
'''

for sale in sales:
    print weblib.trim(
        '''
        <tr><td><a href="sale.py?saleID=%(ID)s">%(ID)s</a></td>
            <td>%(tsSold)s</td>
            <td>%(lname)s, %(fname)s</td>
            <td>$%(subtotal)s</td>
            <td>$%(total)s</tr>
        ''' % sale)
        
print '''
</table>
'''


##############################################################
## THE REST OF THIS STUFF IS ONLY FOR AFFILIATE SUPPORT ######
##############################################################
##   #------- commission -------------
##   # clunky, but it works... (love that bloat..)
##
##   if ($affiliateID) {
##     $db = new ShopDB;
##     $db->query($sql);
##     $total = 0;
##     while ($db->next_record()){
## 	   $total += $db->f("subtotal");
##  	}
##
##     if ($total > 0) {
##        $db->query("select affiliate, commission from affiliate " 
##                  ."where ID = $affiliateID");
##        if ($db->next_record()){
## 		   $com = $db->f("commission");
##            $aff = $db->f("affiliate");
##            $tcom = $total * $com / 100;
##            print "<p><b>Total of subtotals:</b> \$$total</p>";
##            print "<p><b>$aff's commission:</b> $com%</p>";
##            print "<p><b>Total commission for $aff</b>: \$$tcom</p>";
##        } else {
##          # this should never happen:
##          print "couldn't find affiliate $affiliateID!";
##        }
##     }
##   }
##
