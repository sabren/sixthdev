"""
list sales in zikeshop
"""
__ver__="$Id$"
import weblib
import zikeshop
import zdc
weblib.auth.check()

cur = zikeshop.dbc.cursor()

dmin = weblib.request.get("dmin", "")
dmax = weblib.request.get("dmax", "")
## affiliateID = 0
includeFilled = weblib.request.get("includeFilled") == "on"
name = weblib.request.get("name", "")
isSearch = weblib.request.get("is_search")


sql = """
   SELECT s.ID, s.tsSold, bc.fname, bc.lname, s.subtotal, s.total 
   FROM shop_sale s
        LEFT JOIN base_contact bc on s.bill_addressID=bc.ID
        LEFT JOIN base_contact sc on s.ship_addressID=sc.ID
   WHERE s.siteID=%i AND 
     """ % weblib.auth.user.siteID


## build the where clause

if (dmin): sql = sql + "s.tsSold >= '%s' AND " % dmin
if (dmax): sql = sql + "s.tsSold <= '%s' AND " % dmax
if (name): sql = sql + "(bc.fname LIKE '%%%s%%' OR " \
                 " bc.lname LIKE '%%%s%%' OR " \
                 " sc.fname LIKE '%%%s%%' OR " \
                 " sc.lname LIKE '%%%s%%') AND " \
                 % (name, name, name, name)

if not includeFilled:
    sql = sql + "(s.status!='complete') AND "


# the 1=1 is so we don't have to test for and strip out the last "and.."
sql = sql + "1=1 ORDER BY s.tsSold ASC"

cur.execute(sql)

model = {}
model["sales"] = zdc.toListDict(cur)
model["dmin"] = dmin
model["dmax"] = dmax
model["name"] = name
