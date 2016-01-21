==============
Channels
==============

.. class:: Channel

    Integer enumeration identifying a channel in a :class:`ChannelLayout`

    Implementation details
    ----------------------

    A channel is a bitflag. See the libgroove `Channel definitions`_ for
    the numeric values.

    ================
    attribute
    ================
    front_left
    front_right
    front_center
    low_frequency
    back_left
    back_right
    left_of_center
    right_of_center
    back_center
    side_left
    side_right
    top_center
    top_front_left
    top_front_center
    top_front_right
    top_back_left
    top_back_center
    top_back_right
    stereo_left
    stereo_right
    wide_left
    wide_right

.. class:: ChannelLayout

    Integer enumeration identifying the channels carried by a
    :class:`AudioFormat`.

    Implementation details
    ----------------------

    A layout is a bitmask of channels, the set bits of a
    layouts value identify the channels it carries. See the libgroove
    `ChannelLayout definitions`_ for the numeric values.

    =====================
    attribute
    =====================
    layout_mono
    layout_stereo
    layout_2p1
    layout_2_1
    layout_surround
    layout_3p1
    layout_4p0
    layout_4p1
    layout_2_2
    layout_quad
    layout_5p0
    layout_5p1
    layout_5p0
    layout_5p1
    layout_6p0
    layout_6p0_front
    layout_hexagonal
    layout_6p1
    layout_6p1_back
    layout_6p1_front
    layout_7p0
    layout_7p0_front
    layout_7p1
    layout_7p1_wide
    layout_7p1_wide_back
    layout_octagonal
    layout_stereo_downmix


.. _`Channel definitions`: https://github.com/andrewrk/libgroove/blob/4.3.0/groove/groove.h#L40-L61
.. _`ChannelLayout definitions`: https://github.com/andrewrk/libgroove/blob/4.3.0/groove/groove.h#L63-L89
