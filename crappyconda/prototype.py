
from strongbox import *
from zebra import html
from handy import trim


def generic_header(title, page):
    return trim(
        '''
        <html>
        <head>
        <title>%(title)s</title>

        <style type="text/css">
        body, table, p {
           font-family: arial, verdana, helvetica;
           font-size: 10pt;
           background: white;
           color: black;
        }

        table {
            border-collapse: collapse;
        }

        th {
            background: silver;
            border: solid black 1px;
            border-left:none;
            border-top: none;
        }

        td {
           border: solid silver 1px;
        }

        </style>
        </head>
        <body>
        <table>
           <tr><td><a href="%(page)s">%(page)s</td></tr>
        </table>
        ''' % locals())



def generic_list(clerk, klass, page):
    res = []
    data = clerk.match(klass)
    slots = klass.__attrs__.keys()
    slots.sort()
    lower = klass.__name__.lower()
    name = klass.__name__
    res.append('</html>')
    res.append(generic_header("%s list" % klass.__name__, page))
    res.append('<p>[<a href="%s?action=edit&what=%s">Add new %s</a>]</p>'
               % (page, lower, name))
    res.append('<h1>%s list</h1>' % name)
    if data:        
        res.append('<table class="workshop" cellspacing="0" cellpadding="2">')
        res.append('<tr>')
        res.append('<td>&nbsp;</td>')
        for a in slots:
            res.append('<th>%s</th>' % a)
        res.append('<td>&nbsp;</td>')
        res.append('</tr>')
        for obj in data:
            res.append('<tr>')
            res.append('<td>[<a href="%s?action=edit&what=%s&ID=%s">edit</a>]</td>'
                       % (page, lower, obj.ID))
            res.append('<th>%s</th>' % getattr(obj, slots[0]))
            for a in slots[1:]:
                res.append('<td>%s</td>' % getattr(obj,a))
            res.append('<td>[<a href="%s?action=delete&what=%s&ID=%s">del</a>]</td>'
                       % (page, lower, obj.ID))
            res.append('</tr>')
        res.append('</table>')
    else:
        res.append("<p>No instances found.</p>")
    return "\n".join(res)




def generic_edit(clerk, obj, page):
    klass = obj.__class__
    res = []
    res.append(generic_header("add new %s" % klass.__name__, page))
    res.append('<form action="%s" method="POST">' % page)
    res.append(html.hidden("what", klass.__name__.lower()))

    
    if obj.ID:
        res.append(html.hidden("ID", obj.ID))
        res.append('<p>edit %s</p>' % klass.__name__)
    else:
        res.append('<p>add new %s</p>' % klass.__name__)

    res.append('<table>')
    for atr in obj.__attrs__:
        if atr == "ID": continue
        atype  = obj.__attrs__[atr].type
        aclass = obj.__attrs__[atr].__class__
        res.append('<tr><td>%s</td>' % atr)
        if aclass.__name__ == "Attribute":
            res.append('    <td>%s</td></tr>'
                       % html.text(atr, getattr(obj,atr)))
        elif aclass.__name__ == "Link":
            res.append('<td><select name="%s">' % atr)
            res.append('<option value="0">&nbsp;</option>')
            
            for op in clerk.match(atype):
                selected = (op.ID == getattr(getattr(obj,atr), "ID", None))
                res.append('<option %s value="%s">%s</option>'
                           % (selected, op.ID, op.name))
            res.append("</select></td>")
        else:
            res.append("<td>...</td>")

    res.append('</table>')
    res.append('<input type="submit" name="action" value="save">')
    res.append('</form>')
    
    res.append('</body>')
    res.append('</html>')
    return "\n".join(res)
    




