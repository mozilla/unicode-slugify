# -*- coding: utf-8 -*-
import six
import unittest
from nose.tools import eq_, raises

from slugify import slugify, smart_text, SLUG_OK

u = u'Ελληνικά'

def test_slugify():
    x = '-'.join([u, u])
    y = ' - '.join([u, u])

    @raises(ValueError)
    def test_incoherent_ok_and_only_ascii_raises_an_error():
        """Checks that only_ascii=True with non ascii "ok" chars actually raises an error."""
        slugify('angry smiley !', ok='è_é', only_ascii=True)

    def check(x, y):
        eq_(slugify(x), y)

    def check_only_ascii(x, y):
        eq_(slugify(x, only_ascii=True), y)

    def check_only_ascii_capital(x, y):
        eq_(slugify(x, lower=False, only_ascii=True), y)

    def check_only_ascii_lower_nospaces(x, y):
        eq_(slugify(x, lower=True, spaces=False, only_ascii=True), y)

    def check_ok_chars(x, y):
        eq_(slugify(x, ok=u'-♰é_è'), y)

    def check_limited_ok_chars_only_ascii(x, y):
        eq_(slugify(x, ok='-', only_ascii=True), y)

    s = [('xx x  - "#$@ x', 'xx-x-x'),
         (u'Bän...g (bang)', u'bäng-bang'),
         (u, u.lower()),
         (x, x.lower()),
         (y, x.lower()),
         ('    a ', 'a'),
         ('tags/', 'tags'),
         ('holy_wars', 'holy_wars'),
         # Make sure we get a consistent result with decomposed chars:
         (u'el ni\N{LATIN SMALL LETTER N WITH TILDE}o', u'el-ni\xf1o'),
         (u'el nin\N{COMBINING TILDE}o', u'el-ni\xf1o'),
         # Ensure we normalize appearance-only glyphs into their compatibility
         # forms:
         (u'\N{LATIN SMALL LIGATURE FI}lms', u'films'),
         # I don't really care what slugify returns.  Just don't crash.
         (u'x𘍿', u'x'),
         (u'ϧ΃𘒬𘓣',  u'\u03e7'),
         (u'¿x', u'x'),
         (u'Bakıcı geldi', u'bak\u0131c\u0131-geldi'),
         (u'Bäuma means tree', u'b\xe4uma-means-tree')]

    only_ascii = [(u'Bakıcı geldi', u'bakici-geldi'), (u'Bäuma means tree', u'bauma-means-tree')]

    only_ascii_capital = [(u'BÄUMA MEANS TREE', u'BAUMA-MEANS-TREE'),
                          (u'EMİN WAS HERE', u'EMIN-WAS-HERE')]

    only_ascii_lower_nospaces = [(u'北京 (China)', u'bei-jing-china'),
                                 (u'   Москва (Russia)   ', u'moskva-russia'),
                                 (u'♰ Vlad ♰ Țepeș ♰', u'vlad-tepes'),
                                 (u'   ☂   Umbrella   Corp.   ☢   ', u'umbrella-corp'),
                                 (u'~   breaking   space   ~', u'~-breaking-space-~'),]

    ok_chars = [(u'-♰é_è ok but not ☢~', u'-♰é_è-ok-but-not'),
                (u'♰ Vlad ♰ Țepeș ♰', u'♰-vlad-♰-țepeș-♰'),# "ț" and "ș" are not "t" and "s"
                (u'   ☂   Umbrella   Corp.   ☢   ', u'umbrella-corp'),
                (u'~   breaking   space   ~', u'breaking-space'),]

    limited_ok_chars_only_ascii = [(u'♰é_è ☢~', u'ee'),
                (u'♰ Vlad ♰ Țepeș ♰', u'vlad-tepes'), #♰ allowed but "Ț" => "t", "ș" => "s"
                (u'   ☂   Umbrella   Corp.   ☢   ', u'umbrella-corp'),
                (u'~   breaking   space   ~', u'breaking-space'),]

    for val, expected in s:
        yield check, val, expected

    for val, expected in only_ascii:
        yield check_only_ascii, val, expected

    for val, expected in only_ascii_capital:
        yield check_only_ascii_capital, val, expected

    for val, expected in only_ascii_lower_nospaces:
        yield check_only_ascii_lower_nospaces, val, expected

    for val, expected in ok_chars:
        yield check_ok_chars, val, expected

    for val, expected in limited_ok_chars_only_ascii:
        yield check_limited_ok_chars_only_ascii, val, expected


class SmartTextTestCase(unittest.TestCase):

    def test_smart_text_raises_an_error(self):
        """Check that broken __unicode__/__str__ actually raises an error."""

        class MyString(object):
            def __str__(self):
                return b'\xc3\xb6\xc3\xa4\xc3\xbc'

            __unicode__ = __str__

        # str(s) raises a TypeError on python 3 if
        # the result is not a text type.

        # python 2 fails when it tries converting from
        # str to unicode (via ASCII).
        exception = TypeError if six.PY3 else UnicodeError
        self.assertRaises(exception, smart_text, MyString())

    def test_smart_text_works_for_data_model_methods(self):
        """Should identify """
        class TestClass:
            if six.PY3:
                def __str__(self):
                    return 'ŠĐĆŽćžšđ'

                def __bytes__(self):
                    return b'Foo'
            else:
                def __str__(self):
                    return b'Foo'

                def __unicode__(self):
                    return '\u0160\u0110\u0106\u017d\u0107\u017e\u0161\u0111'

        self.assertEqual(smart_text(TestClass()),
                         '\u0160\u0110\u0106\u017d\u0107\u017e\u0161\u0111')
        self.assertEqual(smart_text(1), '1')
        self.assertEqual(smart_text('foo'), 'foo')
        self.assertEqual(smart_text(u), u)
