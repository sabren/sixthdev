

class Range(object):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __contains__(self, item):
        raise NotImplementedError(
            "use InclusiveRange or ExclusiveRange instead")


class ExclusiveRange(Range):

    def __contains__(self, item):
        return self.left < item < self.right


class InclusiveRange(Range):

    def __contains__(self, item):
        return self.left <= item <= self.right
    
