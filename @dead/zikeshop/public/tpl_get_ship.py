class Report:

    def show(self, model={}):
        print self.fetch(model)

    def fetch(self, model={}):
        import copy   # used by scope
        self.model = model
        scope = model
        scope_stack = []
        zres = ""
        import tpl_head
        zres = zres+ tpl_head.fetch(scope)
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
        zres = zres + 'b'
        zres = zres + '>'
        zres = zres + 'name:'
        zres = zres + '<'
        zres = zres + '/b'
        zres = zres + '>'
        zres = zres + 'first: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"fname\" value=\"\"'
        zres = zres + '>'
        zres = zres + ' \nlast: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"lname\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'address 1: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"address1\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'address 2: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"address2\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'address 3: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"address3\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'city: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"city\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'state: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" size=\"2\" name=\"stateCD\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'zip/postal code: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"postal\" value=\"\"'
        zres = zres + '>'
        zres = zres + 'country: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"countryCD\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
        zres = zres + '>'
        zres = zres + 'phone: '
        zres = zres + '<'
        zres = zres + 'input type=\"text\" name=\"phone\" value=\"\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'br'
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
        zres = zres + 'input type=\"submit\" name=\"action\" value=\"save\"'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/form'
        zres = zres + '>'
        import tpl_foot
        zres = zres+ tpl_foot.fetch(scope)
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
