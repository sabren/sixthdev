import zikeshop, weblib, zdc
store = zikeshop.Store(ID=weblib.auth.user.siteID)

model={}

#@TODO: fix this while nodeID stuff..
if locals().get("nodeID"):
    zikeshop.siteID = weblib.auth.user.siteID #@TODO: fix this!

    # @TODO: better way to handle products in no category
    nodeID = int(nodeID)
    if nodeID:
        cat = zikeshop.Category(ID=nodeID)
    else:
        cat = zikeshop.Category()
        cat.ID = 0

    model["products"] = cat.q_products()
    model["path"] = cat.path
else:
    products = []
    #@TODO: optimize this, allow for objectsets, etc..
    for prod in store.products:
        products.append(zdc.ObjectView(prod))
    model["products"] = products
