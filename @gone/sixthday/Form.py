
#@TODO: AdminApp should use this Form object.
#@TODO: Form should replace (subclass?) BoxView.

class Form:
    """
    I provide dictionary-like access to my model
    and check it for required fields
    """
    def __init__(self, model):
        self.model = model
        self.errors = {}
        self.required = []

    ## dictionary interface #############

    def __getitem__(self, key):
        return getattr(self.model, key)

    def __setitem__(self, key, value):
        setattr(self.model, key, value)

    def update(self, data):
        self.errors = {}
        for k,v in data.items():
            if hasattr(self.model, k):
                try:
                    setattr(self.model, k, v)
                except (ValueError, TypeError), e:
                    self.errors[k]="Invalid %s: %s" % (k, v)
        if self.errors:
            raise ValueError, "invalid data, see self.errors"

    def keys(self):
        if hasattr(self.model, "__attrs__"):
            return self.model.__attrs__.keys()
        else:
            return tuple([a for a in dir(self.model) if not a.startswith("_")])

    ## extra stuff ######################

    def toDict(self):
        d = {}
        for field in self.keys():
            d[field] = self[field]
        return d
        

    def require(self, *fields):
        for field in fields:
            self.required.append(field)

    def isComplete(self):
        res = True
        for field in self.required:
            if getattr(self.model, field) in ["",None]:
                self.errors[field] = "A value is required for %s." % field
                res = False
        return res
