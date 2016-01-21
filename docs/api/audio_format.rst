============
Audio Format
============

.. class:: AudioFormat

    Represents a format for audio samples. This class wraps `struct
    GrooveAudioFormat`_.

    .. attribute:: sample_rate

       Sample rate in Hz

    .. attribute:: channel_layout

       :class:`ChannelLayout` describing the channels carried in the
       format.

    .. attribute:: sample_format

       :class:`SampleFormat` describing the format of each sample.

    .. method:: clone(other)

       Copy the attributes of another AudioFormat. After a clone, `audio_fmt ==
       other` will be `True`.


.. _`struct GrooveAudioFormat`: http://andrewrk.github.io/libgroove/structGrooveAudioFormat.html
