
if 1:
    class TwistedTest: pass
else:
    import os
    import unittest
    from twisted.test.test_web import DummyRequest
    from weblib.misc import weblibtwisted


    class TwistedTest(unittest.TestCase):
        def test_render(self):
            import weblib
            base = os.path.split(weblib.__file__)[0]
            resource = weblibtwisted.RantResource(os.path.join(
                *[base, 'spec', 'twisted.app']), None)
            request = DummyRequest([]) # The url segments below resource to request
            result = resource.render(request)
            self.assert_(result)
