
class Model(dict):
    # for assertions in unit tests:
    isModel, isRedirect = True, False
    
    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self.update(kwargs)

    def __getattr__(self, key):
        """
        this lets you access via . instead of []
        """
        return self[key]
