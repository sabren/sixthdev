
from py3d import OrthographicCamera
import unittest

class OrthographicCameraTest(unittest.TestCase):

    def check_Projection(self):
	cam = OrthographicCamera()
    	assert cam.project((-2, 2, 6)) == (-2, 2)
	assert cam.project((2, 0, 6)) == (2, 0)

    def check_movement(self):
        # whtever's directly in front of the camera
        # should appear at (0,0)
        cam = OrthographicCamera((10,0,-10))
        assert cam.project((10,0,10)) == (0,0)

