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
        zres = zres + 'h1'
        zres = zres + '>'
        zres = zres + 'Shipping Address'
        zres = zres + '<'
        zres = zres + '/h1'
        zres = zres + '>'
        _ = 0
        _max_ = len(self.model["addressbook"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        scope.update(locals())
        for _ in range(_max_):
            scope.update(self.model["addressbook"][_])
            scope["_"] = _
            if _ == 0:
                zres = zres + '<'
                zres = zres + 'form action=\"checkout.py\" method=\"POST\"'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'h3'
                zres = zres + '>'
                zres = zres + 'Select an address to ship to...'
                zres = zres + '<'
                zres = zres + '/h3'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'select name=\"shipAddressID\"'
                zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'option value=\"'
            zres = zres + str(scope.get('ID',''))
            zres = zres + '\"'
            zres = zres + '>'
            zres = zres + str(scope.get('fname',''))
            zres = zres + '&'
            zres = zres + 'nbsp;'
            zres = zres + str(scope.get('lname',''))
            zres = zres + '/'
            zres = zres + str(scope.get('address1',''))
            zres = zres + '/'
            zres = zres + str(scope.get('city',''))
            zres = zres + '<'
            zres = zres + '/option'
            zres = zres + '>'
            if _ + 1 == _max_:
                zres = zres + '<'
                zres = zres + '/select'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'input type=\"hidden\" name=\"action\" value=\"update\"'
                zres = zres + '>'
                zres = zres + '&'
                zres = zres + 'nbsp;'
                zres = zres + '<'
                zres = zres + 'input type=\"submit\" value=\"submit\"'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + '/form'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'h3'
                zres = zres + '>'
                zres = zres + '... or enter a new address below:'
                zres = zres + '<'
                zres = zres + '/h3'
                zres = zres + '>'
        scope = scope_stack.pop()
        del _
        if not _max_:
            zres = zres + '<'
            zres = zres + 'h3'
            zres = zres + '>'
            zres = zres + 'enter a '
            zres = zres + '<'
            zres = zres + 'b'
            zres = zres + '>'
            zres = zres + 'shipping'
            zres = zres + '<'
            zres = zres + '/b'
            zres = zres + '>'
            zres = zres + ' address below:'
            zres = zres + '<'
            zres = zres + '/h3'
            zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'form action=\"newaddress.py\" method=\"post\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'table border=\"0\"'
        zres = zres + '>'
        import tpl_address
        zres = zres+ tpl_address.fetch(scope)
        zres = zres + '<'
        zres = zres + '/table'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'input type=\"hidden\" name=\"isPrimary\" value=\"0\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'input type=\"hidden\" name=\"context\" value=\"checkout\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'input type=\"hidden\" name=\"whichone\" value=\"ship\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/form'
        zres = zres + '>'
        import tpl_sslfoot
        zres = zres+ tpl_sslfoot.fetch(scope)
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
