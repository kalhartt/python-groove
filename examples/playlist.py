#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""playlist
Play a set of files

Usage:
    playlist [-v...] [--volume VOL] [--exact] [--dummy] FILE...

Options:
    --volume VOL       Volume adjustment for the set of files [default: 1.0]
    --exact            Use media's exact audio format for playback
    --dummy            Use dummy playback device
    -v --verbose       Set logging level, repeat to increase verbosity
"""
from __future__ import print_function, unicode_literals

import logging
import sys

from docopt import docopt
import groove


_log = logging.getLogger(__name__)


def main(infiles, volume=1.0, exact=False, dummy=False):
    _log.debug('Creating a player and playlist')
    player = groove.Player()
    playlist = groove.Playlist()

    _log.debug('Opening files and adding to playlist')
    for infile in infiles:
        gfile = groove.File(infile)
        gfile.open()
        playlist.append(gfile)

    _log.debug('Setting options for playlist and player')
    playlist.gain = volume
    player.use_exact_audio_format = exact
    player.device = groove.Player.dummy_device if dummy else groove.Player.default_device

    _log.debug('Attaching playlist to player')
    player.playlist = playlist

    _log.debug('Entering player event loop')
    while True:
        _log.debug('Getting event')
        # Can't interrupt this
        # in reality blocking calls should be done in a separate thread
        event = player.event_get(True)
        _log.debug('Got event %d', event)

        if event == None:
            break

        elif event == groove.PlayerEvent.buffer_underrun:
            _log.error('Buffer underrun')
            continue

        elif event == groove.PlayerEvent.device_reopened:
            _log.error('Device re-opened')
            continue

        elif event == groove.PlayerEvent.now_playing:
            pitem, seconds = player.position()

            if pitem is None:
                _log.debug('Reached end of playlist')
                break

            # Print item info
            _log.debug('Playing new file')
            tags = pitem.file.get_tags()
            if 'artist' in tags and 'title' in tags:
                print('Now playing: {0} - {1}'.format(tags['artist'], tags['title']))
            else:
                print('Now playing: {0}'.format(pitem.file.filename))

    _log.debug('Detaching playlist from player')
    player.playlist = None

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
        args['FILE'],
        float(args['--volume']),
        args['--exact'],
        args['--dummy']
    ))
