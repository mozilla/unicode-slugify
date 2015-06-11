import re
import six
import unicodedata
from unidecode import unidecode


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


def slugify(s, ok=SLUG_OK, lower=True, spaces=False, only_ascii=False):
    """
    Creates a unicode slug for given string with several options.

    L and N signify letter/number.
    http://www.unicode.org/reports/tr44/tr44-4.html#GC_Values_Table

    :param s: Your unicode string.
    :param ok: Extra characters outside of alphanumerics to be allowed.
    :param lower: Lower the output string.
    :param spaces: True allows spaces, False replaces a space with a dash (-).
    :param only_ascii: True to replace non-ASCII unicode characters with their ASCII representations.
    :type s: String
    :type ok: String
    :type lower: Bool
    :type spaces: Bool
    :type only_ascii: Bool
    :return: Slugified unicode string

    """

    if only_ascii and type(ok) == unicode:
        try:
            ok.decode('ascii')
        except UnicodeEncodeError:
            raise ValueError((u'You can not use "only_ascii=True" with '
                              u'a non ascii available chars in "ok" ("%s" given)') % ok)

    rv = []
    for c in unicodedata.normalize('NFKC', smart_text(s)):
        cat = unicodedata.category(c)[0]
        if cat in 'LN' or c in ok:
            rv.append(c)
        if cat == 'Z':  # space
            rv.append(' ')
    new = ''.join(rv).strip()

    if only_ascii:
        new = unidecode(new)
    if not spaces:
        new = re.sub('[-\s]+', ('-' if '-' in ok else ''), new)
    if lower:
        new = new.lower()

    return new
