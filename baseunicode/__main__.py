#!/usr/bin/env python3

import math
import re
import sys

from . import alphabet
from . import fnv


def number_of_usable_bits(usable_chars):
    length = len(usable_chars)
    usable_bits = 0
    while True:
        if length < 2 ** (usable_bits + 1):
            break
        usable_bits += 1
    return usable_bits


def encode(usable_chars, stream):
    assert 256 <= len(usable_chars)

    bit_buffer = 0
    current_shift = 0
    bits_per_symbol = number_of_usable_bits(usable_chars)
    ones = 2 ** bits_per_symbol - 1
    datahash = fnv.Fnv1A_64()
    while True:
        byte = stream.read(1)
        if byte == b'':
            break
        datahash.update(byte)
        byte = byte[0]
        bit_buffer |= (byte << current_shift)
        current_shift += 8
        if bits_per_symbol <= current_shift:
            yield chr(usable_chars[bit_buffer & ones])
            bit_buffer >>= bits_per_symbol
            current_shift -= bits_per_symbol
    yield '!{}!{}!{}'.format(
        chr(usable_chars[bit_buffer]), current_shift, hex(datahash.digest())[2:]
    )


class DecodeError(Exception):
    pass


def decode(usable_chars, stream):
    inverted_lookup = {c: idx for idx, c in enumerate(usable_chars)}
    bit_buffer = 0
    current_shift = 0
    bits_per_symbol = number_of_usable_bits(usable_chars)
    ones = 2 ** bits_per_symbol - 1
    datahash = fnv.Fnv1A_64()

    while True:
        c = stream.read(1)
        if c == '':
            raise DecodeError('Unexpected end of input.')
        if c == '!':
            break
        value = inverted_lookup[ord(c)]
        bit_buffer |= value << current_shift
        current_shift += bits_per_symbol
        while 8 <= current_shift:
            octet = bit_buffer & 0xff
            bit_buffer >>= 8
            current_shift -= 8
            yield octet
            datahash.update(bytes((octet,)))

    last_bit = stream.read(4096)
    m = re.match('^([^!]+)!([0-9]+)!([^!]+)$', last_bit)
    if not m:
        raise DecodeError('Could not read trailer.')
    value = inverted_lookup[ord(m.group(1))]
    bit_buffer |= value << current_shift
    current_shift += int(m.group(2))
    assert current_shift % 8 == 0
    while current_shift:
        octet = bit_buffer & 0xff
        bit_buffer >>= 8
        current_shift -= 8
        yield octet
        datahash.update(bytes((octet,)))

    if datahash.digest() != int(m.group(3), 16):
        raise DecodeError('Checksum did not match! (Got {:x}, excepted {:x})'.format(
            datahash.digest(), int(m.group(3), 16)
        ))


if __name__ == '__main__':
    if sys.argv[1] == 'encode':
        for c in encode(alphabet.USABLE_CHARS, sys.stdin.buffer):
            sys.stdout.write(c)
    elif sys.argv[1] == 'decode':
        for b in decode(alphabet.USABLE_CHARS, sys.stdin):
            sys.stdout.buffer.write(bytes((b,)))
    elif sys.argv[1] == 'about':
        print(
            'Number of usable bits per character: {}'.format(
                number_of_usable_bits(alphabet.USABLE_CHARS)
            )
        )
        print(
            'len(characters): {}'.format(len(alphabet.USABLE_CHARS))
        )
        print(
            'log(len(characters)): {}'.format(
                math.log2(len(alphabet.USABLE_CHARS))
            )
        )
