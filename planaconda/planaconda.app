
import sys
sys.path.append("/home/sabren/lib")
sys.path.append("/web/script/sabren/sabren.net/work")

import zebra
from planaconda import PlanApp

app = PlanApp(REQ)
page = REQ.get("action", "viewListProject")
meth = getattr(app, page, None)
if meth:
    template = "listProject"
    if template:
        print >> RES, zebra.fetch(template, meth())
    else:
        print >> RES, "no template for %s" % page
else:
    print >> RES, "unknown action: %s" % page
