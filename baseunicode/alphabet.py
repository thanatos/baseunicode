_BASIC_LATIN = list(range(0x22, 0x7e + 1))
_LATIN1_SUPPLEMENT = (
    list(range(0xa1, 0xac + 1)) + list(range(0xae, 0xff + 1))
)
_LATIN_EXTENDED_A = (
    list(range(0x100, 0x17f + 1))
)
_LATIN_EXTENDED_B = (
    list(range(0x180, 0x24f + 1))
)
_IPA_EXTENSIONS = (
    list(range(0x250, 0x2af + 1))
)
# Note: has some weird holes
_GREEK_AND_COPTIC = (
    list(range(0x38e, 0x3a1 + 1))
    + list(range(0x3a3, 0x3ff + 1))
)
# More weird holes:
_CYRILLIC = (
    list(range(0x400, 0x482 + 1))
    + list(range(0x48a, 0x4ff + 1))
)
# Some weird ones at the end:
_CYRILLIC_SUPPLEMENT = (
    list(range(0x500, 0x525 + 1))
)
# More holes.
_ARMENIAN = (
    list(range(0x531, 0x556 + 1))
    + list(range(0x561, 0x587 + 1))
)
# Holes.
_THAI = (
    list(range(0xe01, 0xe30 + 1))
)
# Evil whitespace.
_GENERAL_PUNCTUATION = (
    list(range(0x2010, 0x2027 + 1))
    + list(range(0x2030, 0x205e + 1))
)
_SUPERSCRIPTS_AND_SUBSCRIPTS = (
    [0x2070, 0x2071]
    + list(range(0x2074, 0x208e + 1))
    + list(range(0x2090, 0x209c + 1))
)
# Missing a few:
_CURRENCY_SYMBOLS = (
    list(range(0x20a0, 0x20b9 + 1))
)
_ARROWS = (
    list(range(0x2190, 0x21ff + 1))
)
_MATHEMATICAL_OPERATORS = (
    list(range(0x2200, 0x22ff + 1))
)
# Missing a few:
_MISCELLANEOUS_TECHINICAL = (
    list(range(0x2300, 0x23e8 + 1))
)
_GEOMETRIC_SHAPES = (
    list(range(0x25a0, 0x25ff + 1))
)
_SUPPLEMENTAL_MATHEMATICAL_OPERATORS = (
    list(range(0x2a00, 0x2aff + 1))
)

USABLE_CHARS = ([]
    + _BASIC_LATIN
    + _LATIN1_SUPPLEMENT
    + _LATIN_EXTENDED_A
    + _LATIN_EXTENDED_B
    + _IPA_EXTENSIONS
    + _GREEK_AND_COPTIC
    + _CYRILLIC
    + _CYRILLIC_SUPPLEMENT
    + _ARMENIAN
    + _THAI
    + _GENERAL_PUNCTUATION
    + _SUPERSCRIPTS_AND_SUBSCRIPTS
    + _CURRENCY_SYMBOLS
    + _ARROWS
    + _MATHEMATICAL_OPERATORS
    + _MISCELLANEOUS_TECHINICAL
    + _GEOMETRIC_SHAPES
    + _SUPPLEMENTAL_MATHEMATICAL_OPERATORS
)
