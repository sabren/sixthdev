

class OrthographicCamera(object):

    def __init__(self, camposition=(0,0,0)):
        self.x, self.y, self.z = camposition
	
    def project(self, coord):
        x, y, _ = coord
	return (self.x-x, self.y+y)


class PerspectiveCamera(object):
    pass

