Changelog
=========

.. _MP3: https://en.wikipedia.org/wiki/MP3
.. _CBR: https://en.wikipedia.org/wiki/Constant_bitrate
.. _M4A: https://en.wikipedia.org/wiki/MPEG-4_Part_14
.. _MP4: https://en.wikipedia.org/wiki/Mp4
.. _Opus: https://en.wikipedia.org/wiki/Opus_(audio_format)
.. _Vorbis: https://en.wikipedia.org/wiki/Vorbis
.. _FFmpeg: https://en.wikipedia.org/wiki/FFmpeg

* 0.2.0 - 2021-04-13

  - We can add chapters to M4A_ files now. This feature requires
    availability of FFmpeg_ software.

  - We can add chapters to Opus_ files now.

  - We can add chapters to Vorbis_ files now.

  - The chapter end time should be provided in the TOC object,
    instead of each audio tagger taking care of calculating it.

* 0.1.0 - 2021-04-09

  Initial release. It can add chapters to MP3_ files.

  .. warning::

     In many MP3_ players, the MP3_ file **MUST BE** CBR_ in order
     for the chapter metadata seeking to be accurate.
