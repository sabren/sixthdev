
class Clerk:
    def __init__(self, store):
        self.store = store

    def new(self, klass):
        # this is here because, until we replace recordobject
        # with strongbox, we still need a Connection object
        # so zdc can figure out the slots..
        return klass(self.store, "isclerk")

    def load(self, klass, **where):
        assert where # (if no where clause, call new() instead)
        return klass(self.store, "isclerk", **where)

    def save(self, instance):
        pass

