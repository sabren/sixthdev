
import zdc, zdc.drivers.DBAPI2Driver, sqlExpress
dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlExpress.dbc))

#import zike
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
test_dbc = dbc
