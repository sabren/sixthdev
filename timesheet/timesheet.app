"""
A timesheet app in 'brute force' style.
"""
__ver__="$Id$"
from sixthday import App
from pytypes import Date

class TimesheetApp(App):
    def __init__(self, input, dbc):
        super(TimesheetApp, self).__init__(input)
        self.dbc = dbc

    def showForm(self, ID, day, hours, note):
        self.write(
            '''
            <form action="timesheet.app" method="POST">
            <input type="hidden" name="ID" value="%s">
            <table border="0">
              <tr>
                <td>day:</td>
                <td><input type="text" name="day" value="%s"></td>
                <td>hours:</td>
                <td><input type="text" name="hours" value="%s"></td>
              </tr>
              <tr><td colspan="4">note:</td></tr>
              <tr>
                <td colspan="4">
                  <textarea cols="40" name="note">%s</textarea>
                </td>
              </tr>
            </table>
            <input type="submit" name="action" value="save">
            ''' % (ID, day, hours, note))
        if ID:
            self.write('<input type="submit" name="action" value="delete">')
        self.write('</form>')

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
        self.write('<table>')
        for row in cur.fetchall():
            ID, day, hours, note = row
            self.write(
                '''
                <tr>
                  <td><a href="timesheet.app?action=edit&ID=%(ID)s"
                         >%(ID)s</a></td>
                  <td>%(day)s</td>
                  <td>%(hours)s</td>
                  <td>%(note)s</td>
                </tr>
                ''' % locals())
        self.write('</table>')

if __name__=="__main__":
    import sqlTimesheet
    print >> RES, TimesheetApp(REQ, sqlTimesheet.dbc).act()
