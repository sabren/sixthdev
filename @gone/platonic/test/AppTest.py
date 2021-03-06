from platonic import App
from platonic import Context as Ctx
import unittest

class AppTest(unittest.TestCase):

    def test_chooseAction(self):
        def result_for(req):
            return App(default="the_default").chooseAction(req)
        assert result_for({}) == "the_default"
        assert result_for({"action":"do this"}) == "do_this"

if __name__=="__main__":
    unittest.main()
