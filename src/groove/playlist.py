from __future__ import absolute_import, unicode_literals

try:
    from collections import MutableSequence
except ImportError:
    from collections.abc import MutableSequence

from groove import _constants
from groove import utils
from groove._groove import ffi, lib
from groove.file import File
from groove.groove import GrooveClass


__all__ = ['Playlist', 'PlaylistItem']


class PlaylistItem(GrooveClass):
    """Item in a playlist

    Playlist items are managed by libgroove, the underlying object will be
    freed when the playlist is destroyed.

    Attributes:
        playlist (Playlist): Playlist this item belongs to
    """
    # NOTE: PlaylistItems must be constructed via PlaylistItem._from_obj()
    #       Remember to set playlist_item.playlist after
    _ffitype = 'struct GroovePlaylistItem *'

    @property
    def file(self):
        """The GrooveFile associated with the item"""
        fileobj = self._obj.file
        if fileobj == ffi.NULL:
            return None

        instance, _ = File._from_obj(fileobj)
        return instance

    @property
    def gain(self):
        """Volume adjustment in float format, used for loudness adjustment

        To convert between dB and float use:
            float = exp(log(10) * 0.05 * dB)
        """
        return self._obj.gain

    @gain.setter
    def gain(self, value):
        lib.groove_playlist_set_item_gain(self.playlist._obj, self._obj, value)

    @property
    def peak(self):
        """Sample peak of the item

        The sample peak of this playlist item is assumed to be 1.0 in float
        format. If you know for certain that the peak is less than 1.0, you
        may set this value which may allow the volume adjustment to use a
        pure amplifier rather than a compressor. This results in slightly
        better audio quality.
        """
        return self._obj.gain

    @peak.setter
    def peak(self, value):
        lib.groove_playlist_set_item_peak(self.playlist._obj, self._obj, value)

    @property
    def prev_item(self):
        """Previous item in the playlist or None"""
        prev_item = self._obj.prev
        if prev_item == ffi.NULL:
            return None

        instance, _ = type(self)._from_obj(prev_item)
        instance.playlist = self.playlist
        return instance

    @property
    def next_item(self):
        """Next item in the playlist or None"""
        next_item = self._obj.next
        if next_item == ffi.NULL:
            return None

        instance, _ = type(self)._from_obj(next_item)
        instance.playlist = self.playlist
        return instance

    def __init__(self):
        # TODO: This feels incredibly unpythonic...
        raise NotImplementedError('PlaylistItems can only be created by the playlist')

    def __eq__(self, rhs):
        return self._obj == rhs._obj


