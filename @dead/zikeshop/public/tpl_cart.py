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
        zres = zres + 'h1'
        zres = zres + '>'
        zres = zres + 'Your Shopping Cart'
        zres = zres + '<'
        zres = zres + '/h1'
        zres = zres + '>'
        _ = 0
        _max_ = len(self.model["contents"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        for _ in range(_max_):
            scope.update(self.model["contents"][_])
            if _ == 0:
                zres = zres + '<'
                zres = zres + 'h4'
                zres = zres + '>'
                zres = zres + 'contents of cart:'
                zres = zres + '<'
                zres = zres + '/h4'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'form action=\"cart.py\" method=\"POST\"'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'ul'
                zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'li'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'a href=\"'
            zres = zres + str(scope['link'])
            zres = zres + '\"'
            zres = zres + '>'
            zres = zres + str(scope['label'])
            zres = zres + '<'
            zres = zres + '/a'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'input name=\"quantity_'
            zres = zres + str(scope['_'])
            zres = zres + '\" size=\"3\" value=\"'
            zres = zres + str(scope['quantity'])
            zres = zres + '\"'
            zres = zres + '>'
            if _ + 1 == _max_:
                zres = zres + '<'
                zres = zres + '/ul'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'input type=\"submit\" name=\"action\" value=\"update\"'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + '/form'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'a href=\"checkout.py\"'
                zres = zres + '>'
                zres = zres + 'checkout'
                zres = zres + '<'
                zres = zres + '/a'
                zres = zres + '>'
        scope = scope_stack.pop()
        del _
        if not _max_:
            zres = zres + '<'
            zres = zres + 'h4'
            zres = zres + '>'
            zres = zres + 'your cart is empty'
            zres = zres + '<'
            zres = zres + '/h4'
            zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'hr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'a href=\"'
        zres = zres + str(scope['basehref'])
        zres = zres + '/category/\"'
        zres = zres + '>'
        zres = zres + 'top'
        zres = zres + '<'
        zres = zres + '/a'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'hr'
        zres = zres + '>'
        zres = zres + 'zikeshop alpha (c)2000 zike interactive, inc\n'
# end of Report.fetch()
        return zres

def fetch(model={}):
    Report().fetch(model)
    
def show(model={}):
    Report().show(model)

