"""
Utility methods and classes
"""
from collections import OrderedDict
import enum

def unique_enum(cls):
    """Make the enum class unique and provide a reverse mapping"""
    cls = enum.unique(cls)
    cls.__values__ = OrderedDict((v.value, v) for v in cls.__members__.values())
    return cls
