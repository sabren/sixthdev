
from py3d import PerspectiveCamera
import unittest

class PerspectiveCameraTest(unittest.TestCase):

    def check_Projection(self):

        # points directly in front of us should be orthographic
    	cam = PerspectiveCamera((0, 0, -10))
	assert cam.project((0, 0, 10)) == (0, 0)
	assert cam.project((0, 0, 0))  == (0, 0)

        # if we move down and to the right, though, a point directly
        # in front of us only moves a down and little to the right
        # of center because of parallax:
        cam = PerspectiveCamera((10, 10, -10))
        assert cam.project((10, 10, 10)) == (5, 5)

