

OPS = {
    "&"         : "AND",
    "|"         : "OR",
    "startswith": "LIKE",
    "endswith"  : "LIKE",
    }

class QueryExpression(object):

    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation
        #@TODO: remove this!
        self.pattern = (left, right, operation)

    
    def __and__(self, other):
        return QueryExpression(self, other, '&')

    def __or__(self, other):
        return QueryExpression(self, other, '|')

    def __str__(self):
        format = isinstance(self.right, QueryExpression) and '(%s %s %s)' or "(%s %s '%s')" 
        right = self.operation == "startswith" and "%s%%" % self.right or self.right
        right = self.operation == "endswith" and "%%%s" % right or right
        op = OPS.get(self.operation, self.operation)
        return format % (self.left, op, str(right))

class QueryBuilder(object):

    def __init__(self, name=''):
        self._name = name

    def __eq__(self, other):
        return QueryExpression(self._name, other, '=') 

    def __ne__(self, other):
        return QueryExpression(self._name, other, '!=') 

    def __lt__(self, other):
        return QueryExpression(self._name, other, '<') 
    
    def __gt__(self, other):
        return QueryExpression(self._name, other, '>')

    def __ge__(self, other):
        return QueryExpression(self._name, other, '>=')
    
    def __le__(self, other):
        return QueryExpression(self._name, other, '<=')

    def startswith(self, other):
        return QueryExpression(self._name, other, 'startswith') 

    def endswith(self, other):
        return QueryExpression(self._name, other, 'endswith') 

    def __str__(self):
        return self._name
