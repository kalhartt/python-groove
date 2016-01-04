"""
Test groove.Playlist
"""
from __future__ import absolute_import, unicode_literals

import pytest

import groove as g
from groove._groove import ffi, lib


class TestPlaylist:
    def setup_class(cls):
        cls.files = [
            g.File('tests/samples/mono-180hz.mp3'),
            g.File('tests/samples/mono-261hz.mp3'),
            g.File('tests/samples/mono-523hz.mp3'),
        ]

    def setup_method(self, method):
        for gfile in self.files:
            gfile.open()

    def teardown_method(self, method):
        for gfile in self.files:
            gfile.close()

    def test_gain(self):
        playlist = g.Playlist()
        playlist.gain = 0.5
        assert playlist.gain == 0.5

    def test_index(self):
        playlist = g.Playlist()
        playlist.extend(self.files)
        assert playlist.index(self.files[1]) == 1

    def test_insert(self):
        playlist = g.Playlist()
        playlist.append(self.files[0])
        playlist.append(self.files[1])
        playlist.insert(1, self.files[2])
        assert playlist[1].file == self.files[2]

    def test_append(self):
        playlist = g.Playlist()
        playlist.append(self.files[0])
        playlist.append(self.files[1])
        assert playlist[0].file == self.files[0]
        assert playlist[1].file == self.files[1]

    def test_clear(self):
        playlist = g.Playlist()
        playlist.extend(self.files)
        playlist.clear()
        assert len(playlist) == 0

    def test_reverse(self):
        # TODO
        pass

    def test_pop(self):
        playlist = g.Playlist()
        playlist.append(self.files[0])
        with pytest.raises(NotImplementedError):
            playlist.pop()

    def test_remove(self):
        playlist = g.Playlist()
        playlist.extend(self.files)
        playlist.remove(self.files[1])
        assert len(playlist) == 2
        assert playlist[0].file == self.files[0]
        assert playlist[1].file == self.files[2]

        with pytest.raises(ValueError):
            playlist.remove(self.files[1])

    def test_iter(self):
        playlist = g.Playlist()
        playlist.extend(self.files)

        for item, gfile in zip(playlist, self.files):
            assert item.file == gfile

    def test_reversed(self):
        playlist = g.Playlist()
        playlist.extend(self.files)

        for item, gfile in zip(reversed(playlist), reversed(self.files)):
            assert item.file == gfile

    def test_len(self):
        playlist = g.Playlist()
        assert len(playlist) == 0
        playlist.extend(self.files)
        assert len(playlist) == 3
        playlist.remove(self.files[1])
        assert len(playlist) == 2

    def test_getitem(self):
        playlist = g.Playlist()
        playlist.extend(self.files)

        for n in range(-len(self.files), len(self.files)):
            assert playlist[n].file == self.files[n]

        with pytest.raises(IndexError):
            playlist[4]

        with pytest.raises(TypeError):
            playlist[0:2]

    def test_setitem(self):
        # Broken, see https://github.com/andrewrk/libgroove/issues/123
        # ATM this probably leaks
        playlist = g.Playlist()
        playlist.append(self.files[0])
        playlist.append(self.files[2])
        playlist[0] = self.files[1]
        assert len(playlist) == 2
        assert playlist[0].file == self.files[1]
        assert playlist[1].file == self.files[2]

    def test_delitem(self):
        playlist = g.Playlist()
        playlist.extend(self.files)
        del playlist[1]
        assert len(playlist) == 2
        assert playlist[0].file == self.files[0]
        assert playlist[1].file == self.files[2]

    def test_play(self):
        # TODO
        pass

    def test_pause(self):
        # TODO
        pass

    def test_seek(self):
        # TODO
        pass
