
import operator
from storage import where

class Storage(object):

    def store(self, table, **row):
        if row.get("ID"):
            return self._update(table, **row)
        else:
            return self._insert(table, **row)

    def fetch(self, table, ID):
        res = self.match(table, where("ID")==ID)
        if len(res)!=1:
            raise LookupError, "match(%r, ID=%r) returned %i rows." \
                  % (table, ID, len(res))
        return res[0]


    ## abstract:

    def delete(self, table, ID):
        raise NotImplementedError
        
    def match(self, table, whereClause=None, orderBy=None, **simple):      
        assert not (whereClause and simple), \
               "where/simple queries are mutually exclusive"
        if simple:
            whereClause = reduce(operator.and_,
                                 [where(k)==simple[k] for k in simple])
        return self._match(table, whereClause, orderBy)

    def _match(self, table, where, orderBy=None):          
        raise NotImplementedError
    
    def _insert(self, table, **row):
        raise NotImplementedError

    def _update(self, table, **row):
        raise NotImplementedError
