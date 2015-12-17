# -*- coding: utf-8 -*-

##########
# groove/groove.h
##########

GROOVE_LOG_QUIET = -8
GROOVE_LOG_ERROR = 16
GROOVE_LOG_WARNING = 24
GROOVE_LOG_INFO = 32

GROOVE_CH_FRONT_LEFT = 0x00000001
GROOVE_CH_FRONT_RIGHT = 0x00000002
GROOVE_CH_FRONT_CENTER = 0x00000004
GROOVE_CH_LOW_FREQUENCY = 0x00000008
GROOVE_CH_BACK_LEFT = 0x00000010
GROOVE_CH_BACK_RIGHT = 0x00000020
GROOVE_CH_FRONT_LEFT_OF_CENTER = 0x00000040
GROOVE_CH_FRONT_RIGHT_OF_CENTER = 0x00000080
GROOVE_CH_BACK_CENTER = 0x00000100
GROOVE_CH_SIDE_LEFT = 0x00000200
GROOVE_CH_SIDE_RIGHT = 0x00000400
GROOVE_CH_TOP_CENTER = 0x00000800
GROOVE_CH_TOP_FRONT_LEFT = 0x00001000
GROOVE_CH_TOP_FRONT_CENTER = 0x00002000
GROOVE_CH_TOP_FRONT_RIGHT = 0x00004000
GROOVE_CH_TOP_BACK_LEFT = 0x00008000
GROOVE_CH_TOP_BACK_CENTER = 0x00010000
GROOVE_CH_TOP_BACK_RIGHT = 0x00020000
GROOVE_CH_STEREO_LEFT = 0x20000000
GROOVE_CH_STEREO_RIGHT = 0x40000000
GROOVE_CH_WIDE_LEFT = 0x0000000080000000
GROOVE_CH_WIDE_RIGHT = 0x0000000100000000

