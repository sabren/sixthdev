# weblib.Engine

import weblib
import string

class Engine:

    def __init__(self, script=None, pool=None, **kw):

        self.script = script       

        # BUT: any of the singletons can be turned off by passing
        # None, or customized by passing an instance..

        for item in ["request", "response", "sess", "auth", "perm"]:
            
            if kw.has_key(item):
                # use the one they supplied
                setattr(self, item, kw[item])
                
            elif item=="sess":
                self.sess = weblib.Sess(pool, engine=self)

            else:
                # use the default (eg, self.perm=weblib.Perm())
                setattr(self, item, weblib.__dict__[string.capitalize(item)](engine=self))
                        
