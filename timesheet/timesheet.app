"""
A timesheet app in 'brute force' style.
"""
__ver__="$Id$"
from sixthday import App
from pytypes import Date
from storage import MySQLStorage
import zebra


class TimesheetApp(App):
    def __init__(self, input, dbc):
        super(TimesheetApp, self).__init__(input)
        self.dbc = dbc
        self.storage = MySQLStorage(self.dbc)

    def showForm(self, ID, day, hours, note):
        self.write(zebra.fetch("form", locals()))

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
                "note":self.input["note"]}
        if self.input.get("ID"):
            data["ID"] = int(self.input["ID"])
        self.storage.store("times", **data)
        self.redirect(action="list")

    def act_list(self):
        self.showForm(ID="", day=Date("today"), hours=0, note="")
        self.write(zebra.fetch("timesheet",
                               {"rows":self.storage.match("times")}))

if __name__=="__main__":
    import sqlTimesheet
    print >> RES, TimesheetApp(REQ, sqlTimesheet.dbc).act()
