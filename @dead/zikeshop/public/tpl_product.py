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
        zres = zres + str(scope.get('name',''))
        zres = zres + '<'
        zres = zres + '/h1'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'h4'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'font color=\"yellow\"'
        zres = zres + '>'
        zres = zres + '$'
        zres = zres + str(scope.get('price',''))
        zres = zres + '<'
        zres = zres + '/font'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + '/h4'
        zres = zres + '>'
        if scope.get('pictureID',''):
            zres = zres + '<'
            zres = zres + 'img src=\"'
            zres = zres + str(scope.get('basehref',''))
            zres = zres + '/picture.py?ID='
            zres = zres + str(scope.get('pictureID',''))
            zres = zres + '\"'
            zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'p'
        zres = zres + '>'
        zres = zres + str(scope.get('descript',''))
        zres = zres + '<'
        zres = zres + '/p'
        zres = zres + '>'
        _ = 0
        _max_ = len(self.model["styles"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        scope.update(locals())
        for _ in range(_max_):
            scope.update(self.model["styles"][_])
            scope["_"] = _
            if scope.get('instock',''):
                if not scope.get('style',''):
                    zres = zres + '<'
                    zres = zres + 'A HREF=\"'
                    zres = zres + str(scope.get('basehref',''))
                    zres = zres + '/cart.py?action=add'
                    zres = zres + '&'
                    zres = zres + 'styleID='
                    zres = zres + str(scope.get('ID',''))
                    zres = zres + '\"'
                    zres = zres + '>'
                    zres = zres + 'add to cart'
                    zres = zres + '<'
                    zres = zres + '/a'
                    zres = zres + '>'
                else:
                    zres = zres + 'style: '
                    zres = zres + str(scope.get('style',''))
                    zres = zres + '&'
                    zres = zres + 'nbsp;'
                    zres = zres + '<'
                    zres = zres + 'a href=\"'
                    zres = zres + str(scope.get('basehref',''))
                    zres = zres + '/cart.py?action=add'
                    zres = zres + '&'
                    zres = zres + 'styleID='
                    zres = zres + str(scope.get('ID',''))
                    zres = zres + '\"'
                    zres = zres + '>'
                    zres = zres + '\nadd to cart'
                    zres = zres + '<'
                    zres = zres + '/a'
                    zres = zres + '>'
                    zres = zres + '<'
                    zres = zres + 'br'
                    zres = zres + '>'
            else:
                if not scope.get('style',''):
                    zres = zres + '(this product is not in stock)'
                    zres = zres + '<'
                    zres = zres + 'br'
                    zres = zres + '>'
                else:
                    zres = zres + 'style: '
                    zres = zres + str(scope.get('style',''))
                    zres = zres + ' (this style is not in stock)'
                    zres = zres + '<'
                    zres = zres + 'br'
                    zres = zres + '>'
        scope = scope_stack.pop()
        del _
        _ = 0
        _max_ = len(self.model["nodes"])
        scope_stack.append(scope)
        scope = copy.copy(scope)
        scope.update(locals())
        for _ in range(_max_):
            scope.update(self.model["nodes"][_])
            scope["_"] = _
            if _ == 0:
                zres = zres + '<'
                zres = zres + 'font face=\"verdana\" size=\"3\"'
                zres = zres + '>'
                zres = zres + 'this product is in these categories:'
                zres = zres + '<'
                zres = zres + '/font'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'br'
                zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'a href=\"'
            zres = zres + str(scope.get('basehref',''))
            zres = zres + '/category/'
            zres = zres + str(scope.get('encpath',''))
            zres = zres + '\"'
            zres = zres + '>'
            zres = zres + str(scope.get('path',''))
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
            zres = zres + 'font face=\"verdana\" size=\"2\"'
            zres = zres + '>'
            zres = zres + 'this product is not categorized.'
            zres = zres + '<'
            zres = zres + '/font'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'br'
            zres = zres + '>'
        import tpl_foot
        zres = zres+ tpl_foot.fetch(scope)
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
