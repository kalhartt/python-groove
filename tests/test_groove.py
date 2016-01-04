"""
Test the python API for libgroove
"""
from __future__ import absolute_import, unicode_literals

import pytest

import groove as g


def test_version():
    assert '4.0.0' <= g.libgroove_version() < '5.0.0'


def test_version_info():
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
