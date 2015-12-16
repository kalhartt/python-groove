# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from cffi import FFI

##########
# Header definitions
##########

_groove_header = r"""
int groove_init(void);
void groove_finish(void);
void groove_set_logging(int level);

int groove_channel_layout_count(uint64_t channel_layout);
uint64_t groove_channel_layout_default(int count);

enum GrooveSampleFormat {
    GROOVE_SAMPLE_FMT_NONE = -1,
    GROOVE_SAMPLE_FMT_U8,
    GROOVE_SAMPLE_FMT_S16,
    GROOVE_SAMPLE_FMT_S32,
    GROOVE_SAMPLE_FMT_FLT,
    GROOVE_SAMPLE_FMT_DBL,

    GROOVE_SAMPLE_FMT_U8P,
    GROOVE_SAMPLE_FMT_S16P,
    GROOVE_SAMPLE_FMT_S32P,
    GROOVE_SAMPLE_FMT_FLTP,
    GROOVE_SAMPLE_FMT_DBLP,
};

struct GrooveAudioFormat {
    int sample_rate;
    uint64_t channel_layout;
    enum GrooveSampleFormat sample_fmt;
};

int groove_sample_format_bytes_per_sample(enum GrooveSampleFormat format);

int groove_audio_formats_equal(const struct GrooveAudioFormat *a, const struct GrooveAudioFormat *b);

int groove_version_major(void);
int groove_version_minor(void);
int groove_version_patch(void);
const char *groove_version(void);
"""

##########
# FFI Build
##########

_groove_source = r"""
#include <groove/encoder.h>
#include <groove/groove.h>
#include <groove/queue.h>
"""
ffi_groove = FFI()
ffi_groove.set_source('groove._groove', _groove_source, libraries=['groove'])
ffi_groove.cdef(_groove_header)

if __name__ == '__main__':
    ffi_groove.compile()
