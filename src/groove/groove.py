"""
Module providing wrapper classes for a pythonic interface to libgroove.so
"""
from __future__ import absolute_import, unicode_literals

from enum import IntEnum
from functools import wraps
from weakref import WeakValueDictionary

from groove import _constants
from groove import utils
from groove._groove import ffi, lib


__all__ = [
    'Channel',
    'ChannelLayout',
    'GrooveClass',
    'SampleFormat',
    'init',
    'libgroove_version',
    'libgroove_version_info',
]


def libgroove_version():
    """libgroove version as a string"""
    return ffi.string(lib.groove_version()).decode('utf-8')


def libgroove_version_info():
    """libgroove version as a tuple"""
    return (
        lib.groove_version_major(),
        lib.groove_version_minor(),
        lib.groove_version_patch(),
    )


def init():
    import atexit
    lib.groove_init()
    atexit.register(lib.groove_finish)


class GrooveClass(object):
    """Base class for all objects backed by a groove struct via cffi

    The attributes and methods defined on this base class will be API stable,
    but their usage is highly discouraged!

    No two python instances should wrap the same underlying C struct.

    Attributes:
        _ffitype (str): Type of the underlying object as used in `ffi.new`,
                        e.g. `'struct GrooveFile *'`
        _obj (cffi.cdata): The backing struct, if it has been instantiated.
    """
    _ffitype = None
    __obj = None

    # Keep a map of `cdata -> instance` so we can get the right
    # instance when a C function gives us a struct pointer.
    _obj_instance_map = WeakValueDictionary()

    @property
    def _obj(self):
        return self.__obj

    @_obj.setter
    def _obj(self, value):
        if value == ffi.NULL:
            value = None

        if value is not None and ffi.typeof(value) is not ffi.typeof(self._ffitype):
            raise TypeError('obj must be of type "%s"' % cls._ffitype)

        if self.__obj is not None:
            del self._obj_instance_map[(self.__obj, self._ffitype)]

        self.__obj = value
        if value is not None:
            self._obj_instance_map[(value, self._ffitype)] = self

    @classmethod
    def _from_obj(cls, obj):
        """Get a Python instance for the cdata obj

        Arguments:
            obj (cffi.cdata): The struct to wrap

        Returns:
            A tuple (instance, created) where instance is a python object
            wrapping `obj`. `created` is `False` if an existing instance was
            found and returned. It is `True` if a new python instance was
            created.
        """
        if ffi.typeof(obj) is not ffi.typeof(cls._ffitype):
            raise TypeError('obj must be of type "%s"' % cls._ffitype)

        instance = cls._obj_instance_map.get((obj, cls._ffitype), None)
        if instance is not None:
            return instance, False

        # TODO: This makes me feel terrible and hate everything :(
        instance = cls.__new__(cls)
        instance._obj = obj
        return instance, True


@utils.unique_enum
class Channel(IntEnum):
    """
    Integer enumeration for audio channels and channel layouts.

    Each audio channel is a power of two to be used as a bitmask

    Attributes:
        front_left
        front_right
        front_center
        low_frequency
        back_left
        back_right
        left_of_center
        right_of_center
        back_center
        side_left
        side_right
        top_center
        top_front_left
        top_front_center
        top_front_right
        top_back_left
        top_back_center
        top_back_right
        stereo_left
        stereo_right
        wide_left
        wide_right
    """
    front_left = _constants.GROOVE_CH_FRONT_LEFT
    front_right = _constants.GROOVE_CH_FRONT_RIGHT
    front_center = _constants.GROOVE_CH_FRONT_CENTER
    low_frequency = _constants.GROOVE_CH_LOW_FREQUENCY
    back_left = _constants.GROOVE_CH_BACK_LEFT
    back_right = _constants.GROOVE_CH_BACK_RIGHT
    left_of_center = _constants.GROOVE_CH_FRONT_LEFT_OF_CENTER
    right_of_center = _constants.GROOVE_CH_FRONT_RIGHT_OF_CENTER
    back_center = _constants.GROOVE_CH_BACK_CENTER
    side_left = _constants.GROOVE_CH_SIDE_LEFT
    side_right = _constants.GROOVE_CH_SIDE_RIGHT
    top_center = _constants.GROOVE_CH_TOP_CENTER
    top_front_left = _constants.GROOVE_CH_TOP_FRONT_LEFT
    top_front_center = _constants.GROOVE_CH_TOP_FRONT_CENTER
    top_front_right = _constants.GROOVE_CH_TOP_FRONT_RIGHT
    top_back_left = _constants.GROOVE_CH_TOP_BACK_LEFT
    top_back_center = _constants.GROOVE_CH_TOP_BACK_CENTER
    top_back_right = _constants.GROOVE_CH_TOP_BACK_RIGHT
    stereo_left = _constants.GROOVE_CH_STEREO_LEFT
    stereo_right = _constants.GROOVE_CH_STEREO_RIGHT
    wide_left = _constants.GROOVE_CH_WIDE_LEFT
    wide_right = _constants.GROOVE_CH_WIDE_RIGHT


