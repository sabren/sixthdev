
class Model: pass
model = Model()

model.name = ""
model.crumbs = []
model.children = []
model.products = []

import zikeshop

def show():
    global model
    if model.name:

        # breadcrumb trail
        print '<h1><A HREF="%s/category">top</A> :' \
              % zikeshop.basehref
        for crumb in model.crumbs:
            print '<A HREF="%s/category/%s">%s</a> : ' \
                  % (zikeshop.basehref, crumb["path"], crumb["name"])
        print "%s</h1>" % model.name

        if model.children:
            print "<h2>Subcategories</h2>"
        for child in model.children:
            print '<a href="%s/category/%s">%s</a>' \
                  % (zikeshop.basehref, child["path"], child["name"])

        # products    
        print "<h2>Products in this category:</h2>"
        for item in model.products:
            print '<A href="%s/product/%s">%s</A><br>' \
                  % (zikeshop.basehref, item["code"], item["name"])

    else:
        print "<h1>top</h1>"
        if model.children:
            print "<h2>Categories</h2>"
        for child in model.children:
            print '<A href="%s/category/%s">%s</A><br>' \
                  % (zikeshop.basehref, child["path"], child["name"])

    print "<hr>"
    print '<a href="%s/cart.py">view cart</a>' % zikeshop.basehref
    print "<hr>"
    print "zikeshop alpha (c)2000 zike interactive, inc"



