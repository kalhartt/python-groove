from __future__ import absolute_import, unicode_literals

from groove import _constants
from groove import utils
from groove._groove import ffi, lib
from groove.buffer import Buffer
from groove.groove import GrooveClass
from groove.playlist import PlaylistItem


__all__ = ['Sink']


class Sink(GrooveClass):
    """Groove Sink"""
    _ffitype = 'struct GrooveSink *'
    BufferClass = Buffer

    disable_resample = utils.property_convert('disable_resample', bool,
        doc="""Set this flag to ignore audio_format.

        If you set this flag, the buffers you pull from this sink could have
        any audio format.
        """)

    buffer_sample_count = utils.property_convert('buffer_sample_count', int,
        doc="""Number of frames to pull into a buffer

        If set to the default of 0, groove will choose a sample count based on
        efficiency.
        """)

    buffer_size = utils.property_convert('buffer_size', int,
        doc="""Buffer queue size in frames, default 8192""")

    @property
    def audio_format(self):
        """Set this to the audio format you want the sink to output"""
        return AudioFormat._from_obj(self._obj.format)

    @property
    def gain(self):
        """Volume adjustment for the audio sink

        It is recommended to leave this at 1.0 and adjust the playlist/item
        gain instead
        """
        return self._obj.gain

    @gain.setter
    def gain(self, value):
        lib.groove_sink_set_gain(self._obj, value)

    @property
    def playlist(self):
        return self._playlist

    @playlist.setter
    def playlist(self, value):
        # TODO: better exception handling
        if self._obj.playlist != ffi.NULL:
            assert lib.groove_sink_detach(self._obj) == 0
        if value is not None:
            assert lib.groove_sink_attach(self._obj, value._obj) == 0
        self._playlist = value

    @property
    def bytes_per_sec(self):
        """Automatically computed from audio format when attached"""
        return self._obj.bytes_per_sec

    @classmethod
    def _from_obj(cls, obj):
        instance, created = super(Sink, cls)._from_obj(obj)
        if created:
            # TODO: is this safe? libgroove uses these callbacks internally
            #       but when it does I think the sink is not exposed
            instance._attach_callbacks()
        return instance, created

    def __init__(self):
        # TODO: better exception handling
        obj = lib.groove_sink_create()
        assert obj != ffi.NULL
        self._obj = ffi.gc(obj, lib.groove_sink_destroy)
        self._attach_callbacks()
        self._playlist = None

    def _attach_callbacks(self):
        self._obj.flush = lib.groove_sink_callback_flush
        self._obj.purge = lib.groove_sink_callback_purge
        self._obj.pause = lib.groove_sink_callback_pause
        self._obj.play = lib.groove_sink_callback_play

    def on_flush(self):
        """Called when the audio queue is flushed.

        For example if you seek to a different location in the song.
        """
        pass

    def on_purge(self, playlist_item):
        """Called when a playlist item is deleted.

        Take this opportunity to remove all references to the PlaylistItem.
        """
        pass

    def on_pause(self):
        """Called when a playlist is paused"""
        pass

    def on_play(self):
        """Called when a playlist is played"""
        pass

    def buffer_peek(self, block=True):
        """Returns True if a buffer is ready, False if not"""
        value = lib.groove_sink_buffer_peek(self._obj, block)
        assert value >= 0
        return value == 1

    def get_buffer(self, block=False):
        """Get the buffer on the sink

        If no buffer is ready, this raises `groove.Buffer.NotReady`
        If the end of the playlist is reached, this raises `groove.Buffer.End`
        If block is True and no buffer is ready, this may block indefinately
        """
        # TODO: add timeout, might have to be done in libgroove to be safe
        buff_obj_ptr = ffi.new('struct GrooveBuffer **')
        value = lib.groove_sink_buffer_get(self._obj, buff_obj_ptr, block)
        assert value >= 0

        if value == _constants.GROOVE_BUFFER_NO:
            raise Buffer.NotReady()
        elif value == _constants.GROOVE_BUFFER_END:
            raise Buffer.End()
        elif value == _constants.GROOVE_BUFFER_YES:
            buff = self.BufferClass._from_obj(buff_obj_ptr[0])
            buff.sink = self
            return buff

        raise Exception('Unknown value %s from groove_sink_buffer_get' % value)


@ffi.def_extern()
def groove_sink_callback_flush(sink_obj):
    sink, _ = Sink._from_obj(sink_obj)
    sink.on_flush()


@ffi.def_extern()
def groove_sink_callback_purge(sink_obj, pitem_obj):
    # TODO: Let the sink choose the PlaylistItem class
    sink, _ = Sink._from_obj(sink_obj)
    pitem, _ = PlaylistItem._from_obj(pitem_obj)
    sink.on_purge(pitem)


@ffi.def_extern()
def groove_sink_callback_pause(sink_obj):
    sink, _ = Sink._from_obj(sink_obj)
    sink.on_pause()


@ffi.def_extern()
def groove_sink_callback_flush(sink_obj):
    sink, _ = Sink._from_obj(sink_obj)
    sink.on_play()
