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


## build the where clause
where = "1=1 "
if (dmin): where = where + " AND tsSold >= '%s' " % dmin
if (dmax): where = where + " AND tsSold <= '%s 23:59:59' " % dmax

if not includeFilled:
    where = where + " AND (status NOT IN ('cancelled','complete')) "

# @TODO: clean this whole query thing up!
# kids, don't try this at home.
ick=[]
for sale in zikeshop.dbc.select(zikeshop.Sale, where, orderBy="status,tsSold"):
    #@TODO: searching by names is gonna get SLOW! fix it!
    if name:
        names = [sale.billAddress.lname,
                 sale.billAddress.fname,
                 sale.shipAddress.fname,
                 sale.shipAddress.lname,]
        if name not in names:
            continue

    # still here, add the record:
    ick.append({
        "ID": sale.ID,
        "tsSold": sale.tsSold,
        "fname" : sale.billAddress.fname,
        "lname" : sale.billAddress.lname,
        "subtotal" : sale.subtotal,
        "total" : sale.total,
        "status": sale.status,
        })

model = {}
model["sales"] = ick
model["dmin"] = dmin
model["dmax"] = dmax
model["name"] = name