GROOVE_CH_LAYOUT_MONO = (GROOVE_CH_FRONT_CENTER)
GROOVE_CH_LAYOUT_STEREO = (GROOVE_CH_FRONT_LEFT|GROOVE_CH_FRONT_RIGHT)
GROOVE_CH_LAYOUT_2POINT1 = (GROOVE_CH_LAYOUT_STEREO|GROOVE_CH_LOW_FREQUENCY)
GROOVE_CH_LAYOUT_2_1 = (GROOVE_CH_LAYOUT_STEREO|GROOVE_CH_BACK_CENTER)
GROOVE_CH_LAYOUT_SURROUND = (GROOVE_CH_LAYOUT_STEREO|GROOVE_CH_FRONT_CENTER)
GROOVE_CH_LAYOUT_3POINT1 = (GROOVE_CH_LAYOUT_SURROUND|GROOVE_CH_LOW_FREQUENCY)
GROOVE_CH_LAYOUT_4POINT0 = (GROOVE_CH_LAYOUT_SURROUND|GROOVE_CH_BACK_CENTER)
GROOVE_CH_LAYOUT_4POINT1 = (GROOVE_CH_LAYOUT_4POINT0|GROOVE_CH_LOW_FREQUENCY)
GROOVE_CH_LAYOUT_2_2 = (GROOVE_CH_LAYOUT_STEREO|GROOVE_CH_SIDE_LEFT|GROOVE_CH_SIDE_RIGHT)
GROOVE_CH_LAYOUT_QUAD = (GROOVE_CH_LAYOUT_STEREO|GROOVE_CH_BACK_LEFT|GROOVE_CH_BACK_RIGHT)
GROOVE_CH_LAYOUT_5POINT0 = (GROOVE_CH_LAYOUT_SURROUND|GROOVE_CH_SIDE_LEFT|GROOVE_CH_SIDE_RIGHT)
GROOVE_CH_LAYOUT_5POINT1 = (GROOVE_CH_LAYOUT_5POINT0|GROOVE_CH_LOW_FREQUENCY)
GROOVE_CH_LAYOUT_5POINT0_BACK = (GROOVE_CH_LAYOUT_SURROUND|GROOVE_CH_BACK_LEFT|GROOVE_CH_BACK_RIGHT)
GROOVE_CH_LAYOUT_5POINT1_BACK = (GROOVE_CH_LAYOUT_5POINT0_BACK|GROOVE_CH_LOW_FREQUENCY)
GROOVE_CH_LAYOUT_6POINT0 = (GROOVE_CH_LAYOUT_5POINT0|GROOVE_CH_BACK_CENTER)
GROOVE_CH_LAYOUT_6POINT0_FRONT = (GROOVE_CH_LAYOUT_2_2|GROOVE_CH_FRONT_LEFT_OF_CENTER|GROOVE_CH_FRONT_RIGHT_OF_CENTER)
GROOVE_CH_LAYOUT_HEXAGONAL = (GROOVE_CH_LAYOUT_5POINT0_BACK|GROOVE_CH_BACK_CENTER)
GROOVE_CH_LAYOUT_6POINT1 = (GROOVE_CH_LAYOUT_5POINT1|GROOVE_CH_BACK_CENTER)
GROOVE_CH_LAYOUT_6POINT1_BACK = (GROOVE_CH_LAYOUT_5POINT1_BACK|GROOVE_CH_BACK_CENTER)
GROOVE_CH_LAYOUT_6POINT1_FRONT = (GROOVE_CH_LAYOUT_6POINT0_FRONT|GROOVE_CH_LOW_FREQUENCY)
GROOVE_CH_LAYOUT_7POINT0 = (GROOVE_CH_LAYOUT_5POINT0|GROOVE_CH_BACK_LEFT|GROOVE_CH_BACK_RIGHT)
GROOVE_CH_LAYOUT_7POINT0_FRONT = (GROOVE_CH_LAYOUT_5POINT0|GROOVE_CH_FRONT_LEFT_OF_CENTER|GROOVE_CH_FRONT_RIGHT_OF_CENTER)
GROOVE_CH_LAYOUT_7POINT1 = (GROOVE_CH_LAYOUT_5POINT1|GROOVE_CH_BACK_LEFT|GROOVE_CH_BACK_RIGHT)
GROOVE_CH_LAYOUT_7POINT1_WIDE = (GROOVE_CH_LAYOUT_5POINT1|GROOVE_CH_FRONT_LEFT_OF_CENTER|GROOVE_CH_FRONT_RIGHT_OF_CENTER)
GROOVE_CH_LAYOUT_7POINT1_WIDE_BACK = (GROOVE_CH_LAYOUT_5POINT1_BACK|GROOVE_CH_FRONT_LEFT_OF_CENTER|GROOVE_CH_FRONT_RIGHT_OF_CENTER)
GROOVE_CH_LAYOUT_OCTAGONAL = (GROOVE_CH_LAYOUT_5POINT0|GROOVE_CH_BACK_LEFT|GROOVE_CH_BACK_CENTER|GROOVE_CH_BACK_RIGHT)
GROOVE_CH_LAYOUT_STEREO_DOWNMIX = (GROOVE_CH_STEREO_LEFT|GROOVE_CH_STEREO_RIGHT)

GROOVE_SAMPLE_FMT_NONE = -1
GROOVE_SAMPLE_FMT_U8 = 0
GROOVE_SAMPLE_FMT_S16 = 1
GROOVE_SAMPLE_FMT_S32 = 2
GROOVE_SAMPLE_FMT_FLT = 3
GROOVE_SAMPLE_FMT_DBL = 4
GROOVE_SAMPLE_FMT_U8P = 5
GROOVE_SAMPLE_FMT_S16P = 6
GROOVE_SAMPLE_FMT_S32P = 7
GROOVE_SAMPLE_FMT_FLTP = 8
GROOVE_SAMPLE_FMT_DBLP = 9

GROOVE_TAG_MATCH_CASE = 1
GROOVE_TAG_DONT_OVERWRITE = 16
GROOVE_TAG_APPEND = 32

GROOVE_EVERY_SINK_FULL = 0
GROOVE_ANY_SINK_FULL = 1

GROOVE_BUFFER_NO = 0
GROOVE_BUFFER_YES = 1
GROOVE_BUFFER_END = 2