#!/usr/bin/python
"""
This tool generates a zebra form template from a strongbox.
"""
_USAGE_ ="formgen.py module classname"
__ver__="$Id$"

import sys
from handy import trim

if __name__=="__main__":
    try:
        theModule, theClass = sys.argv[1:3]
    except:
        print "usage:", _USAGE_
        sys.exit()

    exec "from %s import %s" % (theModule, theClass)
    instance = locals()[theClass]()

    print trim(
          '''
          *# remember to update ####### tags in this generated file!
          * exec:
              from zebra import html

          <form action="########index.py" method="POST">
          {:html.hidden("what", "#######%(theClass)s"):}
          * if ID:
              edit %(theClass)s
              {:html.hidden("ID", ID):}
          * el:
              add new %(theClass)s

          <table>
          ''' % locals())

    for field in instance.__attrs__:
        if field != 'ID':
            print trim(
                '''
                <tr><td>%(field)s</td>
                    <td>{:html.text("%(field)s", %(field)s):}</td></tr>
                ''' % locals())

    print '</table>'
    print '<input type="submit" name="action" value="save">'
    print '</form>'

