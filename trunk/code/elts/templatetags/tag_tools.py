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
def item_tags_as_links(item):
    """Returns ``item``'s tags as a comma-separated, hyperlinked list.

    Each element of the returned list is an HTML <a> tag. For example:

        [
            '<a href="/elts/tag/15">daft</a>',
            '<a href="/elts/tag/20">furry</a>',
        ]

    """
    tags = models.Tag.objects.filter(item__id = item.id)
    return [
        '<a href="{}">{}</a>'.format(
            urlresolvers.reverse(
                'elts.views.tag_id',
                args = [tag.id],
            ),
            tag.name,
        )
        for tag
        in tags
    ]

@register.filter
def tag_items(tag):
    """Returns ``tag``'s items as a list."""
    return models.Item.objects.filter(tags__id = tag.id)

@register.filter
def tag_items_as_links(tag):
    """Returns ``tag``'s items as a comma-separated, hyperlinked list.

    Each element of the returned list is an HTML <a> tag. For example:

        [
            '<a href="/elts/item/15">sportscar</a>',
            '<a href="/elts/item/20">penguin</a>',
        ]

    """
    items = models.Item.objects.filter(tags__id = tag.id)
    return [
        '<a href="{}">{}</a>'.format(
            urlresolvers.reverse(
                'elts.views.item_id',
                args = [item.id],
            ),
            item.name,
        )
        for item
        in items
    ]
