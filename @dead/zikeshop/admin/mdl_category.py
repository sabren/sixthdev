# 
# mdl_categories = all categories in the current store
#

import zdc, zikeshop
cats =  zikeshop.dbc.select(zikeshop.Category, orderBy="path")
for i in range(len(cats)):
    cats[i] = zdc.ObjectView(cats[i])
model = {"categories" : cats}

