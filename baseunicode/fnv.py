class Fnv1A_64(object):
    _PRIME = 1099511628211
    _OFFSET_BASIS = 14695981039346656037
    _HASH_MODULO_MASK = 2 ** 64 - 1

    def __init__(self):
        self._hash = self._OFFSET_BASIS

    def update(self, data):
        for octet in data:
            self._hash = (self._hash * self._PRIME) & self._HASH_MODULO_MASK
            self._hash ^= octet

    def digest(self):
        return self._hash
