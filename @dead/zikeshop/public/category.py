
import weblib, zdc, zikebase, zikeshop
import tpl_category

#@TODO: have a zikeshop.rootnode()

if weblib.request.get("path"):
    cat = zikeshop.Category(path=weblib.request["path"],
                            siteID=zikeshop.siteID)
    assert cat.siteID == zikeshop.siteID, \
           "You don't have rights to this category."
else:
    cat = zikeshop.Category()
    cat.ID = 0

model = {
    "basehref": zikeshop.basehref,
    "name": cat.name,
    "crumbs": cat.q_crumbs(),
    "products": cat.q_products(),
    "children": cat.q_children(),
    }

tpl_category.show(model)
