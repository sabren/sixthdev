
import zdc, zdc.drivers.DBAPI2Driver, sqlTest
dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlTest.dbc))

#import zike
#1
#import sqlTest
#dbc = zdc.Connection(zike.MultiBaseDriver(sqlTest.dbc, DB=1))

# since this is my development environment, test==production
# *****************************************
# *****************************************
#
# YOU REALLY REALLY NEED TO CHANGE THIS!!!
# OR ELSE RUNNING THE  TESTS WILL  DESTROY
# ALL YOUR DATA!!!!
#
# *****************************************
# *****************************************
#import sqlExpress
sqlExpress = sqlTest
test_dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlExpress.dbc))

