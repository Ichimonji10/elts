"""Tools for inspecting ``Category`` model objects in templates."""
from django.utils.timezone import utc
from datetime import date, datetime
from django.db.models import Q
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
def count(queryset):
    return queryset.count()

@register.filter
def category_items(category):
    """Return all items that belong to Category ``category``.

    Only items that have *all* of the tags in ``category`` are returned.

    >>> from elts import factories
    >>> item1 = factories.ItemFactory.create()
    >>> item2 = factories.ItemFactory.create()
    >>> item3 = factories.ItemFactory.create()
    >>> tag1 = factories.TagFactory.create()
    >>> tag2 = factories.TagFactory.create()
    >>> item1.tags.add(tag1, tag2)
    >>> item2.tags.add(tag1)
    >>> category_t1  = factories.CategoryFactory.create(tags = [tag1])
    >>> category_t2  = factories.CategoryFactory.create(tags = [tag2])
    >>> category_t12 = factories.CategoryFactory.create(tags = [tag1, tag2])
    >>> set(category_items(category_t1)) == set(item1, item2)
    True
    >>> set(category_items(category_t2)) == set(item1)
    True
    >>> set(category_items(category_t12)) == set(item1)
    True

    """
    # FIXME: this query returns all items that have ANY category tags, not ALL
    # category tags
    return models.Item.objects.filter(
        tags__category__exact = category
    ).distinct()

# FIXME: write doctests
def _lends(items):
    return models.Lend.objects.filter(item_id__in = items)

# FIXME: write doctests
@register.filter
def items_available(items):
    now = datetime.utcnow().replace(tzinfo = utc)
    conflicting_lends = _lends(items).filter(
        # Find lends where either of the following holds true.
        (
            # `out` and `back` are set and `now` occurs between those datetimes.
            Q(out__isnull = False) &
            Q(back__isnull = False) &
            Q(out__lte = now) &
            Q(back__gte = now)
        ) | (
            # Only `out` is set and `now` occurs after that datetime.
            Q(out__isnull = False) &
            Q(back__isnull = True) &
            Q(out__lte = now)
        )
    )
    return items.exclude(lend__in = conflicting_lends).count()

# FIXME: write doctests
@register.filter
def category_next_due_out(category):
    lend = _lends(category_items(category)).filter(
        due_out__gte = date.today()
    ).order_by('due_out').first()
    if lend is None:
        return 'n/a'
    else:
        return lend.due_out

# FIXME: write doctests
@register.filter
def category_next_due_back(category):
    lend = _lends(category_items(category)).filter(
        due_back__gte = date.today()
    ).order_by('due_back').first()
    if lend is None:
        return 'n/a'
    else:
        return lend.due_back
