import re
import six
import unicodedata

LETTERS = {
    u'\N{LATIN SMALL LETTER DOTLESS I}': 'i',
    u'\N{LATIN SMALL LETTER S WITH CEDILLA}': 's',
    u'\N{LATIN SMALL LETTER C WITH CEDILLA}': 'c',
    u'\N{LATIN SMALL LETTER G WITH BREVE}': 'g',
    u'\N{LATIN SMALL LETTER O WITH DIAERESIS}': 'o',
    u'\N{LATIN SMALL LETTER U WITH DIAERESIS}': 'u',
    u'\N{LATIN SMALL LETTER A WITH GRAVE}' : 'a',
    u'\N{LATIN SMALL LETTER A WITH ACUTE}' : 'a',
    u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}' : 'a',
    u'\N{LATIN SMALL LETTER A WITH TILDE}' : 'a',
    u'\N{LATIN SMALL LETTER A WITH DIAERESIS}' : 'a',
    u'\N{LATIN SMALL LETTER A WITH RING ABOVE}' : 'a',
    u'\N{LATIN SMALL LETTER A WITH MACRON}': 'a',
    u'\N{LATIN SMALL LETTER A WITH BREVE}': 'a',
    u'\N{LATIN SMALL LETTER AE}' : 'ae',
    u'\N{LATIN SMALL LETTER E WITH GRAVE}' : 'e',
    u'\N{LATIN SMALL LETTER E WITH ACUTE}' : 'e',
    u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}' : 'e',
    u'\N{LATIN SMALL LETTER E WITH DIAERESIS}' : 'e',
    u'\N{LATIN SMALL LETTER I WITH GRAVE}' : 'i',
    u'\N{LATIN SMALL LETTER I WITH ACUTE}' : 'i',
    u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}' : 'i',
    u'\N{LATIN SMALL LETTER I WITH DIAERESIS}' : 'i',
    u'\N{LATIN SMALL LETTER N WITH TILDE}' : 'n',
    u'\N{LATIN SMALL LETTER O WITH GRAVE}' : 'o',
    u'\N{LATIN SMALL LETTER O WITH ACUTE}' : 'o',
    u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}' : 'o',
    u'\N{LATIN SMALL LETTER O WITH TILDE}' : 'o',
    u'\N{LATIN SMALL LETTER O WITH STROKE}': 'o',
    u'\N{LATIN SMALL LETTER U WITH GRAVE}': 'u',
    u'\N{LATIN SMALL LETTER U WITH ACUTE}': 'u',
    u'\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}': 'u',
    u'\N{LATIN SMALL LETTER Y WITH ACUTE}': 'y',
    u'\N{LATIN SMALL LETTER Y WITH DIAERESIS}': 'y'
}

CAPITAL_LETTERS = {
    u'\N{LATIN CAPITAL LETTER I WITH DOT ABOVE}': 'I',
    u'\N{LATIN CAPITAL LETTER S WITH CEDILLA}': 'S',
    u'\N{LATIN CAPITAL LETTER C WITH CEDILLA}': 'C',
    u'\N{LATIN CAPITAL LETTER G WITH BREVE}': 'G',
    u'\N{LATIN CAPITAL LETTER O WITH DIAERESIS}': 'O',
    u'\N{LATIN CAPITAL LETTER U WITH DIAERESIS}': 'U',
    u'\N{LATIN CAPITAL LETTER A WITH GRAVE}' : 'A',
    u'\N{LATIN CAPITAL LETTER A WITH ACUTE}' : 'A',
    u'\N{LATIN CAPITAL LETTER A WITH CIRCUMFLEX}' : 'A',
    u'\N{LATIN CAPITAL LETTER A WITH TILDE}' : 'A',
    u'\N{LATIN CAPITAL LETTER A WITH DIAERESIS}' : 'A',
    u'\N{LATIN CAPITAL LETTER A WITH RING ABOVE}' : 'A',
    u'\N{LATIN CAPITAL LETTER A WITH MACRON}': 'A',
    u'\N{LATIN CAPITAL LETTER A WITH BREVE}': 'A',
    u'\N{LATIN CAPITAL LETTER AE}' : 'AE',
    u'\N{LATIN CAPITAL LETTER E WITH GRAVE}' : 'E',
    u'\N{LATIN CAPITAL LETTER E WITH ACUTE}' : 'E',
    u'\N{LATIN CAPITAL LETTER E WITH CIRCUMFLEX}' : 'E',
    u'\N{LATIN CAPITAL LETTER E WITH DIAERESIS}' : 'E',
    u'\N{LATIN CAPITAL LETTER I WITH GRAVE}' : 'I',
    u'\N{LATIN CAPITAL LETTER I WITH ACUTE}' : 'I',
    u'\N{LATIN CAPITAL LETTER I WITH CIRCUMFLEX}' : 'I',
    u'\N{LATIN CAPITAL LETTER I WITH DIAERESIS}' : 'I',
    u'\N{LATIN CAPITAL LETTER N WITH TILDE}' : 'N',
    u'\N{LATIN CAPITAL LETTER O WITH GRAVE}' : 'O',
    u'\N{LATIN CAPITAL LETTER O WITH ACUTE}' : 'O',
    u'\N{LATIN CAPITAL LETTER O WITH CIRCUMFLEX}' : 'O',
    u'\N{LATIN CAPITAL LETTER O WITH TILDE}' : 'O',
    u'\N{LATIN CAPITAL LETTER O WITH STROKE}': 'O',
    u'\N{LATIN CAPITAL LETTER U WITH GRAVE}': 'U',
    u'\N{LATIN CAPITAL LETTER U WITH ACUTE}': 'U',
    u'\N{LATIN CAPITAL LETTER U WITH CIRCUMFLEX}': 'U',
    u'\N{LATIN CAPITAL LETTER Y WITH ACUTE}': 'Y',
    u'\N{LATIN CAPITAL LETTER Y WITH DIAERESIS}': 'Y'
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


def slugify(s, ok=SLUG_OK, lower=True, spaces=False, smart_replace=False):
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

    new = new.lower() if lower else new

    # Smart replace
    if smart_replace == True:

        for char, new_char in LETTERS.items():
            new = new.replace(char, new_char)

        if not lower:
            for char, new_char in CAPITAL_LETTERS.items():
                new = new.replace(char, new_char)

    return new
