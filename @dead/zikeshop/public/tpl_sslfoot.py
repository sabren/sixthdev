class Report:

    def show(self, model={}):
        print self.fetch(model)

    def fetch(self, model={}):
        import copy   # used by scope
        self.model = model
        scope = model
        scope_stack = []
        zres = ""
        zres = zres + '<'
        zres = zres + '/font'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/table'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/table'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/body'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/html'
        zres = zres + '>'
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
