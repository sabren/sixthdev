
import weblib
import zikeshop
from zikeshop import dbc

assert weblib.request.has_key('code'), "Must supply a product code."
try:
    prod = zikeshop.Product(code=weblib.request['code'])
    assert prod.siteID == zikeshop.siteID
except:
    assert 0, "Invalid product."



model ={
    "basehref" : zikeshop.basehref,
    
    "code" : prod.code,
    "name" : prod.name,
    "price": prod.price,
    "retail": prod.retail,
    "descript" : prod.descript,
    "pictureID": prod.pictureID,
    "nodes" : prod.q_nodes(),
    "styles" : prod.q_styles(),
    }

import tpl_product
tpl_product.show(model)