class Playlist(GrooveClass, MutableSequence):
    """Groove Playlist - A mutable sequence of playlist items

    Insertions accept open Groove Files, acceses return PlaylistItems
    The Playlist is responsible for and does free PlaylistItems
    The Playlist is not responsible for open/close/free Groove Files

    Since its a linked list, each list operation is O(n)

    Class Attributes:
        ItemClass (type): Class to use for playlist items
        any_sink_full (int): Flag for `set_fill_mode`. With this behavior, the
                             playlist will stop decoding audio when any
                             attached sink is full, and then resume decoding
                             audio when every sink is not full.
        every_sink_full (int): Flag for `set_fill_mode`. This is the default
                               behavior. The playlist will decode audio if any
                               sinks are not full. If any sinks do not drain
                               fast enough, the data will buffer up in the
                               playlist.
    """
    _ffitype = 'struct GroovePlaylist *'

    ItemClass = PlaylistItem
    any_sink_full = _constants.GROOVE_ANY_SINK_FULL
    every_sink_full = _constants.GROOVE_EVERY_SINK_FULL

    @property
    def gain(self):
        """Volume adjustment in float format, used for loudness adjustment

        To convert between dB and float use:
            float = exp(log(10) * 0.05 * dB)
        """
        return self._obj.gain

    @gain.setter
    def gain(self, value):
        lib.groove_playlist_set_gain(self._obj, value)

    def __init__(self):
        obj = lib.groove_playlist_create()
        # TODO: raise proper exception
        # TODO: read error message from AV_LOG
        assert obj != ffi.NULL
        self._obj = ffi.gc(obj, lib.groove_playlist_destroy)

    def __iter__(self):
        item_obj = self._obj.head
        while item_obj != ffi.NULL:
            yield self._pitem(item_obj)
            item_obj = item_obj.next

    def __reversed__(self):
        item_obj = self._obj.tail
        while item_obj != ffi.NULL:
            yield self._pitem(item_obj)
            item_obj = item_obj.prev

    def __len__(self):
        return len([x for x in self])

    def __getitem__(self, index):
        # TODO: slicing
        if isinstance(index, slice):
            raise TypeError("Slicing a Playlist is not supported")

        if index < 0:
            iterator = reversed(self)
            index = -index - 1
        else:
            iterator = self

        for n, item in enumerate(iterator):
            if n == index:
                return self._pitem(item._obj)
        raise IndexError

    def __setitem__(self, index, value):
        remove_obj = self[index]._obj
        lib.groove_playlist_insert(self._obj, value._obj, 1.0, 1.0, remove_obj)
        lib.groove_playlist_remove(self._obj, remove_obj)

    def __delitem__(self, index):
        remove_obj = self[index]._obj
        lib.groove_playlist_remove(self._obj, remove_obj)

    def _pitem(self, obj):
        """Shortcut to get the PlaylistItem for a cdata object"""
        pitem, _ = self.ItemClass._from_obj(obj)
        pitem.playlist = self
        return pitem

    def index(self, gfile, start=0, stop=None):
        # TODO: Negative indexing
        # TODO: Slicing
        if start != 0 or stop is not None:
            raise TypeError("Slicing a Playlist is not supported (yet)")

        for count, item in enumerate(self):
            if gfile == item.file:
                return count

        raise ValueError("File is not in Playlist")

    def insert(self, index, gfile, gain=1.0, peak=1.0):
        # TODO: handle index error like list does
        next_obj = self[index]._obj
        lib.groove_playlist_insert(self._obj, gfile._obj, gain, peak, next_obj)

    def append(self, gfile, gain=1.0, peak=1.0):
        # TODO: better error handling
        new_item = lib.groove_playlist_insert(self._obj, gfile._obj, gain, peak, ffi.NULL)
        assert new_item != ffi.NULL, "Out of Memory"

    def clear(self):
        lib.groove_playlist_clear(self._obj)

    def reverse(self):
        # TODO
        raise NotImplementedError("Unsupported at this time")

    def pop(self, index=-1):
        raise NotImplementedError("Can't pop, removing from the list deletes the item")

    def remove(self, gfile):
        # TODO: handle groove.File and groove.PlaylistItem?
        for item in self:
            if item.file == gfile:
                lib.groove_playlist_remove(self._obj, item._obj)
                break
        else:
            raise ValueError("File is not in Playlist")

    def set_fill_mode(self, value):
        """Set the fill mode for the playlist

        See the attributes `every_sink_full` and `any_sink_full` for details.
        """
        # TODO: is there no way to get the fill mode?
        lib.groove_playlist_set_fill_mode(self._obj, value)

    def play(self):
        lib.groove_playlist_play(self._obj)

    def pause(self):
        lib.groove_playlist_pause(self._obj)

    def seek(self, playlist_item, seconds):
        """Seek to the given location in the playlist"""
        lib.groove_playlist_seek(self._obj, playlist_item._obj, seconds)

    def decode_position(self):
        """Get the current position of the decode head

        Returns:
            A tuple of (playlist_item, seconds). If the playlist is empty
            playlist_item will be None and seconds will be -1.0
        """
        pitem_obj_ptr = ffi.new('struct GroovePlaylistItem **')
        seconds = ffi.new('double *')
        lib.groove_playlist_position(self._obj, pitem_obj_ptr, seconds)
        if pitem_obj_ptr[0] == ffi.NULL:
            pitem = None
        else:
            pitem = self._pitem(pitem_obj_ptr[0])
        return pitem, float(seconds[0])

    def is_playing(self):
        return lib.groove_playlist_playing(self._obj) == 1
