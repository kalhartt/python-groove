#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""transcode
Transcode one or more files into one output file

Usage:
    transcode [--bitrate=RATE] [--format=NAME] [--codec=NAME] [--mime=TYPE]
              FILE... --output=OUTFILE

Options:
    --bitrate RATE          Bitrate to sample at [default: 320]
    --format NAME
    --codec NAME
    --mime TYPE
"""
from __future__ import print_function, unicode_literals

import logging
import sys

from docopt import docopt
import groove


logging.basicConfig()
_log = logging.getLogger(__name__)


def main(bitrate, fmt, codec, mime, outname, *infilenames):
    # Create a playlist and encoder
    playlist = groove.Playlist()
    encoder = groove.Encoder()
    encoder.bitrate = bitrate * 1000
    encoder.format_short_name = fmt
    encoder.codec_short_name = codec
    encoder.mime_type = mime
    encoder.filename = outname

    # Open all the files and add them to the playlist
    for fname in infilenames:
        gfile = groove.File(fname)
        gfile.open()
        playlist.append(gfile, 1.0, 1.0)

    # If we are only converting one file, copy the audio format and metadata
    if len(playlist) == 1:
        pitem = playlist[0]

        infmt = pitem.file.audio_format()
        outfmt = encoder.target_audio_format
        outfmt.clone(infmt)

        tags = pitem.file.get_tags()
        encoder.set_tags(tags)

    # attach the playlist to the encoder
    encoder.playlist = playlist

    # Open the ouput file and write the results
    with open(outname, 'wb') as ofile:
        while True:
            try:
                buff = encoder.get_buffer(True)
            except groove.Buffer.End:
                break
            ofile.write(buff.data)

            # unref the buffer to advance
            buff.unref()

    # Detach the playlist
    encoder.playlist = None

    # Close and remove files from the playlist
    while len(playlist) > 0:
        playlist[0].file.close()
        del playlist[0]

    return 0


if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        args['--bitrate'] = int(args['--bitrate'])
    except ValueError:
        _log.error('Could not parse bitrate \"%s\" as an integer', args['--bitrate'])
        sys.exit(1)

    groove.init()
    sys.exit(main(
        args['--bitrate'],
        args['--format'],
        args['--codec'],
        args['--mime'],
        args['--output'],
        *args['FILE']
    ))
