"""Tools for displaying tag information in templates."""
from django.core.urlresolvers import reverse
from django.template import Library
from elts import models

register = Library()

@register.filter
def item_tags(item):
    """Returns ``item``'s tags as a list."""
    return models.Tag.objects.filter(item__id = item.id)

@register.filter
def item_notes(item):
    """Returns ``item``'s notes as a list."""
    return models.ItemNote.objects.filter(item_id = item.id)

@register.filter
def tag_link(tag):
    """Returns URI for the given ``tag``.

    Sample output:

        '<a href="/elts/tag/15">daft</a>'

    """
    return '<a href="{}">{}</a>'.format(
        reverse(
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
        reverse(
            'elts.views.item_id',
            args = [item.id],
        ),
        item.name,
    )

@register.filter
def related_tags(item):
    """Returns tags related to, but not used by, ``item``.

    This function compiles a tuple of all tags used by this item. It then finds
    all items which use those tags and compiles a tuple of all of *their* tags.
    All tags used by ``item`` are stripped out, duplicate tags are removed, and
    the tuple of tags is returned.

    """
    # sets are an unordered collection of unique objects
    tags = set(item_tags(item))

    related_items = set()
    for tag in tags:
        related_items = related_items.union(tag_items(tag))

    related_tags = set()
    for related_item in related_items:
        related_tags = related_tags.union(item_tags(related_item))

    return related_tags - tags
