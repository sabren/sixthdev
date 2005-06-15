import weblib
from platonic import Intercept, Redirect

class App(object):

    def __init__(self, tiles={}, default=None):
        self.tiles = tiles
        self.defaultAction = default or "home"
        
    def __call__(self, ctx):
        self.dispatch(ctx)

    def chooseAction(self, req):
        return req.get("action","").replace(" ","_") or self.defaultAction

    def findFeature(self, action):
        """
        returns the uninstantiated class for the feature
        """
        assert action in self.featureSet, "unknown action: %s" % action
        return self.featureSet[action]

    def buildFeature(self, action):
        """
        returns an initialized feature instance
        """
        return self.findFeature(action)()

    def prepareModel(self,req):
        return {}

    def invokeFeature(self, f, req, res):
        return f.handle(req,res)

    # this is the main function that gets called from the
    # app file
    def dispatch(self, req, res=None):
        a = self.chooseAction(req)
        m = self.prepareModel(req)
        f = self.buildFeature(a)
        try:            
            m.update(self.invokeFeature(f, req, res))
        except Redirect, e:
            raise weblib.Redirect(e.where)
        except Intercept, e:
            if e.data:
                m.update(e.data)
            f = self.buildFeature(e.where)
            m.update(self.invokeFeature(f, req,res))
        f.render(m, res)

        # i thought about letting you chain intercepts and whatnot,
        # but for the time being that's not possible... it wouldn't
        # be hard... you'd just put that above stuff in a loop
