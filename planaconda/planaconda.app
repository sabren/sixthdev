
import os
import sys
sys.path.append("/home/sabren/lib")
sys.path.append("/web/script/sabren/sabren.net/work")

import zebra

from planaconda import config
from planaconda import PlanApp
import arlo
import shelve
import storage

shelf = shelve.open("data/planaconda.shf")
if not shelf.get("store"):
    shelf["store"] = storage.MockStorage()
ENG.do_on_exit(shelf.close)

store = shelf["store"]
clerk = arlo.Clerk(store, config.DBMAP)

app = PlanApp(clerk, REQ)
page = REQ.get("action", "viewListProject")
meth = getattr(app, page, None)
if meth:
    template = "html/%s.zb" % page
    if os.path.exists(template):
        print >> RES, zebra.fetch(template, meth())
    else:
        print >> RES, "no template for %s" % page
else:
    print >> RES, "unknown action: %s" % page
