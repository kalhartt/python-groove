"""
Test the ffi wrapper for libgroove
"""
from groove._groove import ffi, lib


def setup_module(module):
    lib.groove_init()
    lib.groove_set_logging(32)


def teardown_module(module):
    lib.groove_finish()


def test_channel_layouts():
    # TODO: replace these numbers with values from groove.constants
    assert lib.groove_channel_layout_count(1) == 1
    assert lib.groove_channel_layout_count(3) == 2
    assert lib.groove_channel_layout_count(7) == 3
    assert lib.groove_channel_layout_default(1) == 4
    assert lib.groove_channel_layout_default(2) == 3
    assert lib.groove_channel_layout_default(3) == 11
