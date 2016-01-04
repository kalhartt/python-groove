from __future__ import absolute_import, unicode_literals

import unittest

import groove as g
from groove._groove import ffi, lib


class TestBuffer(unittest.TestCase):
    def run(self, result=None):
        with \
            g.File('tests/samples/mono-180hz.mp3') as gf0, \
            g.File('tests/samples/mono-261hz.mp3') as gf1, \
            g.File('tests/samples/mono-523hz.mp3') as gf2:
            self.files = [gf0, gf1, gf2]
            self.playlist = g.Playlist()
            self.playlist.extend(self.files)
            self.sink = g.Sink()
            self.sink.playlist = self.playlist
            print('RUN METHOD')
            return super(TestBuffer, self).run(result)

    def test_init(self):
        # It should raise when trying to initialize
        with self.assertRaises(NotImplementedError):
            buff = g.Buffer()

    def test_get_buffer(self):
        import pdb; pdb.set_trace()
        self.playlist.seek(self.playlist[0], 2)
        buff = self.sink.get_buffer()
