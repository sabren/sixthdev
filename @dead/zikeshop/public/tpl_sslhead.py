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
        zres = zres + 'html'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'head'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'title'
        zres = zres + '>'
        zres = zres + 'aggressivemall.com: '
        zres = zres + str(scope.get('title',''))
        zres = zres + '<'
        zres = zres + '/title'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/head'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'body bgcolor=\"#383438\" text=\"#FFFFFF\" link=\"#FFFF00\" vlink=\"#FFFF00\" alink=\"#FFFF00\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'font face=\"verdana\" size=\"2\"'
        zres = zres + '>'
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
