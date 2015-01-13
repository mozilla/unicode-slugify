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
You might want to use unicode-slugify with Django's SlugField.
However, you will be prevented from saving a form with a SlugField (e.g. in the Django Admin) if the field value is invalid by [Django's slug standard](https://github.com/django/django/blob/2e65d56156b622e2393dee1af66e9c799a51924f/django/core/validators.py#L210).

The solution to this is to create a new UnicodeSlugField which inherits most of it's functionality from SlugField,
but overrides the validation.

#### fields.py
This code can technically be placed anywhere in your project,
but placing it in some_app.fields is consistent with the rest of Django.
Then you import UnicodeSlugField in your model and the custom form field should automatically be used in both normal forms and in the Django admin.

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
