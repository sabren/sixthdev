"""
list sales in zikeshop
"""
__ver__="$Id$"
import weblib
import zikeshop
import zdc


dmin = weblib.request.get("dmin", "")
dmax = weblib.request.get("dmax", "")
includeFilled = weblib.request.get("includeFilled") == "1"
name = weblib.request.get("name", "")
isSearch = weblib.request.get("is_search")


select =\
    """
    SELECT s.ID, s.tsSold, bc.fname, bc.lname, s.subtotal, s.total 
    FROM shop_sale s
        LEFT JOIN base_contact bc on s.bill_addressID=bc.ID
        LEFT JOIN base_contact sc on s.ship_addressID=sc.ID
    """ 

## build the where clause
where = "1=1 "
if (dmin): where = where + " AND s.tsSold >= '%s' AND " % dmin
if (dmax): where = where + " AND s.tsSold <= '%s 23:59:59' AND " % dmax
if (name): where = where + " AND (bc.fname LIKE '%%%s%%' OR " \
                 " bc.lname LIKE '%%%s%%' OR " \
                 " sc.fname LIKE '%%%s%%' OR " \
                 " sc.lname LIKE '%%%s%%') " \
                 % (name, name, name, name)
if not includeFilled:
    where = where + "AND (s.status!='complete') "

# @TODO: clean this whole query thing up!
# kids, don't do this at home.
ick = []
sales = zdc.find(zikeshop.Sale, where, orderBy="s.tsSold", _select=select)
for sale in sales:
    ick.append({
        "ID": sale.ID,
        "tsSold": sale.tsSold,
        "fname" : sale.billAddress.fname,
        "lname" : sale.billAddress.lname,
        "subtotal" : sale.subtotal,
        "total" : sale.total,
        })

model = {}
model["sales"] = ick
model["dmin"] = dmin
model["dmax"] = dmax
model["name"] = name
