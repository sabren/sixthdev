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
        zres = zres + 'hr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'h4'
        zres = zres + '>'
        zres = zres + '(ZS)'
        zres = zres + '<'
        zres = zres + '/h4'
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
