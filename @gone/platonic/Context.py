
class Context:
    """
    you can use any object as a context.
    this is just handy for oneliners
    """
    def __init__(self, **kwargs):
        self.model = {}
        for k,v in kwargs.items():
            setattr(self,k,v)
