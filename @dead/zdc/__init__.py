"""
zdc: zike data classes (wrapper for python db-api 2.0)
"""
__ver__="$Id$"

from Field import Field
from Table import Table
from Record import Record
from RecordObject import RecordObject
from ObjectView import ObjectView
from LinkSet import LinkSet
from Junction import Junction
from Connection import Connection

    
# @TODO: we need to know which module 'dbc' comes from, because
# we need to get certain constants (eg, for field types)
# that are in the module, but not connected to the
# connection object... This is a shortcoming of the DB-API.. :/
from MySQLdb import NUMBER


###############

def sqlEscape(s):
    #@TODO: get the real version of this out of Record
    #@TODO: get rid of this? (probably no longer needed)
    import string
    return string.replace(s, "'", "\\'")


def sqlSet(*data):
    """returns a string with a SQL set containing whatever you pass in"""
    #@TODO: get rid of this? (probably no longer needed)
    set = []
    for item in data:
        
        # we don't accept dicts.
        if type(item) == type({}):
            raise TypeError, "sqlSet we can't handle dicts"

        # but we DO accept lists and tuples
        elif type(item) in (type(()), type([])):
            set = set+list(item)

        # ... as well as scalars.
        else:
            set.append(item)

    # stringify the set
    res = str(tuple(set))

    # one-item tuples have a "," at the end, but
    # sql doesn't like that.
    if res[-2]==",":
        res = res[:-2]+")"
        
    return res


def toListDict(cur):
    """converts cursor.fetchall() results into a list of IdxDicts"""
    #@TODO: (is this still needed?)
    from pytypes import IdxDict
    res = []
    for row in cur.fetchall():
        dict = IdxDict()
        for i in range(len(cur.description)):
            dict[cur.description[i][0]] = row[i]
        res.append(dict)
    return res

def viewToXML(view, itemLabel="item", listLabel="list"):
    """
    viewToXML(view, itemLabel='item', listLabel='list')
    """
    res = "<%s>" % listLabel
    for item in view:
        attrs = ""
        for key in item.keys():
            attrs = attrs + ' %s="%s"' % (key, item[key])
        res = res + "<%s%s/>" % (itemLabel, attrs)
        
    res = res + "</%s>" % listLabel
    return res

