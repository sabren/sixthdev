
from weblib import Sess, SessPool

pool = SessPool.InMemorySessPool() #"session.db")
sess = Sess(pool, REQ, RES)
sess.start()
#ENG.do_on_exit(sess.stop)

sess.setdefault("count",0)
sess["count"] += 1

print >> RES, "this is visit #%s" % sess["count"]

sess.stop()
