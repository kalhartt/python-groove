#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""replaygain
Calculate replaygain values for a set of files

Usage:
    replaygain [-v...] FILE...

Options:
    -v --verbose       Set logging level, repeat to increase verbosity
"""
from __future__ import print_function, unicode_literals

import logging
import sys

from docopt import docopt
import groove


_log = logging.getLogger(__name__)


def loudness_to_replaygain(loudness):
    """Convert loudness to replaygain value, clamped to (-51.0, 51.0)"""
    rg = -18.0 - loudness
    rg = min(max(rg, -51.0), 51.0)
    return rg

def main(infiles):
    _log.debug('Creating a playlist and loudness detector')
    loudness_detector = groove.LoudnessDetector()
    playlist = groove.Playlist()

    _log.debug('Opening files and adding to playlist')
    for infile in infiles:
        gfile = groove.File(infile)
        gfile.open()
        playlist.append(gfile)

    _log.debug('Attaching playlist to detector')
    loudness_detector.playlist = playlist

    _log.debug('Processing playlist')
    for loudness, peak, duration, pitem in loudness_detector:
        if pitem is None:
            print('\nAll files complete.')
        else:
            print('\nfile complete: {0}\n'.format(pitem.file.filename))

        print('suggested gain: {0:.2f}, sample peak: {1}, duration: {2}'
            .format(loudness_to_replaygain(loudness), peak, duration))

    _log.debug('Detaching playlist')
    loudness_detector.playlist = None

    _log.debug('Closing files and clearing playlist')
    while len(playlist) > 0:
        playlist[0].file.close()
        del playlist[0]

    return 0


if __name__ == '__main__':
    args = docopt(__doc__)

    loglvl = {
        0: logging.WARNING,
        1: logging.INFO,
    }.get(args['--verbose'], logging.DEBUG)
    logging.basicConfig(level=loglvl)

    groove.init()
    sys.exit(main(
        args['FILE']
    ))
