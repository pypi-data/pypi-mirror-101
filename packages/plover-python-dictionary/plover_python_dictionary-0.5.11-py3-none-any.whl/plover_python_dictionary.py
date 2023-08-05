# vim: set fileencoding=utf-8 :

from plover.steno_dictionary import StenoDictionary


class PythonDictionary(StenoDictionary):

    readonly = True

    def __init__(self):
        super().__init__()
        self._mod = None
        self._lookup = None
        self._reverse_lookup = None
        self.readonly = True

    def _load(self, filename):
        with open(filename) as fp:
            source = fp.read()
        mod = {}
        exec(source, mod)
        longest_key = mod.get('LONGEST_KEY')
        if not isinstance(longest_key, int) or longest_key <= 0:
            raise ValueError('missing or invalid `LONGEST_KEY\' constant: %s\n' % longest_key)
        lookup = mod.get('lookup')
        if not isinstance(lookup, type(lambda x: x)):
            raise ValueError('missing or invalid `lookup\' function: %s\n' % lookup)
        reverse_lookup = mod.get('reverse_lookup', lambda x: [])
        if not isinstance(reverse_lookup, type(lambda x: x)):
            raise ValueError('invalid `reverse_lookup\' function: %s\n' % reverse_lookup)
        self._mod = mod
        self._lookup = lookup
        self._longest_key = longest_key
        self._reverse_lookup = reverse_lookup

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __getitem__(self, key):
        return self._lookup(key)

    def get(self, key, fallback=None):
        try:
            return self._lookup(key)
        except KeyError:
            return fallback

    def reverse_lookup(self, value):
        return self._reverse_lookup(value)
