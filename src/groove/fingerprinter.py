from __future__ import absolute_import, unicode_literals

from groove import utils
from groove._groove import ffi, lib
from groove.groove import GrooveClass

__all__ = ['Fingerprinter']


class Fingerprinter(GrooveClass):
    """Use this to find out the unique id of an audio track"""
    _ffitype = 'struct GrooveFingerprinter *'

    info_queue_size = utils.property_convert('info_queue_size', int,
        doc="""Maximum number of items to store in this Fingerprinter's queue

        This defaults to MAX_INT, meaning that fingerprinter will cause the
        decoder to decode the entire playlist. If you want instead, for
        example, obtain fingerprints at the same time as playback, you might
        set this value to 1.
        """)

    sink_buffer_size = utils.property_convert('sink_buffer_size', int,
        doc="""How big the sink buffer should be, in sample frames

        This defaults to 8192.
        """)

    @classmethod
    def encode(cls, fp):
        """Compress and base64-encode a raw fingerprint"""
        # TODO: error handling
        efp_obj_ptr = ffi.new('char **')
        fp_obj = ffi.new('int32_t[]', fp)
        assert lib.groove_fingerprinter_encode(fp_obj, len(fp), efp_obj_ptr) == 0

        # copy the result to python and free the c obj
        result = ffi.string(efp_obj_ptr[0])
        lib.groove_fingerprinter_dealloc(efp_obj_ptr[0])

        return result

    @classmethod
    def decode(cls, encoded_fp):
        """Uncompress and base64-decode a raw fingerprint"""
        efp_obj = ffi.new('char[]', encoded_fp)
        fp_obj_ptr = ffi.new('int32_t **')
        size_obj_ptr = ffi.new('int *')
        assert lib.groove_fingerprinter_decode(efp_obj, fp_obj_ptr, size_obj_ptr) == 0

        # copy the result to python and free the c obj
        fp_obj = fp_obj_ptr[0]
        result = [int(fp_obj[n]) for n in range(size_obj_ptr[0])]
        lib.groove_fingerprinter_dealloc(fp_obj)

        return result

    @property
    def playlist(self):
        """Playlist to generate fingerprints for"""
        return self._playlist

    @playlist.setter
    def playlist(self, value):
        if self._playlist:
            assert lib.groove_fingerprinter_detach(self._obj) == 0
            self._playlist = None

        if value is not None:
            assert lib.groove_fingerprinter_attach(self._obj, value._obj) == 0
            self._playlist = value

    def __init__(self, base64_encode=True):
        # TODO: error handling
        obj = lib.groove_fingerprinter_create()
        assert obj != ffi.NULL
        self._obj = ffi.gc(obj, lib.groove_fingerprinter_destroy)
        self._playlist = None
        self.base64_encode = base64_encode

    def __del__(self):
        # Make sure playlist gets detached before we loose the obj
        if self.playlist is not None:
            self.playlist = None

    def __iter__(self):
        info_obj = ffi.new('struct GrooveFingerprinterInfo *');
        while True:
            status = lib.groove_fingerprinter_info_get(self._obj, info_obj, True)
            assert status >= 0
            if status != 1 or info_obj.item == ffi.NULL:
                break

            fp_obj = info_obj.fingerprint
            fp_size_obj = info_obj.fingerprint_size

            if self.base64_encode:
                efp_obj_ptr = ffi.new('char **')
                assert lib.groove_fingerprinter_encode(fp_obj, fp_size_obj, efp_obj_ptr) == 0
                fp = ffi.string(efp_obj_ptr[0])
                lib.groove_fingerprinter_dealloc(efp_obj_ptr[0])
            else:
                fp = [int(fp_obj[n]) for n in range(fp_size_obj)]

            duration = float(info_obj.duration)
            pitem = self.playlist._pitem(info_obj.item)
            lib.groove_fingerprinter_free_info(info_obj)
            yield (fp, duration, pitem)

    def info_peek(self, block=False):
        """Check if info is ready"""
        result = lib.groove_fingerprinter_info_peek(self._obj, block)
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
        lib.groove_fingerprinter_position(self._obj, pitem_obj_ptr, seconds)
        if pitem_obj_ptr[0] == ffi.NULL:
            pitem = None
        else:
            pitem = self.playlist._pitem(pitem_obj_ptr[0])
        return pitem, float(seconds[0])
