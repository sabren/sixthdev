
from sixthday import *
from strongbox import *
from arlo import *
import zebra

class Thing(Strongbox):
    ID = attr(int)
    name = attr(str)
    kids = linkset(forward, "parent")
    parent = link(forward)

Thing.__attrs__["kids"].type = Thing
Thing.__attrs__["parent"].type = Thing


class DemoApp(AdminApp):
    def act_(self):
        t = Thing(name="durran")
        t.kids << Thing(name="blah")
        t.kids << Thing(name="blah")
        t.kids << Thing(name="blah")
        t.kids << Thing(name="etc")
        print >> self, zebra.fetch("template.zb", BoxView(t))




if __name__=="__main__":
    CLERK = MockClerk()
    print >> RES, DemoApp(CLERK, REQ).act()