@utils.unique_enum
class ChannelLayout(IntEnum):
    """
    A layout of audio channels, each layout

    Attributes:
        layout_mono
        layout_stereo
        layout_2p1
        layout_2_1
        layout_surround
        layout_3p1
        layout_4p0
        layout_4p1
        layout_2_2
        layout_quad
        layout_5p0
        layout_5p1
        layout_5p0
        layout_5p1
        layout_6p0
        layout_6p0_front
        layout_hexagonal
        layout_6p1
        layout_6p1_back
        layout_6p1_front
        layout_7p0
        layout_7p0_front
        layout_7p1
        layout_7p1_wide
        layout_7p1_wide_back
        layout_octagonal
        layout_stereo_downmix
    """
    # TODO: remove layout prefix and give these better names
    layout_mono = _constants.GROOVE_CH_LAYOUT_MONO
    layout_stereo = _constants.GROOVE_CH_LAYOUT_STEREO
    layout_2p1 = _constants.GROOVE_CH_LAYOUT_2POINT1
    layout_2_1 = _constants.GROOVE_CH_LAYOUT_2_1
    layout_surround = _constants.GROOVE_CH_LAYOUT_SURROUND
    layout_3p1 = _constants.GROOVE_CH_LAYOUT_3POINT1
    layout_4p0 = _constants.GROOVE_CH_LAYOUT_4POINT0
    layout_4p1 = _constants.GROOVE_CH_LAYOUT_4POINT1
    layout_2_2 = _constants.GROOVE_CH_LAYOUT_2_2
    layout_quad = _constants.GROOVE_CH_LAYOUT_QUAD
    layout_5p0 = _constants.GROOVE_CH_LAYOUT_5POINT0
    layout_5p1 = _constants.GROOVE_CH_LAYOUT_5POINT1
    layout_5p0_back = _constants.GROOVE_CH_LAYOUT_5POINT0_BACK
    layout_5p1_back = _constants.GROOVE_CH_LAYOUT_5POINT1_BACK
    layout_6p0 = _constants.GROOVE_CH_LAYOUT_6POINT0
    layout_6p0_front = _constants.GROOVE_CH_LAYOUT_6POINT0_FRONT
    layout_hexagonal = _constants.GROOVE_CH_LAYOUT_HEXAGONAL
    layout_6p1 = _constants.GROOVE_CH_LAYOUT_6POINT1
    layout_6p1_back = _constants.GROOVE_CH_LAYOUT_6POINT1_BACK
    layout_6p1_front = _constants.GROOVE_CH_LAYOUT_6POINT1_FRONT
    layout_7p0 = _constants.GROOVE_CH_LAYOUT_7POINT0
    layout_7p0_front = _constants.GROOVE_CH_LAYOUT_7POINT0_FRONT
    layout_7p1 = _constants.GROOVE_CH_LAYOUT_7POINT1
    layout_7p1_wide = _constants.GROOVE_CH_LAYOUT_7POINT1_WIDE
    layout_7p1_wide_back = _constants.GROOVE_CH_LAYOUT_7POINT1_WIDE_BACK
    layout_octagonal = _constants.GROOVE_CH_LAYOUT_OCTAGONAL
    layout_stereo_downmix = _constants.GROOVE_CH_LAYOUT_STEREO_DOWNMIX

    @classmethod
    def channels(cls, layout):
        """Return the channels used in a layout"""
        return [c for c in Channel.__members__.values() if (layout & c)]

    @classmethod
    def count(cls, layout):
        """Count number of channels in a layout"""
        return lib.groove_channel_layout_count(layout)

    @classmethod
    def default(cls, count):
        """Get the default layout for a given number of channels

        Args:
            count (int): Number of audio channels

        Returns:
            The default layout for count number of channels.
        """
        layout_value = lib.groove_channel_layout_default(count)
        return cls.__values__[layout_value]


@utils.unique_enum
class SampleFormat(IntEnum):
    """
    Enumeration for audio sample formats

    Attributes:
        none
        u8    unsigned 8 bits
        s16   signed 16 bits
        s32   signed 32 bits
        flt   float
        dbl   double
        u8p   unsigned 8 planar
        s16p  signed 16 planar
        s32p  signed 32 planar
        fltp  float planar
        dblp  double planar
    """
    none = _constants.GROOVE_SAMPLE_FMT_NONE
    u8 = _constants.GROOVE_SAMPLE_FMT_U8
    s16 = _constants.GROOVE_SAMPLE_FMT_S16
    s32 = _constants.GROOVE_SAMPLE_FMT_S32
    flt = _constants.GROOVE_SAMPLE_FMT_FLT
    dbl = _constants.GROOVE_SAMPLE_FMT_DBL
    u8p = _constants.GROOVE_SAMPLE_FMT_U8P
    s16p = _constants.GROOVE_SAMPLE_FMT_S16P
    s32p = _constants.GROOVE_SAMPLE_FMT_S32P
    fltp = _constants.GROOVE_SAMPLE_FMT_FLTP
    dblp = _constants.GROOVE_SAMPLE_FMT_DBLP

    def bytes_per_sample(self):
        return lib.groove_sample_format_bytes_per_sample(self)
