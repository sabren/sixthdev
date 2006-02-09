"""
vector math routines
"""
__ver__="$Id$"
try:
    import Numeric
except:
    Numeric = None

if Numeric is None:
    try: import numpy as Numeric
    except ImportError: raise ImportError ("no numeric like thing found")

    
import math

def magnitude(vec):
    """
    returns the geometric length of the vector
    """
    return Numeric.sqrt(Numeric.sum(vec**2))

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
    return Numeric.innerproduct(normalize(a), normalize(b))


if __name__=="__main__":
    
    '''
    For these tests, imagein that we have a 2-D graph of
    various "documents":
    
        x axis is the "dog" axis
        y axis is the "cat" axis
    
    We could then graph the following documents:
    
        b          a = 'cat'
        |          b = 'cat cat'
        a  c       c = 'dog cat'
        | /        d = 'dog'
        |/__d
    
    As you can see, the more similar two documents are,
    the smaller the angle between them. We can calculate
    this angle for any number of dimensions using the
    vcos() routine (thanks, linear algebra!)
    '''
    
    cat    = Numeric.array([0,1])
    catcat = Numeric.array([0,2])
    dogcat = Numeric.array([1,1])
    dog    = Numeric.array([1,0])
    
    assert magnitude(cat) == 1
    assert magnitude(catcat) == 2
    assert magnitude(dogcat) == math.sqrt(2) # a^2+b^2=c^2
    assert magnitude(dog) == 1
    
    assert normalize(cat) == Numeric.array([0,1])
    assert normalize(catcat) == Numeric.array([1,1])
    assert normalize(dogcat) == Numeric.array([1/math.sqrt(2), 1/math.sqrt(2)])
    assert normalize(dog) == Numeric.array([1,0])
    
    assert round(vcos(cat, cat), 3) == round(dcos(0),3)
    assert round(vcos(cat, catcat), 3) == round(dcos(0),3)
    assert round(vcos(cat, dogcat), 3) == round(dcos(45),3)
    assert round(vcos(cat, dog), 3) == round(dcos(90),3)
    
    
