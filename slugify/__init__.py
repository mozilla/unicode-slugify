import re
import six
import unicodedata

LETTERS = {
    u'\u0131': 'i',
    u'\u015f': 's',
    u'\xe7': 'c',
    u'\u011f': 'g',
    u'\xf6': 'o',
    u'\xfc': 'u',
    u'\xe2': 'a',
    u'\xee': 'i'
}

CAPITAL_LETTERS = {
    u'\u0130': 'I',
    u'\u015e': 'S',
    u'\xc7': 'C',
    u'\u011e': 'G',
    u'\xd6': 'O',
    u'\xdc': 'U',
    u'\xc2': 'A',
    u'\xce': 'I'
}

def smart_text(s, encoding='utf-8', errors='strict'):
    if isinstance(s, six.text_type):
        return s

    if not isinstance(s, six.string_types):
        if six.PY3:
            if isinstance(s, bytes):
                s = six.text_type(s, encoding, errors)
            else:
                s = six.text_type(s)
        elif hasattr(s, '__unicode__'):
            s = six.text_type(s)
        else:
            s = six.text_type(bytes(s), encoding, errors)
    else:
        s = six.text_type(s)
    return s


# Extra characters outside of alphanumerics that we'll allow.
SLUG_OK = '-_~'


def slugify(s, ok=SLUG_OK, lower=True, spaces=False):
    # L and N signify letter/number.
    # http://www.unicode.org/reports/tr44/tr44-4.html#GC_Values_Table
    rv = []
    for c in unicodedata.normalize('NFKC', smart_text(s)):
        cat = unicodedata.category(c)[0]
        if cat in 'LN' or c in ok:
            rv.append(c)
        if cat == 'Z':  # space
            rv.append(' ')
    new = ''.join(rv).strip()
    if not spaces:
        new = re.sub('[-\s]+', '-', new)
    return new.lower() if lower else new
