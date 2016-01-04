"""
Test groove.AudioFormat
"""
from __future__ import absolute_import, unicode_literals

import pytest

import groove as g
from groove._groove import ffi, lib


class TestAudioFormat():
    def test_from_obj(self):
        obj = ffi.new(g.AudioFormat._ffitype, {
            'sample_rate': 1,
            'channel_layout': g.ChannelLayout.layout_stereo,
            'sample_fmt': g.SampleFormat.s32,
        })
        fmt, fmt_created = g.AudioFormat._from_obj(obj)
        fmt2, fmt2_created = g.AudioFormat._from_obj(obj)

        assert fmt.sample_rate == 1
        assert fmt.channel_layout is g.ChannelLayout.layout_stereo
        assert fmt.sample_format is g.SampleFormat.s32
        assert fmt is fmt2
        assert fmt_created == True
        assert fmt2_created == False

    def test_init_from_args(self):
        fmt = g.AudioFormat(
            sample_rate=1,
            channel_layout=g.ChannelLayout.layout_stereo,
            sample_format=g.SampleFormat.s32,
        )

        assert fmt.sample_rate == 1
        assert fmt.channel_layout is g.ChannelLayout.layout_stereo
        assert fmt.sample_format is g.SampleFormat.s32

    def test_sample_rate(self):
        fmt = g.AudioFormat()
        fmt.sample_rate = 2
        assert fmt.sample_rate == 2

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
        assert fmt_a != 5

        for other in (fmt_c, fmt_d, fmt_e):
            assert fmt_a is not other
            assert (fmt_a == other) is False
