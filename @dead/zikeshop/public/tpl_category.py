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
        if scope.get('name',''):
            zres = zres + '<'
            zres = zres + 'h1'
            zres = zres + '>'
            zres = zres + '<'
            zres = zres + 'a href=\"'
            zres = zres + str(scope.get('basehref',''))
            zres = zres + '/category\"'
            zres = zres + '>'
            zres = zres + 'top'
            zres = zres + '<'
            zres = zres + '/a'
            zres = zres + '>'
            zres = zres + ' :'
            _ = 0
            _max_ = len(self.model["crumbs"])
            scope_stack.append(scope)
            scope = copy.copy(scope)
            scope.update(locals())
            for _ in range(_max_):
                scope.update(self.model["crumbs"][_])
                scope["_"] = _
                zres = zres + '<'
                zres = zres + 'a href=\"'
                zres = zres + str(scope.get('basehref',''))
                zres = zres + '/category/'
                zres = zres + str(scope.get('path',''))
                zres = zres + '\"'
                zres = zres + '>'
                zres = zres + str(scope.get('name',''))
                zres = zres + '<'
                zres = zres + '/a'
                zres = zres + '>'
                zres = zres + ' :'
            scope = scope_stack.pop()
            del _
            zres = zres + str(scope.get('name',''))
            zres = zres + '<'
            zres = zres + '/h1'
            zres = zres + '>'
            _ = 0
            _max_ = len(self.model["children"])
            scope_stack.append(scope)
            scope = copy.copy(scope)
            scope.update(locals())
            for _ in range(_max_):
                scope.update(self.model["children"][_])
                scope["_"] = _
                if _ == 0:
                    zres = zres + '<'
                    zres = zres + 'h2'
                    zres = zres + '>'
                    zres = zres + 'subcategories'
                    zres = zres + '<'
                    zres = zres + '/h2'
                    zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'a href=\"'
                zres = zres + str(scope.get('basehref',''))
                zres = zres + '/category/'
                zres = zres + str(scope.get('path',''))
                zres = zres + '\"'
                zres = zres + '>'
                zres = zres + str(scope.get('name',''))
                zres = zres + '<'
                zres = zres + '/a'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'br'
                zres = zres + '>'
            scope = scope_stack.pop()
            del _
            _ = 0
            _max_ = len(self.model["products"])
            scope_stack.append(scope)
            scope = copy.copy(scope)
            scope.update(locals())
            for _ in range(_max_):
                scope.update(self.model["products"][_])
                scope["_"] = _
                if _ == 0:
                    zres = zres + '<'
                    zres = zres + 'h2'
                    zres = zres + '>'
                    zres = zres + 'Products in this Category:'
                    zres = zres + '<'
                    zres = zres + '/h2'
                    zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'a href=\"'
                zres = zres + str(scope.get('basehref',''))
                zres = zres + '/product/'
                zres = zres + str(scope.get('code',''))
                zres = zres + '\"'
                zres = zres + '>'
                zres = zres + str(scope.get('name',''))
                zres = zres + '<'
                zres = zres + '/a'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'br'
                zres = zres + '>'
            scope = scope_stack.pop()
            del _
            if not _max_:
                zres = zres + '(No products in this category.)\n\n'
        else:
            zres = zres + '<'
            zres = zres + 'h1'
            zres = zres + '>'
            zres = zres + 'top'
            zres = zres + '<'
            zres = zres + '/h1'
            zres = zres + '>'
            _ = 0
            _max_ = len(self.model["children"])
            scope_stack.append(scope)
            scope = copy.copy(scope)
            scope.update(locals())
            for _ in range(_max_):
                scope.update(self.model["children"][_])
                scope["_"] = _
                if _ == 0:
                    zres = zres + '<'
                    zres = zres + 'h2'
                    zres = zres + '>'
                    zres = zres + 'Categories'
                    zres = zres + '<'
                    zres = zres + '/h2'
                    zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'a href=\"'
                zres = zres + str(scope.get('basehref',''))
                zres = zres + '/category/'
                zres = zres + str(scope.get('path',''))
                zres = zres + '\"'
                zres = zres + '>'
                zres = zres + str(scope.get('name',''))
                zres = zres + '<'
                zres = zres + '/A'
                zres = zres + '>'
                zres = zres + '<'
                zres = zres + 'br'
                zres = zres + '>'
            scope = scope_stack.pop()
            del _
        zres = zres + '<'
        zres = zres + 'hr'
        zres = zres + '>'
        zres = zres + '<'
        zres = zres + 'a href=\"'
        zres = zres + str(scope.get('basehref',''))
        zres = zres + '/cart.py\"'
        zres = zres + '>'
        zres = zres + 'view cart'
        zres = zres + '<'
        zres = zres + '/a'
        zres = zres + '>'
        import tpl_foot
        zres = zres+ tpl_foot.fetch(scope)
# end of Report.fetch()
        return zres

def fetch(model={}):
    return Report().fetch(model)
    
def show(model={}):
    return Report().show(model)
