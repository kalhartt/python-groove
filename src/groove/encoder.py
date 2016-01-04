from __future__ import absolute_import, unicode_literals

from groove import _constants
from groove import utils
from groove._groove import ffi, lib
from groove.audio_format import AudioFormat
from groove.buffer import Buffer
from groove.groove import GrooveClass


__all__ = ['Encoder']


class Encoder(GrooveClass):
    """Groove Encoder"""
    _ffitype = 'struct GrooveEncoder *'

    BufferClass = Buffer

    format_short_name = utils.property_char_ptr('format_short_name',
        """Short name of the format

        Optional - choose a short name for the format to help libgroove choose
        which format to use. Use `avconfig -formats` to get a list of possibilities
        """)

    codec_short_name = utils.property_char_ptr('codec_short_name',
        """Short name of the codec

        Optional - choose a short name for the codec to help libgroove choose
        which codec to use. Use `avconfig -codecs` to get a list of possibilities
        """)

    filename = utils.property_char_ptr('filename',
        """An example filename

        Optional - provide an example filename to help libgroove guess which
        format/codec to use.
        """)

    mime_type = utils.property_char_ptr('mime_type',
        """A mime type string

        Optional - provide a mime type string to help libgroove guess which
        format/codec to use.
        """)

    bit_rate = utils.property_convert('bit_rate', int,
        doc="""Target encoding quality in bits per second

        Select encoding quality by choosing a target bit rate in bits per
        second. Note that typically you see this expressed in "kbps", such as
        320kbps or 128kbps. Surprisingly, in this circumstance 1 kbps is 1000
        bps, *not* 1024 bps as you would expect. This defaults to 256000.
        """)

    sink_buffer_size = utils.property_convert('sink_buffer_size', int,
        doc="""How big the sink buffer should be, in sample frames.

        This defaults to 8192.
        """)

    encoded_buffer_size = utils.property_convert('encoded_buffer_size', int,
        doc="""How big the encoded buffer should be, in bytes.

        This defaults to 16384.
        """)

    @property
    def actual_audio_format(self):
        fmt_obj = ffi.addressof(self._obj.actual_audio_format)
        fmt, _ = AudioFormat._from_obj(fmt_obj)
        return fmt

    @property
    def target_audio_format(self):
        fmt_obj = ffi.addressof(self._obj.target_audio_format)
        fmt, _ = AudioFormat._from_obj(fmt_obj)
        return fmt

    @property
    def gain(self):
        """The volume adjustment to make to this player.

        It is recommended to leave this at 1.0 and instead adjust the gain of
        the underlying playlist.
        """
        return float(self._obj.gain)

    @gain.setter
    def gain(self, value):
        lib.groove_encoder_set_gain(self._obj, value)

    @property
    def playlist(self):
        return self._playlist

    @playlist.setter
    def playlist(self, value):
        # TODO: better exception handling
        if self._playlist:
            assert lib.groove_encoder_detach(self._obj) == 0
            self._playlist = None

        assert lib.groove_encoder_attach(self._obj, value._obj) == 0
        self._playlist = value

    def __init__(self):
        # TODO: better exception handling
        obj = lib.groove_encoder_create()
        assert obj != ffi.NULL
        self._obj = ffi.gc(obj, lib.groove_encoder_destroy)
        self._playlist = None

    @property
    def disable_resample(self):
        """Set this flag to ignore audio_format.

        If you set this flag, the buffers you pull from this could have
        any audio format.
        """
        return self._obj.disable_resample

    @disable_resample.setter
    def disable_resample(self, value):
        if value:
            self._obj.disable_resample = 1

    @property
    def buffer_sample_count(self):
        """Number of frames to pull into a buffer

        If set to the default of 0, groove will choose a sample count based on
        efficiency.
        """
        return self._obj.buffer_sample_count

    @buffer_sample_count.setter
    def buffer_sample_count(self, value):
        self._obj.buffer_sample_count = value

    @property
    def buffer_size(self):
        """Buffer queue size in frames, default 8192"""
        return self._obj.buffer_size

    @buffer_size.setter
    def buffer_size(self, value):
        self._obj.buffer_size = value

    @property
    def gain(self):
        """Volume adjustment for the audio

        It is recommended to leave this at 1.0 and adjust the playlist/item
        gain instead
        """
        return self._obj.gain

    @gain.setter
    def gain(self, value):
        lib.groove_encoder_set_gain(self._obj, value)

    @property
    def playlist(self):
        return self._playlist

    @playlist.setter
    def playlist(self, value):
        # TODO: better exception handling
        if self._obj.playlist != ffi.NULL:
            assert lib.groove_encoder_detach(self._obj) == 0
        if value is not None:
            assert lib.groove_encoder_attach(self._obj, value._obj) == 0
        self._playlist = value

    @property
    def bytes_per_sec(self):
        """Automatically computed from audio format when attached"""
        return self._obj.bytes_per_sec

    def buffer_peek(self, block=True):
        """Returns True if a buffer is ready, False if not"""
        value = lib.groove_encoder_buffer_peek(self._obj, 1 if block else 0)
        assert value >= 0
        return value == 1

    def get_buffer(self, block=False):
        """Get the buffer on the encoder

        If no buffer is ready, this raises `groove.Buffer.NotReady`
        If the end of the playlist is reached, this raises `groove.Buffer.End`
        If block is True and no buffer is ready, this may block indefinately
        """
        # TODO: add timeout, might have to be done in libgroove to be safe
        buff_obj_ptr = ffi.new('struct GrooveBuffer **')
        value = lib.groove_encoder_buffer_get(self._obj, buff_obj_ptr, 1 if block else 0)
        assert value >= 0

        if value == _constants.GROOVE_BUFFER_NO:
            raise Buffer.NotReady()
        elif value == _constants.GROOVE_BUFFER_END:
            raise Buffer.End()
        elif value == _constants.GROOVE_BUFFER_YES:
            buff, _ = self.BufferClass._from_obj(buff_obj_ptr[0])
            buff.encoder = self
            return buff

        raise Exception('Unknown value %s from groove_encoder_buffer_get' % value)

    def get_tags(self, flags=0):
        """Get the tags for an encoder

        Args:
            flags (int)  Bitmask of tag flags

        Returns:
            A dictionary of `name: value` pairs. Both `name` and `value` will
            be type `bytes`.
        """
        # Have to make a GrooveTag** so cffi doesn't try to sizeof GrooveTag
        gtag_ptr = ffi.new('struct GrooveTag **')
        gtag = gtag_ptr[0]
        tags = OrderedDict()
        while True:
            gtag = lib.groove_encoder_metadata_get(self._obj, b'', gtag, flags)
            if gtag == ffi.NULL:
                break

            key = ffi.string(lib.groove_tag_key(gtag))
            value = ffi.string(lib.groove_tag_value(gtag))
            tags[key] = value

        return tags

    def set_tags(self, tagdict, flags=0):
        """Shortcut to set each flag in tagdict

        This will overwrite existing tags, but will not delete existing tags
        that are not listed in tagdict. To delete a tag, set its value to
        `None`
        """
        for k, v in tagdict.items():
            self.set_tag(k, v, flags)

    def set_tag(self, key, value, flags=0):
        """Set tag `key` to `value`

        If `value` is `None`, the tag will be deleted. `key` and `value` must
        be type `bytes`.
        """
        if value is None:
            value = ffi.NULL

        status = lib.groove_encoder_metadata_set(self._obj, key, value, flags)
        return status

    def decode_position(self):
        """Get the current position of the decode head

        Returns:
            A tuple of (playlist_item, seconds). If the playlist is empty
            playlist_item will be None and seconds will be -1.0
        """
        pitem_obj_ptr = ffi.new('struct GroovePlaylistItem **')
        seconds = ffi.new('double *')
        lib.groove_encoder_position(self._obj, pitem_obj_ptr, seconds)
        return self._pitem(pitem_obj_ptr[0]), float(seconds[0])
