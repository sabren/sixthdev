"""
A timesheet app in 'brute force' style.
"""
__ver__="$Id$"
from sixthday import App, Auth
from pytypes import Date
from storage import MySQLStorage
import weblib
import zebra
import sys

class TimesheetApp(App):
    def __init__(self, input, dbc, username):
        super(TimesheetApp, self).__init__(input)
        self.dbc = dbc
        self.storage = MySQLStorage(self.dbc)
        self.username = username

    def showForm(self, **model):
        self.write(zebra.fetch("form", model))

    def act_(self):
        self.act_list()

    def act_edit(self):
        if self.input.get("ID"):
            rec = self.storage.fetch("times", self.input["ID"])
            self.showForm(**rec)
        else:
            self.write("no ID given")

    def act_delete(self):
        if self.input.get("ID"):
            self.storage.delete("times", int(self.input["ID"]))
            self.redirect(action="list")
        else:
            self.write("no ID given")

    def act_save(self):
        data = {"day":self.input["day"],
                "hours":self.input["hours"],
                "note":self.input["note"],
                "project":self.input["project"]}
        if self.input.get("ID"):
            data["ID"] = int(self.input["ID"])
	data["user"] = self.username
        self.storage.store("times", **data)
        self.redirect(action="list")

    def act_list(self):
        self.showForm(ID="", day=Date("today"), hours=0, note="", project="")
        self.write(zebra.fetch("timesheet",
                               {"rows":self.storage.match("times", user=self.username)}))

if __name__=="__main__":
    import sqlTimesheet
    from weblib.Sess import Sess
    SESS = Sess(weblib.SessPool.SqlSessPool(sqlTimesheet.dbc), REQ, RES)
    SESS.start()
    try:
        from sixthday import Auth
        AUTH = Auth(SESS, {"mario":"mario",
                           "michal":"michal"})
        AUTH.check()
        print >> RES, TimesheetApp(REQ, sqlTimesheet.dbc, username=AUTH.key).act()
    finally:
        SESS.stop()


