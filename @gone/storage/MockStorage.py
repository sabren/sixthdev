"""
Mock Storage object for in-memory testing.
"""

from storage import Storage

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

    def _dictmatch(self, pattern, subject):
        diff = [key for key
                in pattern
                if subject[key] != pattern[key]]
        return not diff

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

    def match(self, table, **where):
        return [row for row
                in self._tables[table]
                if self._dictmatch(where, row)]


    def delete(self, table, ID):
        rows = self._tables[table]
        for i in range(len(rows)):
            if rows[i]["ID"]==ID:
                rows.remove(rows[i])
                break
