# zdc.Field

class Field:

    def __init__(self, name, type, displaySize=None, internalSize=None,
                 precision=None, scale=None, allowNull=None, default=None,
                 isGenerated=None):
        self.name = name
        self.type = type
        self.displaySize = displaySize
        self.internalSize = internalSize
        self.precision = precision
        self.scale = scale
        self.allowNull = allowNull
        self.default = default
        self.isGenerated = isGenerated
