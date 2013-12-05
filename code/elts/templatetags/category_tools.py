"""Tools for inspecting ``Category`` model objects in templates."""
from django.template import Library
from elts import models

# A function decorated with @register.filter can be used as a filter.
register = Library() # pylint: disable=C0103

@register.filter
def category_tags(category):
    """Return ``category``'s tags as a list.

    >>> from elts import factories
    >>> from elts.models import Tag
    >>> category = factories.CategoryFactory.create(
    ...     tags = factories.category_tags()
    ... )
    >>> tags = category_tags(category)
    >>> if len(tags) > 0:
    ...     isinstance(tags[0], Tag)
    ... else:
    ...     True
    True

    """
    return models.Tag.objects.filter(category__exact = category) # pylint: disable=E1101

# FIXME: write doctests
@register.filter
def category_items_total(category):
    return models.Item.objects.filter(tags__category__exact = category).count() # pylint: disable=E1101

# FIXME: write doctests
@register.filter
def category_items_available(category):
    return 'FIXME'

# FIXME: write doctests
@register.filter
def category_next_out(category):
    return 'FIXME'

# FIXME: write doctests
@register.filter
def category_next_back(category):
    return 'FIXME'
