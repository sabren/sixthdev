import zikeshop, zdc
store = zikeshop.Store()
nodeID=None # @TODO: FIX THIS (it's reassigned in index)
model={}

def doit():
    global nodeID
    #@TODO: fix this whole nodeID stuff..
    if nodeID:
        # @TODO: better way to handle products in no category
        nodeID = int(nodeID)
        if nodeID:
            cat = zikeshop.Category(ID=nodeID)
        else:
            cat = zikeshop.Category()
            cat.ID = 0

        products = []
        for prod in cat.products:
            products.append(zdc.ObjectView(prod))
        model["products"] = products
        model["path"] = cat.path
    else:
        products = []
        #@TODO: optimize this, allow for objectsets, etc..
        for prod in store.products:
            products.append(zdc.ObjectView(prod))
        model["products"] = products
