# 
# mdl_categories = all categories in the current store
#

import zdc, zikeshop
cats =  zdc.find(zikeshop.Category, orderBy="path")
for i in range(len(cats)):
    cats[i] = zdc.ObjectView(cats[i])
model = {"categories" : cats}

