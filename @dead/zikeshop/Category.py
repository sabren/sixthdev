"""
A Node with Products in it.
"""
__ver__="$Id$"

import sixthday
from zikeshop import Product
from strongbox import *

class Category(sixthday.Node):
    name = attr(str)
    products = linkset(Product)

#    _tuples = ["crumbs", "children", "products"] # @TODO: clean this up!

##     #@TODO: move delete off into admin interface
##     def delete(self):
##         assert len(self.products)==0, \
##                "Cannot delete a category that has products in it."
##         super(Category,self).delete()
