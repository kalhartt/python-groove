from __future__ import absolute_import, unicode_literals

from groove import utils
from groove._groove import ffi, lib
from groove.groove import ChannelLayout
from groove.groove import GrooveClass
from groove.groove import SampleFormat


__all__ = ['AudioFormat']


class AudioFormat(GrooveClass):
    """Groove Audio Format"""
    _ffitype = 'struct GrooveAudioFormat *'

    sample_rate = utils.property_convert('sample_rate',
        from_cdef=int,
        doc="""Sample rate in Hz""")

    channel_layout = utils.property_convert('channel_layout',
        from_cdef=ChannelLayout.__values__.get,
        doc="""ChanelLayout for the audio format""")

    sample_format = utils.property_convert('sample_fmt',
        from_cdef=SampleFormat.__values__.get,
        doc="""SampleFormat for the audio format""")

    def __init__(self):
        self._obj = ffi.new(self._ffitype)

    def __eq__(self, rhs):
        if not isinstance(rhs, AudioFormat):
            return False
        return lib.groove_audio_formats_equal(self._obj, rhs._obj) == 1

    def clone(self, other):
        """Set this AudioFormat equal to another format"""
        self.sample_rate = other.sample_rate
        self.channel_layout = other.channel_layout
        self.sample_format = other.sample_format