if __name__=="__main__":
    import sys
    import sqlPair
    cur = sqlPair.dbc.cursor()

    try:
        OUTFILE = sys.argv[1]
    except:
        print "usage: workshop.py OUTFILE"
        sys.exit()

    out = open(OUTFILE,"w")

    classes = {}
    forward = {}
    tables = {}
    links = []

    print >> out, "##"
    print >> out, "## GENERATED FILE. DO NOT CHANGE!"
    print >> out, "##"

    print >> out,  "from strongbox import *"
    print >> out,  "from pytypes import *"
    print >> out,  "from sixthday import AdminApp"
    print >> out,  "import workshop"
    print >> out

    cur.execute(
        """
        SELECT ID, name, _table
        FROM work_class
        """)
    for id, className, table in cur.fetchall():
        classes[id] = className
        tables[className] = table
        print >> out,  "class %s(Strongbox):" % className
        print >> out,  "    ID = attr(long)"

        cur.execute(
            """
            SELECT name, type
            FROM work_attr
            WHERE classID=%s
            """ % id)
        for attrName, type in cur.fetchall():
            print >> out,  "    %s = attr(%s)" % (attrName, type)

        cur.execute(
            """
            SELECT name, otherID, field
            FROM work_link
            WHERE classID=%s
            """ % id)
        for linkName, otherID, field in cur.fetchall():
            klass = classes.get(otherID,"forward")
            links.append((className, linkName, otherID, field))
            if klass == "forward":
                forward[(className, linkName)] = otherID
            print >> out, "    %s = link(%s)" % (linkName, klass)


        cur.execute(
            """
            SELECT j.name, j.otherID, j.field, link.name back
            FROM work_join j
            LEFT JOIN work_link link on j.linkID=link.ID
            WHERE j.classID=%s
            """ % id)
        for linkName, otherID, field, back in cur.fetchall():
            klass = classes.get(otherID,"forward")
            links.append((className, linkName, otherID, field))
            if klass == "forward":
                forward[(className, linkName)] = otherID

            print >> out, "    %s = linkset(%s, %s)" \
                  % (linkName, klass, repr(back))


        print >> out, "    pass" # just in case there's no attrs
        print >> out


    print >> out,  "## resolve forward definitions"
    for className, linkName in forward:
        print >> out,  '%s.__attrs__["%s"].type=%s' % (
            className, linkName, classes[forward[(className, linkName)]])



    ## db map
    print >> out,  "dbmap = {"
    for klass in tables:
        print  >> out, "    %s: '%s',"  % (klass, tables[klass])
    for className, linkName, otherID, field in links:
        print  >> out, "    %s.__attrs__['%s']: (%s,'%s')," \
              % (className, linkName, classes[otherID], field)
    print >> out,  "}"


    print >> out,  'class MyAdminApp(AdminApp):'
    lists = []
    cur.execute("select classID, action, view, next from work_action")
    for classID, action, view, next in cur.fetchall():
        klass = classes[classID]
        print >> out,  '    def %s_%s(self):' % (action, klass.lower())
        if action=="list":
            lists.append(klass)
            if view:
                print  >> out, '        data=[BoxView(_) for _ in self.clerk.match(%s)],' \
                      % klass
                print >> out,  '        self.generic_list(data, "%s")' % (data, view)
            else:
                print >> out,  '        self.write(workshop.generic_list(self.clerk, %s, "%s"))'\
                      % (klass, OUTFILE)
                pass
        elif action=="edit":
            print >> out, '        obj = self._getInstance(%s)' % klass
            print >> out, '        self.write(workshop.generic_edit(self.clerk,  obj,"%s"))'\
                  % (OUTFILE)
        elif action=="save":
            print >> out, '        # populate with data from form:'

            # @TODO: move this to the AdminApp class or something:
            for className, linkName, otherID, field in links:
                if className == klass:
                    print >> out, '        %s = self.input.get("%s")' \
                          % (linkName, linkName)
                    print >> out, '        if %s: del self.input["%s"]' \
                          % (linkName, linkName)
                    

            print >> out, '        obj = self._getInstance(%s)' % klass

            for className, linkName, otherID, field in links:
                if className == klass:
                    print >> out, '        if %s:' % (linkName)
                    print >> out, '            obj.%s = self.clerk.fetch(%s,ID=%s)' \
                          % (linkName, classes[otherID], linkName)

            print >> out, '        self.clerk.store(obj)'
        else:
            print >> out, '        self.generic_%s(%s, "%s")' \
                  % (action, klass, view)
        if next:
            print >> out, '        self.redirect("%s")' % next


    # default action
    print >> out,  '    def act_(self):'
    print >> out,  '        self.write("""'
    if lists:
        print >> out,  '<ul>'
        for klass in lists:
            print >> out,  '<li><a href="%s?action=list&what=%s">%s</a></li>' \
                  % (OUTFILE, klass.lower(), klass)
        print >> out,  '</ul>'
    else:
        print >> out,  'no lists defined'
    print >> out,  '        """)'
    print >> out


    ## main code
    print >> out, 'if __name__=="__main__":'
    print >> out, '    from arlo import Clerk'
    print >> out, '    from sqlPair import dbc'
    print >> out, '    from storage import MySQLStorage'
    print >> out, '    CLERK = Clerk(MySQLStorage(dbc), dbmap)'
    print >> out, '    print >> RES, MyAdminApp(CLERK, REQ).act()'
