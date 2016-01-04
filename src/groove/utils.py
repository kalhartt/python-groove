"""
Utility methods and classes
"""
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
import enum

from groove._groove import ffi, lib


def unique_enum(cls):
    """Make the enum class unique and provide a reverse mapping"""
    cls = enum.unique(cls)
    cls.__values__ = OrderedDict((v.value, v) for v in cls.__members__.values())
    return cls


def property_char_ptr(attr, doc, encoding='utf-8'):
    """Create a property wrapping a char ptr"""
    uattr = '_' + attr

    def getter(self):
        value = getattr(self._obj, attr)
        if value == ffi.NULL:
            return None
        return ffi.string(value).decode(encoding)

    def setter(self, value):
        if value is None:
            setattr(self._obj, attr, ffi.NULL)
            setattr(self, uattr, None)
        else:
            # Keep a reference to this in python
            # or else it will be freed when gc happens
            value = ffi.new('char[]', value.encode(encoding))
            setattr(self._obj, attr, value)
            setattr(self, uattr, value)

    def deleter(self):
        setattr(self._obj, attr, ffi.NULL)
        setattr(self, uattr, None)

    return property(getter, setter, deleter, doc)


def property_convert(attr, from_cdef=None, to_cdef=None, doc=None):
    """Create a rw property wrapping an _obj attribute

    Arguments:
        attr (str): Name of the attribute on the struct
        from_cdef (callable): Function converting the c value to a python object
        to_cdef (callable): Function converting the python object to a c value
        doc (str): Docstring for the property
    """
    def getter(self):
        value = getattr(self._obj, attr)
        if from_cdef:
            value = from_cdef(value)
        return value

    def setter(self, value):
        if to_cdef:
            value = to_cdef(value)
        setattr(self._obj, attr, value)

    return property(getter, setter, doc=doc)
