
DBFILE = "blog.rdb"

import sqlite, storage
dbc = sqlite.connect(DBFILE)
sto = storage.PySQLiteStorage(dbc)
