"""
zdc.Object - a base class for building database objects
"""
__ver__ = "$Id$"


class Object(object):
    """
    A base class for building business objects.

    zdc.Object is a generic base class for business
    objects. It has the ability to reject adding
    attributes that don't apply to it.

    see RecordObject and ModelObject (?) for examples..
    """
