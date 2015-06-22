===============
``baseunicode``
===============

What is this?
=============

It's ``base64``, but with more characters. Whereas ``base64`` encodes 6 bits /
character, ``baseunicode`` can currently encode 11. Note that this is *bits per
character*, not *bits per output byte*. ``baseunicode`` is not intended to be
the most efficient *per byte*.

Specifically, ``baseunicode`` optimizes for screen space. It aims to help
provide an extremely rudimentary file transfer method: display a text string,
somehow transmit it, then decode it on the other end, using copy-paste between
the terminal and something like a chat program. To keep the copy-pasting to a
minimum, we use Unicode, which allows us to compact more information into less
screen area. (And you can copy Unicode, whereas raw bytes do not copy quite as
well.) Since most channels (like chat) handle Unicode just fine, we allow the
use of such characters.

Most channels handle unicode data just fine, so why stop at 64 characters?

``baseunicode`` is intended for one-off manual transfers. Production stuff
should probably use ``base64``, since the output is more recognizable and less
susceptible to corruption, or just find a way to actually transmit raw bytes.


Format
======

The rough outline:

::

    <unicode string data>
      "!" <last couple of bits of data>
      "!" <number of bits in the last bit>
      "!" <FNV-1a 64-bit checksum, as a base16 integer>

The alphabet is assumed to be pre-agreed on.
