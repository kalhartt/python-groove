from __future__ import absolute_import, unicode_literals

from groove import _constants
from groove._groove import ffi, lib
from groove.groove import GrooveClass


__all__ = ['Buffer']


class Buffer(GrooveClass):
    """Groove Buffer

    Attributes:
        playlist (Playlist): The playlist of the buffers current PlaylistItem
                             if it exists, else `None`
    """
    # NOTE: Buffers must be constructed via Buffer._from_obj
    _ffitype = 'struct GrooveBuffer *'

    class NotReady(Exception): pass
    class End(Exception): pass

    @property
    def data(self):
        """Actual buffer data

        for interleaved audio, data[0] is the buffer.
        for planar audio, each channel has a separate data pointer.
        for encoded audio, data[0] is the encoded buffer.
        """
        return ffi.buffer(self._obj.data[0], self._obj.size)[:]

    @property
    def audio_format(self):
        audio_format, _ = AudioFormat._from_obj(self._obj.format)
        return audio_format

    @property
    def frame_count(self):
        """Number of audio frames described by the buffer

        For encoded audio, this is unknown and set to 0
        """
        return self._obj.frame_count

    @property
    def playlist_item(self):
        """Playlist item being processed

        When encoding, if item is None, this is a format header or trailer.
        otherwise, this is encoded audio for the item specified.
        when decoding, item is never None
        """
        item_obj = self._obj.item
        if item_obj == ffi.NULL:
            return None

        # TODO: figure out what playlist this comes from and use
        #       playlist.ItemClass
        instance, _ = PlaylistItem._from_obj(item_obj)
        instance.playlist = self.playlist
        return instance

    @property
    def position(self):
        """Buffer offset in seconds"""
        return self._obj.pos

    @property
    def size(self):
        """Total bytes in the buffer"""
        return self._obj.size

    @property
    def time_stamp(self):
        """Presentation time stamp of the buffer"""
        return self._obj.pts

    def __init__(self):
        raise NotImplementedError('Buffers can only be created by a Sink')

    def ref(self):
        """Increment the reference count"""
        lib.groove_buffer_ref(self._obj)

    def unref(self):
        """Decrement reference count

        This can be used to advance the buffer, see the examples
        """
        lib.groove_buffer_unref(self._obj)
