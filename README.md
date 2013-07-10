# Unicode Slugify

Unicode Slugify is a slugifier that generates unicode slugs.  It was originally
used in the Firefox Add-ons web site to generate slugs for add-ons and add-on
collections.  Many of these add-ons and collections had unicode characters and
required more than simple transliteration.

## Usage
```python
>>> import slugify
>>> slugify.slugify(u'Bän...g (bang)')
u'bäng-bang'
```
