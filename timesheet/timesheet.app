"""
A timesheet app in 'brute force' style.
"""
__ver__="$Id$"
from sixthday import App
from pytypes import Date
import zebra


def toListOfDicts(cur):
    """
    converts cursor.fetchall() results into a list of IdxDicts
    """
    from pytypes import IdxDict
    res = []
    for row in cur.fetchall():
        dict = IdxDict()
        for i in range(len(cur.description)):
            dict[cur.description[i][0]] = row[i]
        res.append(dict)
    return res


class TimesheetApp(App):
    def __init__(self, input, dbc):
        super(TimesheetApp, self).__init__(input)
        self.dbc = dbc

    def showForm(self, ID, day, hours, note):
        self.write(zebra.fetch("form", locals()))
        
    def query(self, sql):
        cur = self.dbc.cursor()
        cur.execute(sql)
        return cur
       
    def act_(self):
        self.act_list()

    def act_edit(self):
        if self.input.get("ID"):
            cur = self.query("SELECT day, hours, note FROM times WHERE ID='%s'"
                             % self.input["ID"])
            day, hours, note = cur.fetchone()
            self.showForm(self.input["ID"], day, hours, note)
        else:
            self.write("no ID given")

    def act_delete(self):
        if self.input.get("ID"):
            self.query("DELETE FROM times WHERE ID='%s'"
                       % self.input["ID"])
            self.redirect(action="list")
        else:
            self.write("no ID given")

    def act_save(self):
        if self.input.get("ID"):
            self.query(
                """
                UPDATE times
                SET day='%(day)s', hours='%(hours)s', note='%(note)s'
                WHERE ID='%(ID)s'
                """ % self.input)
        else:
            self.query(
                """
                INSERT INTO times (day, hours, note)
                VALUES ('%(day)s', '%(hours)s', '%(note)s')
                """ % self.input)
        self.redirect(action="list")

    def act_list(self):
        cur = self.query("SELECT ID, day, hours, note FROM times")
        self.showForm(ID="", day=Date("today"), hours=0, note="")
        self.write(zebra.fetch("timesheet", {"rows":toListOfDicts(cur)}))

if __name__=="__main__":
    import sqlTimesheet
    print >> RES, TimesheetApp(REQ, sqlTimesheet.dbc).act()
