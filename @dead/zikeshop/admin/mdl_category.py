# 
# mdl_categories = all categories in the current store
#

import zdc, zikeshop, weblib

cur = zikeshop.dbc.cursor()
sql ="SELECT ID, path FROM base_node where siteID=%s order by path" \
      % weblib.auth.user.siteID
cur.execute(sql)

model = {
    "categories" : zdc.toListDict(cur)
    }

