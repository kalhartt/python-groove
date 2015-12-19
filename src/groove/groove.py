"""
Module providing wrapper classes for a pythonic interface to libgroove.so
"""
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from enum import IntEnum
from functools import wraps

from groove import _constants
from groove import utils
from groove._groove import ffi, lib


__all__ = [
    'AudioFormat',
    'Channel',
    'ChannelLayout',
    'SampleFormat',
    'init',
    'libgroove_version',
    'libgroove_version_info',
    'finish',
]


def libgroove_version():
    """libgroove version as a string"""
    return lib.groove_version()


def libgroove_version_info():
    """libgroove version as a tuple"""
    return (
        lib.groove_version_major(),
        lib.groove_version_minor(),
        lib.groove_version_patch(),
    )


def init():
    lib.groove_init()


def finish():
    lib.groove_finish()


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


class AudioFormat(object):
    """Audio Format

    Attributes:
        sample_rate ()
        channel_layout ()
        sample_format ()
    """
    _ffitype = 'struct GrooveAudioFormat *'

    def __init__(self, sample_rate=None, channel_layout=None, sample_format=None, _obj=None):
        if _obj is not None:
            # Initialize from a separately obtained ffi object
            # This class doesn't do any memory management on _obj in this case
            assert ffi.typeof(_obj) is ffi.typeof(self._ffitype)
            self._obj = _obj
            return

        self._obj = ffi.new(self._ffitype)
        for attr in ('sample_rate', 'channel_layout', 'sample_format'):
            value = locals()[attr]
            if value is not None:
                setattr(self, attr, value)

    @property
    def sample_rate(self):
        return self._obj.sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._obj.sample_rate = value

    @property
    def channel_layout(self):
        return ChannelLayout.__values__[self._obj.channel_layout]

    @channel_layout.setter
    def channel_layout(self, value):
        self._obj.channel_layout = value

    @property
    def sample_format(self):
        return SampleFormat.__values__[self._obj.sample_fmt]

    @sample_format.setter
    def sample_format(self, value):
        self._obj.sample_fmt = value

    def __eq__(self, rhs):
        if not isinstance(rhs, AudioFormat):
            return False

        return lib.groove_audio_formats_equal(self._obj, rhs._obj) == 1


class File(object):
    """GrooveFile wrapper

    Args:
        filename (str)  Name of the file to open
    """
    _ffitype = 'struct GrooveFile *'
    tag_match_case = _constants.GROOVE_TAG_MATCH_CASE
    tag_dont_overwrite = _constants.GROOVE_TAG_MATCH_CASE
    tag_append = _constants.GROOVE_TAG_MATCH_CASE

    def __init__(self, filename):
        self._obj = None
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    def _require_open(method):
        # TODO: preserve argspec
        @wraps(method)
        def new_method(self, *args, **kwargs):
            if self._obj is None:
                raise ValueError('File is not open')
            return method(self, *args, **kwargs)
        return new_method

    def open(self):
        """Open the file

        In general this should not be used, use the context manager approach
        when possible
        """
        if self._obj is not None:
            raise ValueError('File is already open')

        self._obj = lib.groove_file_open(self._filename.encode())
        if self._obj == ffi.NULL:
            # TODO: get error from AV_LOG
            self._obj = None
            raise ValueError('I/O error opening file')

    def close(self):
        """Close the file

        In general this should not be used, use the context manager approach
        when possible
        """
        lib.groove_file_close(self._obj or ffi.NULL)
        self._obj = None

    @_require_open
    def save(self):
        """Save changes made to the file"""
        status = lib.groove_file_save(self._obj)
        if status < 0:
            # TODO: Read error msg from AV_LOG
            raise ValueError('Unknown error')

    @_require_open
    def dirty(self):
        """True if unsaved changed have been made to the file"""
        return self._obj.dirty == 1

    @_require_open
    def get_tags(self, flags=0):
        """Get the tags for an open file

        Args:
            flags (int)  Bitmask of tag flags

        Returns:
            A dictionary of `name: value` pairs
        """
        # Have to make a GrooveTag** so cffi doesn't try to sizeof GrooveTag
        gtag_ptr = ffi.new('struct GrooveTag **')
        gtag = gtag_ptr[0]
        tags = OrderedDict()
        while True:
            gtag = lib.groove_file_metadata_get(self._obj, b'', gtag, flags)
            if gtag == ffi.NULL:
                break

            # TODO: figure out proper decoding method here
            # I know ID3 tags have an encoding byte, not sure about what we
            # get from ffmpeg. Also some tags have binary content, maybe
            # we shouldnt decode value at all?
            key = ffi.string(lib.groove_tag_key(gtag)).decode()
            value = ffi.string(lib.groove_tag_value(gtag)).decode()
            tags[key] = value

        return tags

    @_require_open
    def set_tags(self, tagdict, flags=0):
        """Shortcut to set each flag in tagdict

        This will overwrite existing tags, but will not delete existing tags
        that are not listed in tagdict. To delete a tag, set its value to
        `None`
        """
        for k, v in tagdict.items():
            self.set_tag(k, v, flags)

    @_require_open
    def set_tag(self, key, value, flags=0):
        """Set tag `key` to `value`

        If `value` is `None`, the tag will be deleted
        """
        if value is None:
            value = ffi.NULL
        else:
            value = value.encode()

        # TODO: Is system encoding right to use here?
        status = lib.groove_file_metadata_set(self._obj, key.encode(), value, flags)
        return status

    @_require_open
    def short_names(self):
        """A list of short names for the format"""
        names = ffi.string(lib.groove_file_short_names(self._obj)).decode()
        return names.split(',')

    @_require_open
    def duration(self):
        """Get the main audio stream duration in seconds

        Note that this relies on a combination of format headers and
        heuristics. It can be inaccurate. The most accurate way to learn
        the duration of a file is to use GrooveLoudnessDetector.
        """
        return lib.groove_file_duration(self._obj)

    @_require_open
    def audio_format(self):
        audio_format = AudioFormat()
        lib.groove_file_audio_format(self._obj, audio_format._obj)
        return audio_format

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_trackback):
        self.close()
