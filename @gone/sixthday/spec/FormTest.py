import unittest
from Form import Form
from strongbox import *

class Model(Strongbox):
    name = attr(str)
    age  = attr(int, default=None)
    prefill = attr(str, default="example")
    limited = attr(str, okay=["a","b","c"], default="a")
    

class FormTest(unittest.TestCase):

    def testInterface(self):
        f = Form(Model())
        assert f["name"] == ""
        assert f["age"] is None
        assert f["prefill"] == "example"

    def testBothways(self):
        f = Form(Model())
        f.model.name = "fred"
        assert f["name"] == "fred"
        f["name"] = "rufus"
        assert f.model.name == "rufus"
        assert f["name"] == "rufus"

    def testValidation(self):
        f = Form(Model())
        try:
            gotError = 0
            f.update({"limited":"bad value",
                      "age":"bad type",
                      "sparky":"bad field"})
        except ValueError:
            gotError = 1

        assert gotError, "expected ValueError"
        assert "age" in f.errors
        assert "limited" in f.errors
        assert "sparky" not in f.errors

    def test_isComplete(self):
        f = Form(Model())
        f.require("age")
        assert not f.isComplete()
        f["age"] = 15
        assert f.isComplete()
        f.require("name","prefill")
        assert not f.isComplete()
        f["name"] = "fred"
        assert f.isComplete()

    def test_keys(self):
        f = Form(Model())
        keys = list(f.keys())
        keys.sort()
        assert keys == ["age","limited","name","prefill"], keys

        # and for non-strongboxes...
        # (YAGNI, probably, but it might help someone else)
        class Gronk: pass
        g = Gronk()
        g.a = 1
        g.b = 2
        g.c = 3
        g._ = "hidden"
        f = Form(g)
        keys = list(f.keys())
        keys.sort()
        assert keys == ["a","b","c"]

    def test_ToDict(self):
        f = Form(Model())
        assert f.toDict() == {"name":"",
                              "age":None,
                              "prefill":"example",
                              "limited":"a"}
       
if __name__=="__main__":
    unittest.main()
