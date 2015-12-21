"""
Test the python API for libgroove
"""
import pytest

from groove import groove as g
from groove._groove import ffi, lib


def setup_module(module):
    g.init()
    lib.groove_set_logging(24)


def teardown_module(module):
    g.finish()


def test_version():
    assert (4, 0, 0) <= g.libgroove_version_info() < (5, 0, 0)


class TestChannelLayout():
    def test_default_layout(self):
        assert g.ChannelLayout.default(1) is g.ChannelLayout.layout_mono
        assert g.ChannelLayout.default(2) is g.ChannelLayout.layout_stereo
        assert g.ChannelLayout.default(3) is g.ChannelLayout.layout_2p1

    def test_channel_count(self):
        assert g.ChannelLayout.count(g.Channel.front_center) == 1
        assert g.ChannelLayout.count(g.ChannelLayout.layout_2p1) == 3
        assert g.ChannelLayout.count(1 | 2 | 4 | 8) == 4


class TestSampleFormat():
    def test_bytes_per_sample(self):
        assert g.SampleFormat.none.bytes_per_sample() == 0
        assert g.SampleFormat.s32.bytes_per_sample() == 4


class TestAudioFormat():
    def test_init_from_obj(self):
        obj = ffi.new(g.AudioFormat._ffitype, {
            'sample_rate': 1,
            'channel_layout': g.ChannelLayout.layout_stereo,
            'sample_fmt': g.SampleFormat.s32,
        })
        fmt = g.AudioFormat(_obj=obj)

        assert fmt.sample_rate == 1
        assert fmt.channel_layout is g.ChannelLayout.layout_stereo
        assert fmt.sample_format is g.SampleFormat.s32

    def test_init_from_args(self):
        fmt = g.AudioFormat(
            sample_rate=1,
            channel_layout=g.ChannelLayout.layout_stereo,
            sample_format=g.SampleFormat.s32,
        )

        assert fmt.sample_rate == 1
        assert fmt.channel_layout is g.ChannelLayout.layout_stereo
        assert fmt.sample_format is g.SampleFormat.s32

    def test_equals(self):
        fmt_a = g.AudioFormat(
            sample_rate=1,
            channel_layout=g.ChannelLayout.layout_stereo,
            sample_format=g.SampleFormat.s32,
        )
        fmt_b = g.AudioFormat(
            sample_rate=1,
            channel_layout=g.ChannelLayout.layout_stereo,
            sample_format=g.SampleFormat.s32,
        )
        fmt_c = g.AudioFormat(
            sample_rate=2,
            channel_layout=g.ChannelLayout.layout_stereo,
            sample_format=g.SampleFormat.s32,
        )
        fmt_d = g.AudioFormat(
            sample_rate=1,
            channel_layout=g.ChannelLayout.layout_mono,
            sample_format=g.SampleFormat.s32,
        )
        fmt_e = g.AudioFormat(
            sample_rate=1,
            channel_layout=g.ChannelLayout.layout_stereo,
            sample_format=g.SampleFormat.s16,
        )

        assert fmt_a is not fmt_b
        assert fmt_a == fmt_b

        for other in (fmt_c, fmt_d, fmt_e):
            assert fmt_a is not other
            assert (fmt_a == other) is False


class TestFile():

    def setup_method(self, method):
        self.gfile = g.File('tests/samples/stereo-440hz.mp3')
        self.gfile.open()
        pass

    def teardown_method(self, method):
        self.gfile.close()
        self.gfile = None

    def test__require_open(self):
        # An open file shouldnt raise
        self.gfile.dirty()

        gfile = g.File('')
        with pytest.raises(ValueError):
            gfile.dirty()

    def test_get_tags(self):
        expected_tags = {
            'artist': 'groove test',
            'title': '440hz test',
            'encoder': 'LAME3.99r',
        }
        assert self.gfile.get_tags() == expected_tags


    def test_set_tag(self):
        # It should update existing tags
        self.gfile.set_tag('artist', 'a')
        assert self.gfile.get_tags()['artist'] == 'a'

        # It should delete existing tags
        self.gfile.set_tag('artist', None)
        assert 'artist' not in self.gfile.get_tags()

        # It should create new tags
        self.gfile.set_tag('delicious', 'penguin')
        assert self.gfile.get_tags()['delicious'] == 'penguin'

    def test_set_tag(self):
        tagdict = {
            'artist': 'a',
            'title': None,
            'delicious': 'penguin',
        }
        expected_tags = {
            'artist': 'a',
            'delicious': 'penguin',
            'encoder': 'LAME3.99r',
        }

        self.gfile.set_tags(tagdict)
        assert self.gfile.get_tags() == expected_tags

    def test_dirty(self):
        assert self.gfile.dirty() == False
        self.gfile.set_tag('delicious', 'penguin')
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

    @pytest.mark.xfail
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
