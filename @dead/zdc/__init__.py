# zike data classes

from IdxDict import IdxDict
from Field import Field
from Table import Table
from Record import Record
from Object import Object
from RecordObject import RecordObject



def sqlSet(*data):
    """returns a string with a SQL set containing whatever you pass in"""
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


