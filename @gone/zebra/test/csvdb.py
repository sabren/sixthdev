# csvdb.py
#
# lets you query tables in csv (comma seperated value) format
# assumes first line contains column names..
#
# this doesn't know about commas inside of quotes:
#
#    "field, with, commas", another field
#
# .. will be treated as four fields..
#
# spaces are passed right on through to the returned values. so..
# DO THIS:
#    1,2,3,4,5
# NOT THIS:  
#    1, 2, 3, 4, 5
#
# implements a subset of the Python DB API
# basically, just enough to test reporting in zebra
#

class Cursor:

    def __init__(self, dirname):
        self.dirname = dirname
        self.description = None
        self.result = []
        self.cursor = 0
        self.rowcount = 0

    def execute(self, query):
        """execute(filename) - treat filename as a recordset"""
        
    def fetchone(self):
        try:
            res = self.result[self.cursor]
            self.cursor = self.cursor + 1
        except IndexError:
            res = None
        return res

    def execute(self, filename):
        import string
        lines = string.split(open(self.dirname + "/" + filename).read(), "\n")
        self.result = []
        self.description = []
        self.cursor = 0
        for field in string.split(lines[0], ","):
            #
            # the DB API 2.0 spec requires a sequence of
            # seven-item sequences. the items are:
            #
            # (name, type_code, display_size, internal_size,
            #  precision, scale, null_ok)
            #
            # um. screw that.. I just want to test zebra. :)
            #
            self.description.append([field])
        # now get the individual lines:
        for line in lines[1:]:
            # ignore blank lines (eg, at the end)
            if line != '': 
                self.result.append(string.split(line, ","))
        # and decide how many lines there are
        self.rowcount = len(self.result)
   

class Connection:

    def __init__(self, dirname):
        self.dirname = dirname

    def cursor(self):
        return Cursor(self.dirname)

    def close(self):
        pass

def connect(dirname):
    return Connection(dirname)


if __name__ =="__main__":
    db = connect('.')
    c=db.cursor()
    c.execute('testcsv.csv')
    row = c.fetchone()
    if (row != None):
        fieldpos = {}
        for fieldnum in range(len(c.description)):
            # the name of the field is the 0th item
            # in a row.description field:
            fieldpos[c.description[fieldnum][0]] = fieldnum
        while (row != None):
            print row[fieldpos["guy"]], "loves", row[fieldpos["girl"]]
            row = c.fetchone()
    else:
        print "no rows in the file."
            
