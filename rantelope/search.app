
import zebra
from rantelope import Story
from sixthday import App
from strongbox import BoxView

class SearchApp(App):
    def __init__(self, index, input):
        self.index = index
        super(SearchApp, self).__init__(input)

    def act_(self):
        self.model["errors"]=[]
        self.model["results"]=[]
        self.model.setdefault("query", "")       
        if self.input.get("query"):
            matches = self.index.search(self.input["query"])
            self.model["results"]=[BoxView(s) for s in matches]
        print >> self, zebra.fetch("search", self.model)
        


if __name__=="__main__":
    from sqlRantelope import index
    print >> RES, SearchApp(index, REQ).act()
