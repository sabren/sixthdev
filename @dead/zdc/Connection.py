"""
zdc.Connection class - connects to a storage area.
"""
__ver__="$Id$"

class Connection:
    from MySQLdb import * # for NUMBER, etc..

    def __init__(self, source=None, **params):
        if source:
            apply(self.open, (source,), params)

    def cursor(self):
        return self.source.cursor()

    def open(self, source, **params):
        self.source = source
