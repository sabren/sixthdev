"""
Mock Storage object for in-memory testing.
"""

from storage import Storage, QueryBuilder, where

OPS = {
    "="   : "__eq__",
    ">"   : "__gt__",
    "<"   : "__lt__",
    ">="  : "__ge__",
    "<="  : "__le__",
    "!="  : "__ne__",
    "&" : "__and__",
    "|"  : "__or__",
    }

class MockStorage(Storage):

    def __init__(self):
        self._tables = {}
        self._counter = {}

    def _ensuretable(self, name):
        if not name in self._tables:
            self._tables[name]=[]
            self._counter[name]=0

    def _nextid(self, table):
        self._counter[table] += 1
        return self._counter[table]

    def _dictmatch(self, expression, subject):
        # RICK: uses querybuilder to match instead.
        (prop, val, op) = expression.pattern
        if op in ["|","&"]:
            return getattr(self._dictmatch(expression.left, subject), OPS[expression.operation])(self._dictmatch(expression.right, subject))
        else:
           
            # get the property value to check
            # take the value after the right-most period
            # Omitted due to the new QueryBuilder object
            #if '.' in prop: prop = prop[prop.rindex('.')+1:]
            p = subject[prop]
            # perform the operation from the pattern against the value
            try:
                op = OPS.get(op,op)
                res = getattr(str(p).lower(), op)(str(val).lower())
                # str.index returns 0 if a match is found in the first character, so return 1
                if op == 'index': return 1
                return res
            except ValueError:
                # str.index raises ValueError if no match is found, return 0
                return 0

    def store(self, table, **row):
        self._ensuretable(table)
        return Storage.store(self, table, **row)

    def _update(self, table, **row):
        rec = self.fetch(table, row["ID"])
        rec.update(row)
        return rec

    def _insert(self, table, **row):
        rec = {}
        rec.update(row)
        rec["ID"] = self._nextid(table)
        self._tables[table].append(rec)
        return rec

    def _match(self, table, where=None, orderBy=None):
        self._ensuretable(table)
        if where is None:
            rows = self._tables[table]
        else:
            rows = [row for row
                    in self._tables[table]
                    if self._dictmatch(where, row)]
        if orderBy is not None:
            # parse orderBy
            # break columns into a list of tuples, containing field name and sort direction
            setcol = lambda x: x.lower().endswith(' desc') and (x.split()[0], 'desc') or (x.strip(), 'asc')
            cols = [setcol(c) for c in orderBy.split(',')]

            # invert() takes n and returns its opposite (invert(15) == -15)
            # rcmp() is a reverse of the cmp() function
            invert = lambda x: x-2*x
            rcmp = lambda x, y: invert(cmp(x, y))

            def listsort(x, y):
                """
                for each column, do a cmp() or rcmp()
                if the columns are equal, move to the next to sort
                if all columns are equal then return 0
                """
                for c in cols:
                    i = c[1]=='asc' and cmp(x[c[0]], y[c[0]]) or rcmp(x[c[0]], y[c[0]])
                    if i: return i
                return i
            rows.sort(listsort)
        return rows

    def fetch(self, table, ID):
        res = self.match(table, where("ID") == ID)
        if len(res)!=1:
            raise LookupError, "match(%r, ID=%r) returned %i rows." \
                  % (table, ID, len(res))
        return res[0]

    def delete(self, table, w):
        self._ensuretable(table)
        rows = self._tables[table]
        if isinstance(w, QueryBuilder):
            # repeat until no rows are deleted
            l = 1
            while l > 0:
                l = len(self.__deleteMatch(w, rows))
        else:
            for i in range(len(rows)):
                if rows[i]["ID"]==long(w):
                    rows.remove(rows[i])
                    break

    def __deleteMatch(self, where, rows):
        # the loop stops once a row is deleted
        return [rows.remove(row) for row
                in rows
                if self._dictmatch(where, row)]

    
