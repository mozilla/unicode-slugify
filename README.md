# Unicode Slugify

Unicode Slugify is a slugifier that generates unicode slugs.  It was originally
used in the Firefox Add-ons web site to generate slugs for add-ons and add-on
collections.  Many of these add-ons and collections had unicode characters and
required more than simple transliteration.

## Usage

    >>> import slugify

    >>> slugify.slugify(u'Bän...g (bang)')
    u'bäng-bang'

### Replacing SlugField in Django

    from django.core.exceptions import ValidationError
    from django.db.models.fields import SlugField
    from django.forms.fields import CharField
    from slugify import slugify
    
    
    def validate_slug(value):
        s = slugify(value)
        if value != s:
            raise ValidationError("Invalid slug. Suggestion: %s", params=(s,), code='error')
    
    
    class UnicodeSlugFormField(CharField):
        default_validators = [validate_slug]
    
        def clean(self, value):
            value = self.to_python(value).strip()
            return super(UnicodeSlugFormField, self).clean(value)
    
    
    class UnicodeSlugField(SlugField):
        default_validators = [validate_slug]
    
        def formfield(self, **kwargs):
            defaults = {'form_class': UnicodeSlugFormField}
            defaults.update(kwargs)
            return super(UnicodeSlugField, self).formfield(**defaults)
