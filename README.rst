===============
``baseunicode``
===============

What is this?
=============

It's ``base64``, but with more characters. Whereas ``base64`` encodes 6 bits /
character, ``baseunicode`` can currently encode 11. Note that this is *bits per
character*, not *bits per output byte*. ``baseunicode`` is intended to be
efficient in the visible screen area consumed by the text; it is not intended
to be the most efficient *per byte*.

This is a toy tool, written for fun. **It is not intended for serious
production use.**

An example::

    % python -m baseunicode encode <<EOF
    heredoc> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
    ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
    velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
    est laborum.
    heredoc> EOF
    ⏙⋚∢X⌟⍭⇩ҖՖ≹∾żɌЊ↧ň⇮⁍Ȗ8⊿ₒ₎яผ⁎≞ſɌćʞҮҔวǪӢɋďʠӎN⋱ǚT⋏ģƍѯҠ∻ȂT⏏ϮՑҦ·↱≆⁑⋓ė⇦Ҟ¹⌱Ȗ⊝⊣⍑※я↭⌙Æ
    ◶⍓ₒơňƲ₣≆R⊟ϼณӖ⋮Իƙ\⋟ЀѾňบՂ≁⏁⌣ğ∕яƳխǺ8⎟Ў₍ň▲⋺Ȗϝ⋔ʅ⊦яҝ↹≞ɵ⌤ₒ=Ӕลխ≂◵ɋϼÝҦƷ⋺Æ⁗⏃ė⇕ӎť∙∲Ϝ⌤ĥ
    ƍӮ↭լ’◵⍣⍧ŠҦф≹≆ϝ⎣Ў↥ƸՖ⌵∲[⊟įƢňʮ⌻≖T⋏ģԆҾť≚Æϝ⎓Јɞяว⁌≖ɹɌ₅=Ӝศ⌺Ȇÿ⏓ď∕яƱ⌚’Ƿ⏄ďčѯล⌺Ǻɕ⎃⍥※я↭
    ⌹Æϗ⌄϶↥ň⇻∛∾R⎏⁵ʡЯ∁⋛þδ◈ϪՏӎ⇲⋛’⁙⍳ĭӳпƨ⁌√ɵɌϪՓѯƩ⌙Ǌ\⍯ₒ=Ҭ▶↺∞⎿⏓z⁻ӖวՄǩY⊿įՑЯť⌻Ǫ◔⋳ϰğѯ¥“∢ϝ
    ⎳₡↨ň▱√∾ɹɌ⁵ʠҖť‥’Ƿ⏔b}зΒ⌻Ǻ↤!"!4!2238ba0df6108cf5

.. note::

   Line breaks added to the above for readability.

``baseunicode`` optimizes for screen space. It aims to help provide an
extremely rudimentary file transfer method: display a text string, somehow
transmit it, then decode it on the other end, such as using copy-paste between
the terminal and something like a chat program. To keep the copy-pasting to a
minimum, we use Unicode, which allows us to compact more information into less
screen area. (And you can copy Unicode, whereas raw bytes do not copy quite as
well.) Since most channels (like chat) handle Unicode just fine, we allow the
use of such characters.

``baseunicode`` is intended for one-off manual transfers. Production stuff
should probably just use ``base64``, since the output is more recognizable and
less susceptible to corruption, or just find a way to actually transmit raw
bytes.

Why is this?
============

I found myself needing to transfer a *lot* of small pieces of data between VMs.
I'm often SSH'd into both ends, and I was copy/pasting text between SSH
sessions. For binary data, I was doing ``| base64`` to make it displayable.

This works fine, but scrolling is a pain point: sometimes you have to wait for
the windowing layer to scroll the window, which it will only do at a finite
speed. Sometimes, you're in ``screen``, and selecting a continuous blob is
impossible. If only we could fit the entirety of our data on the screen, so we
could copy-paste it to another window, and decode it there.

and thus, this tool. Mostly as a toy, and a proof of concept. This is not
seriously intended to be used in production anywhere (often, bytes are more
important).


Why not ``scp``?
----------------

``scp`` is often a better answer than copy-pasting text between terminal
windows. However, consider that I do VM-to-VM transfers:

* ``scp`` requires the ``-3`` flag for remote-to-remote transfers. (by default,
  it attempts to ssh from the first remote to the second; our VMs in production
  don't have access to other VMs, as that would make a single compromise
  *extremely* bad, and we don't do agent forwarding for security.)
* ``scp`` can't transfer a file that requires ``sudo`` to access (to my
  knowledge, at least).
* ``scp`` has a bizarre syntax for filenames:
  ``scp 'remote:/dir/dir/Bad\ File\ Name' ...`` — note how we need to escape
  that filename *twice*, as if ``scp`` runs its arg through the shell a second
  time. It's weird, and I still have no idea why I'm required to do this.

The only real argument is the ``sudo`` one; that can somewhat be overcome by
re-implementing ``scp``::

    ssh remote 'sudo tar -C /dir -cz <paths>' | ssh other-remote 'sudo tar -xz -C …'


Format
======

The rough outline:

::

    <unicode string data>
      "!" <last couple of bits of data>
      "!" <number of bits in the last bit>
      "!" <FNV-1a 64-bit checksum, as a base16 integer>

The alphabet is assumed to be pre-agreed on.
