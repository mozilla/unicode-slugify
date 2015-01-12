# Unicode Slugify

Unicode Slugify is a slugifier that generates unicode slugs.  It was originally
used in the Firefox Add-ons web site to generate slugs for add-ons and add-on
collections.  Many of these add-ons and collections had unicode characters and
required more than simple transliteration.

## Usage

    >>> import slugify

    >>> slugify.slugify(u'Bän...g (bang)')
    u'bäng-bang'

    >>> slugify.slugify(u'Bäuma means a tree', replace_latin=True)
    u'bauma-means-a-tree'

    >>> slugify(u'Bakıcı geldi', replace_latin=True)
    u'bakici-geldi'

