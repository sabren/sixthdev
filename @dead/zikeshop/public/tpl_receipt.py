class Report:

    def show(self, model={}):
        print self.fetch(model)

    def fetch(self, model={}):
        import copy   # used by scope
        self.model = model
        scope = model
        scope_stack = []
        zres = ""
        import tpl_sslhead
        zres = zres+ tpl_sslhead.fetch(scope)
        zres = zres + '<'
        zres = zres + 'h2'
        zres = zres + '>'
        zres = zres + 'Thank you!'
        zres = zres + '<'
        zres = zres + '/h2'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'b'
        zres = zres + '>'
        zres = zres + str(scope.get('date',''))
        zres = zres + ' - receipt for '
        zres = zres + '<'
        zres = zres + 'a href=\"http://www.aggressivemall.com/\"'
        zres = zres + '>'
        zres = zres + 'aggressivemall.com'
        zres = zres + '<'
        zres = zres + '/a'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/b'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + '&'
        zres = zres + 'nbsp;'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'table border=\"1\"'
        zres = zres + '>'
        _ = 0
        _max_ = len(self.model["products"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        scope.update(locals())
        for _ in range(_max_):
            scope.update(self.model["products"][_])
            scope["_"] = _
            zres = zres + '<'
            zres = zres + 'tr'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'td'
            zres = zres + '>'
            zres = zres + str(scope.get('label',''))
            if scope.get('quantity','') > 1:
                zres = zres + '<'
                zres = zres + 'b'
                zres = zres + '>'
                zres = zres + '(* '
                zres = zres + str(scope.get('quantity',''))
                zres = zres + ')'
                zres = zres + '<'
                zres = zres + '/b'
                zres = zres + '>'
            zres = zres + '<'
            zres = zres + '/td'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'td align=\"right\"'
            zres = zres + '>'
            zres = zres + '$'
            zres = zres + str(scope.get('subtotal',''))
            zres = zres + '<'
            zres = zres + '/td'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + '/tr'
            zres = zres + '>'
        scope = scope_stack.pop()
        del _
        zres = zres + '<'
        zres = zres + 'tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'td bgcolor=\"#666666\"'
        zres = zres + '>'
        zres = zres + 'SalesTax'
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'td align=\"right\"'
        zres = zres + '>'
        zres = zres + '$'
        zres = zres + str(scope.get('salestax',''))
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'td bgcolor=\"#666666\"'
        zres = zres + '>'
        zres = zres + 'Shipping'
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'td align=\"right\"'
        zres = zres + '>'
        zres = zres + '$'
        zres = zres + str(scope.get('shipping',''))
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/tr'
        zres = zres + '>'
        if scope.get('adjustment',''):
            zres = zres + '<'
            zres = zres + 'tr'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'td bgcolor=\"#666666\"'
            zres = zres + '>'
            zres = zres + 'Adjustment'
            zres = zres + '<'
            zres = zres + '/td'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'td align=\"right\"'
            zres = zres + '>'
            zres = zres + str(scope.get('adjustment',''))
            zres = zres + '<'
            zres = zres + '/td'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + '/tr'
            zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'td bgcolor=\"#000000\"'
        zres = zres + '>'
        zres = zres + 'Total'
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'td align=\"right\"'
        zres = zres + '>'
        zres = zres + '$'
        zres = zres + str(scope.get('total',''))
        zres = zres + '<'
        zres = zres + '/td'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/tr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/table'
        zres = zres + '>'
        import tpl_sslfoot
        zres = zres+ tpl_sslfoot.fetch(scope)
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
