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
        zres = zres + str(scope['name'])
        zres = zres + '<'
        zres = zres + '/h1'
        zres = zres + '>'
        if scope['pictureID']:
            zres = zres + '<'
            zres = zres + 'img src=\"picture.py?ID='
            zres = zres + str(scope['pictureID'])
            zres = zres + '\"'
            zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'p'
        zres = zres + '>'
        zres = zres + str(scope['descript'])
        zres = zres + '<'
        zres = zres + '/p'
        zres = zres + '>'
        _ = 0
        _max_ = len(self.model["styles"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        for _ in range(_max_):
            scope.update(self.model["styles"][_])
            if not scope['style']:
                zres = zres + '<'
                zres = zres + 'A HREF=\"'
                zres = zres + str(scope['basehref'])
                zres = zres + '/cart.py?action=add'
                zres = zres + '&'
                zres = zres + 'styleID='
                zres = zres + str(scope['ID'])
                zres = zres + '\"'
                zres = zres + '>'
                zres = zres + 'add to cart'
                zres = zres + '<'
                zres = zres + '/a'
                zres = zres + '>'
            else:
                zres = zres + 'style: '
                zres = zres + str(scope['style'])
                zres = zres + '<'
                zres = zres + 'a href=\"'
                zres = zres + str(scope['basehref'])
                zres = zres + '/cart.py?action=add'
                zres = zres + '&'
                zres = zres + 'styleID='
                zres = zres + str(scope['ID'])
                zres = zres + '\"'
                zres = zres + '>'
                zres = zres + 'add to cart'
                zres = zres + '<'
                zres = zres + '/a'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'br'
                zres = zres + '>'
        scope = scope_stack.pop()
        del _
        _ = 0
        _max_ = len(self.model["nodes"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        for _ in range(_max_):
            scope.update(self.model["nodes"][_])
            if _ == 0:
                zres = zres + '<'
                zres = zres + 'h2'
                zres = zres + '>'
                zres = zres + 'this product is in these categories:'
                zres = zres + '<'
                zres = zres + '/h2'
                zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'a href=\"'
            zres = zres + str(scope['basehref'])
            zres = zres + '/category/'
            zres = zres + str(scope['path'])
            zres = zres + '\"'
            zres = zres + '>'
            zres = zres + str(scope['path'])
            zres = zres + '<'
            zres = zres + '/a'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'br'
            zres = zres + '>'
        scope = scope_stack.pop()
        del _
        if not _max_:
            zres = zres + '<'
            zres = zres + 'h2'
            zres = zres + '>'
            zres = zres + 'this product is not categorized.'
            zres = zres + '<'
            zres = zres + '/h2'
            zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'hr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'a href=\"cart.py\"'
        zres = zres + '>'
        zres = zres + 'view cart'
        zres = zres + '<'
        zres = zres + '/a'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'hr'
        zres = zres + '>'
        zres = zres + 'zikeshop alpha (c)2000 zike interactive, inc\n\n\n'
# end of Report.fetch()
        return zres

def fetch(model={}):
    Report().fetch(model)
    
def show(model={}):
    Report().show(model)

