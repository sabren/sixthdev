__ver__="$Id$"

from rantelope import *
from sesspool import Sess, SqlSessPool

### main code #######################################

if __name__=="__main__":

    from sqlRantelope import clerk, dbc
    ENG.do_on_exit(dbc.close)
   
    sess = Sess(SqlSessPool(dbc), REQ, RES)
    sess.start()
    ENG.do_on_exit(sess.stop)

    auth = AuthorAuth(sess, clerk)
    auth.check()
    
    print >> RES, RantelopeApp(clerk, REQ, auth.user).act()
