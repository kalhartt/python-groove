from __future__ import absolute_import, unicode_literals

from collections import namedtuple

from groove import utils
from groove._groove import ffi, lib
from groove.groove import GrooveClass

__all__ = [
    'LoudnessDetector',
    'LoudnessDetectorInfo',
]


LoudnessDetectorInfo = namedtuple('LoudnessDetectorInfo', [
    'loudness',
    'peak',
    'duration',
    'playlist_item',
])


class LoudnessDetector(GrooveClass):
    """pass"""
    _ffitype = 'struct GrooveLoudnessDetector *'

    info_queue_size = utils.property_convert('info_queue_size', int,
        doc="""Maximum number of items to store in this LoudnessDetector's
        queue

        This defaults to MAX_INT, meaning that the loudness detector will cause
        the decoder to decode the entire playlist. If you want to instead, for
        example, obtain loudness info at the same time as playback, you might
        set this value to 1.
        """)

    sink_buffer_size = utils.property_convert('sink_buffer_size', int,
        doc="""How big the sink buffer should be, in sample frames

        LoudnessDetector defaults this to 8192
        """)

    disable_album = utils.property_convert('disable_album', bool,
        doc="""Set True to only compute track loudness

        This is faster and requires less memory than computing both.
        LoudnessDetector defaults this to False
        """)

    @property
    def playlist(self):
        """Playlist to generate loudness info for"""
        return self._playlist

    @playlist.setter
    def playlist(self, value):
        if self._playlist:
            assert lib.groove_loudness_detector_detach(self._obj) == 0
            self._playlist = None

        if value is not None:
            assert lib.groove_loudness_detector_attach(self._obj, value._obj) == 0
            self._playlist = value

    def __init__(self):
        # TODO: error handling
        obj = lib.groove_loudness_detector_create()
        assert obj != ffi.NULL
        self._obj = ffi.gc(obj, lib.groove_loudness_detector_destroy)
        self._playlist = None

    def __del__(self):
        # Make sure playlist gets detached before we loose the obj
        if self.playlist is not None:
            self.playlist = None

    def __iter__(self):
        info_obj = ffi.new('struct GrooveLoudnessDetectorInfo *');
        pitem = True

        while pitem:
            status = lib.groove_loudness_detector_info_get(self._obj, info_obj, True)
            assert status >= 0
            if status != 1:
                break

            loudness = float(info_obj.loudness)
            peak = float(info_obj.peak)
            duration = float(info_obj.duration)

            if info_obj.item == ffi.NULL:
                pitem = None
            else:
                pitem = self.playlist._pitem(info_obj.item)

            yield LoudnessDetectorInfo(loudness, peak, duration, pitem)

    def info_peek(self, block=False):
        """Check if info is ready"""
        result = lib.groove_loudness_detector_info_peek(self._obj, block)
        assert result >= 0
        return bool(result)

    def position(self):
        """Get the current position of the printer head

        Returns:
            A tuple of (playlist_item, seconds). If the playlist is empty
            playlist_item will be None and seconds will be -1.0
        """
        pitem_obj_ptr = ffi.new('struct GroovePlaylistItem **')
        seconds = ffi.new('double *')
        lib.groove_loudness_detector_position(self._obj, pitem_obj_ptr, seconds)
        if pitem_obj_ptr[0] == ffi.NULL:
            pitem = None
        else:
            pitem = self.playlist._pitem(pitem_obj_ptr[0])
        return pitem, float(seconds[0])
