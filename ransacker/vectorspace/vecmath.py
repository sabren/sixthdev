"""
vector math routines
"""
__ver__="$Id$"

import numpy
import math

def magnitude(vec):
    """
    returns the geometric length of the vector
    """
    return numpy.sqrt(numpy.sum(vec**2))

def normalize(vec):
    return vec/magnitude(vec)

def deg2rad(d):
    return d * math.pi / 180

def dcos(d):
    """
    cosine(degrees)
    """
    return math.cos(deg2rad(d))

def vcos(a,b):
    """
    cosine of angle between two vectors
    """
    return numpy.inner(normalize(a), normalize(b))


