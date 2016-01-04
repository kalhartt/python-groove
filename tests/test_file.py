"""
Test groove.File
"""
from __future__ import absolute_import, unicode_literals

import pytest

import groove as g
from groove._groove import ffi, lib


class TestFile():
    def setup_method(self, method):
        self.gfile = g.File('tests/samples/stereo-440hz.mp3')
        self.gfile.open()

    def teardown_method(self, method):
        self.gfile.close()
        self.gfile = None

    def test_from_obj(self):
        gfile, created = g.File._from_obj(self.gfile._obj)

        assert gfile.filename == 'tests/samples/stereo-440hz.mp3'
        assert created == False
        assert self.gfile is gfile

        gfile_obj = lib.groove_file_open(b'tests/samples/mono-180hz.mp3')
        gfile, created = g.File._from_obj(gfile_obj)

        assert gfile.filename == 'tests/samples/mono-180hz.mp3'
        assert created == True

    def test__require_open(self):
        # An open file shouldnt raise
        self.gfile.dirty()

        gfile = g.File('')
        with pytest.raises(ValueError):
            gfile.dirty()

    def test_get_tags(self):
        expected_tags = {
            b'artist': b'groove test',
            b'title': b'440hz test',
            b'encoder': b'LAME3.99r',
        }
        assert self.gfile.get_tags() == expected_tags


    def test_set_tag(self):
        # It should update existing tags
        self.gfile.set_tag(b'artist', b'a')
        assert self.gfile.get_tags()[b'artist'] == b'a'

        # It should delete existing tags
        self.gfile.set_tag(b'artist', None)
        assert b'artist' not in self.gfile.get_tags()

        # It should create new tags
        self.gfile.set_tag(b'delicious', b'penguin')
        assert self.gfile.get_tags()[b'delicious'] == b'penguin'

    def test_set_tag(self):
        tagdict = {
            b'artist': b'a',
            b'title': None,
            b'delicious': b'penguin',
        }
        expected_tags = {
            b'artist': b'a',
            b'delicious': b'penguin',
            b'encoder': b'LAME3.99r',
        }

        self.gfile.set_tags(tagdict)
        assert self.gfile.get_tags() == expected_tags

    def test_dirty(self):
        assert self.gfile.dirty() == False
        self.gfile.set_tag(b'delicious', b'penguin')
        assert self.gfile.dirty() == True

    def test_short_names(self):
        assert self.gfile.short_names() == ['mp3']

    def test_duration(self):
        # Sample track is roughly 5 seconds
        assert 4.9 <= self.gfile.duration() <= 5.1

    def test_audio_format(self):
        audio_format = self.gfile.audio_format()
        assert audio_format.sample_rate == 44100
        assert audio_format.channel_layout is g.ChannelLayout.layout_stereo
        assert audio_format.sample_format is g.SampleFormat.s16p

    def test_context_manager(self):
        # undo the automatic setup first
        self.gfile.close()

        assert self.gfile._obj is None
        with self.gfile:
            assert self.gfile._obj is not None
        assert self.gfile._obj is None
