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

import groove._constants as c
from docopt import docopt
from groove._groove import ffi, lib


logging.basicConfig()
_log = logging.getLogger(__name__)


def main(bitrate, fmt, codec, mime, outname, *infilenames):
    fmtcstr = ffi.new('char[]', fmt.encode())
    codeccstr = ffi.new('char[]', codec.encode())
    mimecstr = ffi.new('char[]', mime.encode())
    outcstr = ffi.new('char[]', outname.encode())
    gplaylist = lib.groove_playlist_create()

    for fname in infilenames:
        gfile = lib.groove_file_open(fname.encode())
        if gfile == ffi.NULL:
            _log.error('Error opening input file %s', fname)
            return 1

        lib.groove_playlist_insert(gplaylist, gfile, 1.0, 1.0, ffi.NULL)

    gencoder = lib.groove_encoder_create()
    gencoder.bit_rate = bitrate * 1000
    gencoder.codec_short_name = codeccstr
    gencoder.format_short_name = fmtcstr
    gencoder.filename = outcstr
    gencoder.mime_type = mimecstr

    if lib.groove_playlist_count(gplaylist) == 1:
        lib.groove_file_audio_format(gplaylist.head.file, ffi.addressof(gencoder.target_audio_format))

        # copy metadata
        gtag = ffi.new('struct GrooveTag **')
        while True:
            gtag[0] = lib.groove_file_metadata_get(gplaylist.head.file, b'', gtag[0], 0)
            if gtag[0] == ffi.NULL:
                break

            key = lib.groove_tag_key(gtag[0])
            value = lib.groove_tag_value(gtag[0])
            _log.warning('key: %s, value %s', ffi.string(key), ffi.string(value))
            lib.groove_encoder_metadata_set(gencoder, key, value, 0)

    if lib.groove_encoder_attach(gencoder, gplaylist) < 0:
        _log.error('error attaching encoder')
        return 1

    with open(outname, 'wb') as ofile:
        gbuffer = ffi.new('struct GrooveBuffer **')
        while lib.groove_encoder_buffer_get(gencoder, gbuffer, 1) == c.GROOVE_BUFFER_YES:
            message = ffi.buffer(gbuffer[0].data[0], gbuffer[0].size)
            ofile.write(message)
            lib.groove_buffer_unref(gbuffer[0])

    lib.groove_encoder_detach(gencoder)
    lib.groove_encoder_destroy(gencoder)

    item = gplaylist.head
    while item != ffi.NULL:
        gfile = item.file
        nextitem = item.next
        lib.groove_playlist_remove(gplaylist, item)
        lib.groove_file_close(gfile)
        item = nextitem

    lib.groove_playlist_destroy(gplaylist)

    return 0


if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        args['--bitrate'] = int(args['--bitrate'])
    except ValueError:
        _log.error('Could not parse bitrate \"%s\" as an integer', args['--bitrate'])
        sys.exit(1)

    assert lib.groove_init() == 0, 'Failed to initialize libgroove'
    lib.groove_set_logging(c.GROOVE_LOG_INFO)

    status = main(
        args['--bitrate'],
        args['--format'],
        args['--codec'],
        args['--mime'],
        args['--output'],
        *args['FILE']
    )

    lib.groove_finish()
    sys.exit(status)
