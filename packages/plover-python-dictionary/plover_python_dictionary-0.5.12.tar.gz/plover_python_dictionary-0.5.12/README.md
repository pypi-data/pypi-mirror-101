# Plover Python dictionary

Add support for Python dictionaries to Plover.


## Usage

A Python dictionary is simply a single module with the following API:

``` python
# Length of the longest supported key (number of strokes).
LONGEST_KEY = 1

# Lookup function: return the translation for <key> (a tuple of strokes)
# or raise KeyError if no translation is available/possible.
def lookup(key):
    assert len(key) <= LONGEST_KEY
    raise KeyError

# Optional: return an array of stroke tuples that would translate back
# to <text> (an empty array if not possible).
def reverse_lookup(text):
    return []
```

For example save the following code to `show_stroke.py`:

``` python
LONGEST_KEY = 2

SHOW_STROKE_STENO = 'STR*'

def lookup(key):
    assert len(key) <= LONGEST_KEY, '%d/%d' % (len(key), LONGEST_KEY)
    if SHOW_STROKE_STENO != key[0]:
        raise KeyError
    if len(key) == 1:
        return ' '
    return key[1]
```

Then add it to your dictionaries stack as you would a normal dictionary.

Now, if you stroke `STR*`, then the next stroke will be shown verbatim
(untranslated), e.g. `-T STROEBG TP-R KW-GS STROEBG KR-GS S STR* STROEBG`
outputs: `the stroke for "stroke" is STROEBG`.

## Release history

### 0.5.12

* update changelog...

### 0.5.11

* drop support for Python < 3.6
* fix use of deprecated `imp` module
* rework tests to use `plover_build_utils.testing`
* use PEP 517/518

### 0.5.10

* fix `./setup.py test` handling
* fix default implementation of `reverse_lookup` to return a list (not a tuple)

### 0.5.9

* update to Plover's latest API
