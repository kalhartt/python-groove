from __future__ import absolute_import, unicode_literals

from collections import OrderedDict

from decorator import decorator

import groove._constants as _constants
from groove.audio_format import AudioFormat
from groove.groove import GrooveClass
from groove._groove import ffi, lib


__all__ = ['File']


@decorator
def _require_open(method, *args, **kwargs):
    if args[0]._obj is None:
        raise ValueError('File is not open')
    return method(*args, **kwargs)


class File(GrooveClass):
    """Groove File

    Args:
        filename (str)  Name of the file to open
    """
    _ffitype = 'struct GrooveFile *'
    tag_match_case = _constants.GROOVE_TAG_MATCH_CASE
    tag_dont_overwrite = _constants.GROOVE_TAG_MATCH_CASE
    tag_append = _constants.GROOVE_TAG_MATCH_CASE

    @property
    def filename(self):
        return self._filename

    @classmethod
    def _from_obj(cls, obj):
        instance, created = super(File, cls)._from_obj(obj)
        if created:
            instance._filename = ffi.string(instance._obj.filename).decode()
        return instance, created

    def __init__(self, filename):
        self._obj = None
        self._filename = filename

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def __eq__(self, rhs):
        if not isinstance(rhs, File):
            return False
        return self.filename == rhs.filename

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
        return bool(self._obj.dirty)

    @_require_open
    def get_tags(self, flags=0):
        """Get the tags for an open file

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
            gtag = lib.groove_file_metadata_get(self._obj, b'', gtag, flags)
            if gtag == ffi.NULL:
                break

            key = ffi.string(lib.groove_tag_key(gtag))
            value = ffi.string(lib.groove_tag_value(gtag))
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

        If `value` is `None`, the tag will be deleted. `key` and `value` must
        be type `bytes`.
        """
        if value is None:
            value = ffi.NULL

        status = lib.groove_file_metadata_set(self._obj, key, value, flags)
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
