"""
winODBCdb - a wrapper for Marc-Andre Lemburg's
           ODBC.Windows module to bring it up to DB-API 2.0 compliance
"""

import ODBC.Windows

class Connection:
    """All this does is fake out python so that
    dbc.__class__.__module__ actually shows up. It's not required
    for the DB-API, but it helps zdc.Record work better."""
    def __init__(self, realconnection):
        #        self.close = realconnection.close
        #        self.commit = realconnection.commit
        #        self.cursor = realconnection.cursor
        for a in dir(realconnection):
            exec('self.' + a + ' = realconnection.' + a)
            
        
def connect(*params):
    realdbc = apply(ODBC.Windows.connect, params)
    dbc = Connection(realdbc)
    return dbc


######################

apilevel = '2.0'
threadsafety = 0 # ???
paramstyle = 'qmark'

# @TODO: Date(year, month, day)
# @TODO: Time(hour, minute, second)
# @TODO: Timestamp(year, month, day, hour, minute, second)
# @TODO: DateFromTicks(ticks)
# @TODO: TimeFromTicks(ticks)
# @TODO: TimestampFromTicks(ticks)
# @TODO: Binary(string)


######################

class DBAPITypeObject:
    def __init__(self, *values):
        self.values = values
    def __cmp__(self, other):
        if other in self.values:
            return 0
        if other < self.values:
            # huh? it's in the DB-API 2.0 spec..
            return 1
        else:
            return -1


STRING = DBAPITypeObject(
    ODBC.Windows.CHAR,
    ODBC.Windows.LONGVARCHAR,
    ODBC.Windows.VARCHAR)

BINARY = DBAPITypeObject(
    ODBC.Windows.BINARY,
    ODBC.Windows.LONGVARBINARY,
    ODBC.Windows.VARBINARY)

NUMBER = DBAPITypeObject(
    ODBC.Windows.TINYINT,
    ODBC.Windows.BIT,
    ODBC.Windows.BIGINT,
    ODBC.Windows.DOUBLE,
    ODBC.Windows.REAL,
    ODBC.Windows.FLOAT,
    ODBC.Windows.SMALLINT,
    ODBC.Windows.INTEGER,
    ODBC.Windows.DECIMAL,
    ODBC.Windows.NUMERIC)

DATETIME = DBAPITypeObject(
    ODBC.Windows.TIMESTAMP,
    ODBC.Windows.TIME,
    ODBC.Windows.DATE)

ROWID = None # not available via ODBC.Windows?

