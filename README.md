# Unicode Slugify

Unicode Slugify is a slugifier that generates unicode slugs.  It was originally
used in the Firefox Add-ons web site to generate slugs for add-ons and add-on
collections. Many of these add-ons and collections had unicode characters and
required more than simple transliteration.

## Usage

```python

from slugify import slugify, SLUG_OK

# Default usage : lower, spaces replaced with "-", only alphanum and "-_~" chars, keeps unicode
slugify(u'Bän...g (bang)')
# u'bäng-bang'

# Keep capital letters and spaces
slugify(u'Bän...g (bang)', lower=False, spaces=True)
# u'Bäng bang'

# Replace non ascii chars with their "best" representation
slugify(u'北京 (capital of China)', only_ascii=True)
# u'bei-jing-capital-of-china'

# Allow some extra chars
slugify(u'北京 (capital of China)', ok=SLUG_OK+'()', only_ascii=True)
# u'bei-jing-(capital-of-china)'

# "snake_case" example
def snake_case(s):
    # As "-" is not in allowed Chars, first one (`_`) is used for space replacement
    return slugify(s, ok='_', only_ascii=True)
snake_case(u'北京 (capital of china)')
# u'bei_jing_capital_of_china'

# "CamelCase" example
def camel_case(s):
    return slugify(s.title(), ok='', only_ascii=True, lower=False)
camel_case(u'北京 (capital of china)')
# u'BeiJingCapitalOfChina'
```

## Thanks

Tomaz Solc, unidecode, https://pypi.python.org/pypi/Unidecode
