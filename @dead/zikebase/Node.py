
import zdc
import zikebase

class Node(zdc.RecordObject):
    _table = zdc.Table(zikebase.dbc, "base_node")
    _defaults = {"parentID" : 0 }

    def getChildren(self):
        res = []
        cur = self._table.dbc.cursor()
        if self.ID:
            cur.execute("select ID from base_node where parentID=%s" % self.ID)
            for row in cur.fetchall():
                res.append(Node(ID=row[0]))

        return res
        

    def _updatePaths(self, parent=None):
        # this is a recursive version.. It's probably really slow.

        if parent:
            self.__dict__["path"] = parent.path + "/" + self.name
        else:
            self.__dict__["path"] = self.name
        
        for child in self.getChildren():
            child._updatePaths(parent=self)
            child.save()  


    def set_path(self, value):
        raise TypeError, "path is read only."


    def set_name(self, value):
        # we set the name attribute:
        self.__dict__["name"]=value

        # and the paths for us and all our descendents:
        self._updatePaths(self.parent)


    def set_parentID(self, value):

        assert value != self.ID, \
               "A node can't be its own parent!"
        
        
        self.__dict__["parentID"]=int(value)
        self._updatePaths(self.parent)

        

    def get_parent(self):
        if self.parentID:
            return Node(ID=self.parentID)
        else:
            return None
            

    def delete(self):
        assert not self.getChildren(), \
               "Cannot delete a Node that has children."
        zdc.RecordObject.delete(self)
