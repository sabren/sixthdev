# 
# mdl_categories = all categories in the current store
#

import zdc, zikeshop

cur = zikeshop.dbc.cursor()
sql ="SELECT ID, path FROM base_node order by path"
cur.execute(sql)

model = {
    "categories" : zdc.toListDict(cur)
    }

