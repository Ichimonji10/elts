"""Tools for displaying tag information in templates."""
from django.core import urlresolvers
from django import template
from elts import models

register = template.Library()

@register.filter
def item_tags(item):
    """Returns ``item``'s tags as a list."""
    return models.Tag.objects.filter(item__id = item.id)

@register.filter
def tag_link(tag):
    """Returns URI for the given ``tag``.

    Sample output:

        '<a href="/elts/tag/15">daft</a>'

    """
    return '<a href="{}">{}</a>'.format(
        urlresolvers.reverse(
            'elts.views.tag_id',
            args = [tag.id],
        ),
        tag.name,
    )

@register.filter
def tag_items(tag):
    """Returns ``tag``'s items as a list."""
    return models.Item.objects.filter(tags__id = tag.id)

@register.filter
def item_link(item):
    """Returns URI for the given ``item``.

    Sample output:

        '<a href="/elts/item/15">daft</a>'

    """
    return '<a href="{}">{}</a>'.format(
        urlresolvers.reverse(
            'elts.views.item_id',
            args = [item.id],
        ),
        item.name,
    )
