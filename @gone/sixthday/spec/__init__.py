import sqlTest
import zdc
import zdc.drivers.DBAPI2Driver
dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlTest.dbc))


