from platonic import Intercept, Redirect

class App(object):
    def __init__(self, tiles={}, default=None):
        self.tiles = tiles
        self.default = default or "home"
        
    def __call__(self, ctx):
        self.dispatch(ctx)

    def _chooseAction(self, ctx):
        return ctx.req.get("action","").replace(" ","_") or self.default

    def dispatch(self, ctx):
        m = self._chooseAction(ctx)

        # perform the action if necessary:
        if hasattr(self, "on_%s" % m):
            meth = getattr(self, "on_%s" % m)
            try:
                meth(ctx)
            except Redirect, e:
                ctx.res.redirect(e.where)
            except Intercept, e:
                m = e.where
                # @TODO: is this right? intercept doesnt call, but just shows the form?
                # maybe that's what deny should do, and intercept should still do
                # more processing.... 

        # if still here, show any associated templates
        if self.tiles.get(m):
            tile = self.tiles[m]() # call to clear the lambda
            tile.write(ctx)
        else:
            raise Exception("no template defined for %s method." % m)
        return ctx # for easy testing
        
    #@TODO: this part here implies a specific framework (mine). decouple.
    def test(self, ctx, method, **kwargs):
        if kwargs:
            ctx.req = kwargs
        getattr(self, "on_" + method)(ctx)
        return ctx
        
        
