"""Tools for inspecting ``Category`` model objects in templates."""
from django.template import Library
from elts import models

# A function decorated with @register.filter can be used as a filter.
register = Library() # pylint: disable=C0103

# FIXME: add unit tests
@register.filter
def category_tags(category):
    """Return ``category``'s tags as a list."""
    return models.Tag.objects.filter(category__id = category.id) # pylint: disable=E1101
