# -*- coding: utf-8 -*-
from nose.tools import eq_

from slugify import slugify


u = u'Ελληνικά'


def test_slugify():
    x = '-'.join([u, u])
    y = ' - '.join([u, u])

    def check(x, y):
        eq_(slugify(x), y)
    s = [('xx x  - "#$@ x', 'xx-x-x'),
         (u'Bän...g (bang)', u'bäng-bang'),
         (u, u.lower()),
         (x, x.lower()),
         (y, x.lower()),
         ('    a ', 'a'),
         ('tags/', 'tags'),
         ('holy_wars', 'holy_wars'),
         # I don't really care what slugify returns.  Just don't crash.
         (u'x𘍿', u'x'),
         (u'ϧ΃𘒬𘓣',  u'\u03e7'),
         (u'¿x', u'x'),
    ]
    for val, expected in s:
        yield check, val, expected
