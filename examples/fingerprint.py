#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""fingerprint
Calculate the fingerprint for a set of audio files

Usage:
    fingerprint [-v...] [--raw] FILE...

Options:
    --raw              Print the raw fingerprint, defaults to b64-encoded
    -v --verbose       Set logging level, repeat to increase verbosity
"""
from __future__ import print_function, unicode_literals

import logging
import sys

from docopt import docopt
import groove


_log = logging.getLogger(__name__)


def main(raw, *infiles):
    # Create a playlist
    playlist = groove.Playlist()

    # open and add all input files to playlist
    for infile in infiles:
        gfile = groove.File(infile)
        gfile.open()
        playlist.append(gfile)

    # Create the fingerprinter and attach the playlist
    printer = groove.Fingerprinter(base64_encode=not raw)
    printer.playlist = playlist

    # Iterate over the fingerprinter
    for fp, duration, pitem in printer:
        print()
        print("duration {}: {}".format(duration, pitem.file.filename))
        print(fp)

    # Detach the playlist
    printer.playlist = None

    # Close and remove files from the playlist
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
        args['--raw'],
        *args['FILE']
    ))
