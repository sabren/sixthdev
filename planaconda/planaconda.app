
import os
import sys
sys.path.insert(0, "/web/script/sabren/sabren.net/work")
sys.path.insert(0, "/home/sabren/lib")

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


if meth is None:
    print >> RES, "unknown action: %s" % page
else:
    try:
        model = meth() # possible Redirect here
    finally:
        shelf["store"] = store
        shelf.close()

    template = "html/%s.zb" % page
    if os.path.exists(template):
        print >> RES, zebra.fetch(template, model)
    else:
        print >> RES, "no template for %s" % page
