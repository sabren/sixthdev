
class Clerk:
    def __init__(self, store, tables=None):
        self.store = store
        self.tables = tables or {}

    def new(self, klass):
        # this is here because, until we replace recordobject
        # with strongbox, we still need a Connection object
        # so zdc can figure out the slots..
        return klass(self.store)

    def load(self, klass, **where):
        assert where # (if no where clause, call new() instead)
        return klass(self.store, **where)

    def save(self, instance):
        # just delegate for now:
        instance.save()

    def select(self, klass, **wargs):
        return self.store.select(self.tables[klass], **wargs)
