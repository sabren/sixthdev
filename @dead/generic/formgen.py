import sys
import weblib
from duckbill.test import dbc #@TODO: get rid of this

theModule, theClass = sys.argv[1:3]
exec "from %s import %s" % (theModule, theClass)
instance = locals()[theClass](dbc)

#@TODO: generic zebra wizard..

print weblib.trim(
      '''
      remember to search for and update ####### tags in this generated file!
      
      * exec:
          from weblib import html
          
      <form action="########index.py" method="POST">
      {:html.hidden("what", "#######%(theClass)s"):}
      * if ID:
          edit %(theClass)s
          {:html.hidden("ID", ID):}
      * el:
          add new %(theClass)s

      <table>
      ''' % locals())
print

for field in instance.getEditableAttrs():
    if field != 'ID':
        print weblib.trim(
            '''
            <tr>
              <td>%(field)s</td>
              <td>{:html.text("%(field)s", %(field)s):}</td>
            </tr>       
            ''' % locals())

print '</table>'
print '<input type="submit" name="action" value="save">'
print '</form>'

