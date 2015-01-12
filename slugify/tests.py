# -*- coding: utf-8 -*-
import six
import unittest
from nose.tools import eq_

from slugify import slugify, smart_text


u = u'Ελληνικά'


def test_slugify():
    x = '-'.join([u, u])
    y = ' - '.join([u, u])

    def check(x, y):
        eq_(slugify(x), y)

    def check_replace_latin(x, y):
        eq_(slugify(x, replace_latin=True), y)

    def check_replace_latin_capital(x, y):
        eq_(slugify(x, lower=False, replace_latin=True), y)

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

    replace_latin = [(u'Bakıcı geldi', u'bakici-geldi'), (u'Bäuma means tree', u'bauma-means-tree')]

    replace_latin_capital = [(u'BÄUMA MEANS TREE', u'BAUMA-MEANS-TREE'),
                             (u'EMİN WAS HERE', u'EMIN-WAS-HERE')]

    for val, expected in s:
        yield check, val, expected

    for val, expected in replace_latin:
        yield check_replace_latin, val, expected

    for val, expected in replace_latin_capital:
        yield check_replace_latin_capital, val, expected


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