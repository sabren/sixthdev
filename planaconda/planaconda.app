
import os
import sys
sys.path.append("/home/sabren/lib")
sys.path.append("/web/script/sabren/sabren.net/work")

from planaconda import config
from planaconda import PlanApp
import arlo
import shelve
import storage
import weblib
import zebra

shelf = shelve.open("data/planaconda.shf")
if not shelf.get("store"):
    shelf["store"] = storage.MockStorage()

store = shelf["store"]
clerk = arlo.Clerk(store, config.DBMAP)

app = PlanApp(clerk, REQ)
page = REQ.get("action", "viewListProject")
meth = getattr(app, page, None)

try:
    model = meth() # possible Redirect here
finally:
    shelf["store"] = store
    shelf.close()

if meth:
    template = "html/%s.zb" % page
    if os.path.exists(template):
        print >> RES, zebra.fetch(template, model)
    else:
        print >> RES, "no template for %s" % page
else:
    print >> RES, "unknown action: %s" % page
