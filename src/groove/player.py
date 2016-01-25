from __future__ import absolute_import, unicode_literals

from collections import namedtuple
from enum import IntEnum

from groove import _constants
from groove import utils
from groove._groove import ffi, lib
from groove.audio_format import AudioFormat
from groove.groove import GrooveClass

__all__ = [
    'Device',
    'Player',
    'PlayerEvent'
]


Device = namedtuple('Device', [
    'index',
    'name',
])


@utils.unique_enum
class PlayerEvent(IntEnum):
    """Enumeration for Player events"""
    now_playing = _constants.GROOVE_EVENT_NOWPLAYING
    buffer_underrun = _constants.GROOVE_EVENT_BUFFERUNDERRUN
    device_reopened = _constants.GROOVE_EVENT_DEVICEREOPENED


class Player(GrooveClass):
    _ffitype = 'struct GroovePlayer *'
    dummy_device = Device(_constants.GROOVE_PLAYER_DUMMY_DEVICE, 'dummy')
    default_device = Device(_constants.GROOVE_PLAYER_DEFAULT_DEVICE, 'default')

    @classmethod
    def list_devices(cls):
        """Get the list of available devices

        This may trigger a complete redetect of available hardware
        """
        devices = [
            Player.dummy_device,
            Player.default_device,
        ]

        device_count = lib.groove_device_count()
        for n in range(device_count):
            name = lib.groove_device_name(n)
            if name == ffi.NULL:
                continue
            name = ffi.string(name).decode('utf-8')
            devices.append(Device(n, name))

        return devices

    device_buffer_size = utils.property_convert('device_buffer_size', int,
        doc="""How big the device buffer should be, in sample frames

        Must be a power of 2, defaults to 1024
        """)

    sink_buffer_size = utils.property_convert('sink_buffer_size', int,
        doc="""How big the sink buffer should be, in sample frames

        Defaults to 8192
        """)

    use_exact_audio_format = utils.property_convert('use_exact_audio_format', bool,
        doc="""Force the device to play with the format of the media

        If true, `target_audio_format` and `actual_audio_format` are ignored
        and no resampling, channel layout remapping, or sample format
        conversion will occur. The audio device will be reopened with exact
        parameters whenever necessary.
        """)

    @property
    def device(self):
        """Device for playback, defaults to Player.dummy_device"""
        return self._device

    @device.setter
    def device(self, value):
        self._obj.device_index = value.index
        self._device = value

    @property
    def target_audio_format(self):
        """The desired audio format to open the device with

        Defaults to 44100Hz, signed 16-bit int, stereo
        These are preferences; if a setting cannot be used, a substitute will
        be used instead. `actual_audio_format` is set to the actual values.
        """
        fmt, _ = AudioFormat._from_obj(self._obj.target_audio_format)
        return fmt

    @property
    def actual_audio_format(self):
        """Set to the actual audio format you get when you open the device"""
        fmt, _ = AudioFormat._from_obj(self._obj.actual_audio_format)
        return fmt

    @property
    def gain(self):
        """The volume adjustment to make to this player

        It is recommended to leave this at 1.0 and instead adjust the gain of
        the underlying playlist.
        """
        return self._obj.gain

    @gain.setter
    def gain(self, value):
        assert lib.groove_player_set_gain(self._obj, value) == 0

    @property
    def playlist(self):
        """Playlist to play"""
        return self._playlist

    @playlist.setter
    def playlist(self, value):
        if self._playlist:
            assert lib.groove_player_detach(self._obj) == 0
            self._playlist = None

        if value is not None:
            assert lib.groove_player_attach(self._obj, value._obj) == 0
            self._playlist = value

    def __init__(self):
        # TODO: error handling
        obj = lib.groove_player_create()
        assert obj != ffi.NULL
        self._obj = ffi.gc(obj, lib.groove_player_destroy)
        self._playlist = None
        self.device = Player.dummy_device

    def __del__(self):
        # Make sure playlist gets detached before we loose the obj
        if self.playlist is not None:
            self.playlist = None

    def event_get(self, block=False):
        """Get player event"""
        event_obj = ffi.new('union GroovePlayerEvent *')
        result = lib.groove_player_event_get(self._obj, event_obj, block)
        assert result >= 0

        if result == 0:
            return None

        return PlayerEvent.__values__[event_obj.type]

    def event_peek(self, block=False):
        """Check if event is ready"""
        result = lib.groove_player_event_peek(self._obj, block)
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
        lib.groove_player_position(self._obj, pitem_obj_ptr, seconds)
        if pitem_obj_ptr[0] == ffi.NULL:
            pitem = None
        else:
            pitem = self.playlist._pitem(pitem_obj_ptr[0])
        return pitem, float(seconds[0])
