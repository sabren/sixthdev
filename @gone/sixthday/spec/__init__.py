import sqlTest
import zdc
import zdc.drivers.DBAPI2Driver
from strongbox import Clerk

dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlTest.dbc))
clerk = Clerk(dbc)

