"""django-tables2 class definitions.

django-tables2 can be used to generate HTML tables from data sets. Those tables
can then be displayed in templates. See:
https://github.com/bradleyayers/django-tables2

"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from elts import models
import django_tables2 as tables

def _read_url(resource, resource_id):
    """Generate the path for reading ``resource`` number ``resource_id``.

    >>> import re
    >>> None != re.search(r'/item/1234/$', _read_url('item', 1234))
    True

    """
    return reverse(
        'elts.views.{}_id'.format(resource),
        args = [resource_id]
    )

def _update_url(resource, resource_id):
    """Generate the path for updating ``resource`` number ``resource_id``.

    >>> import re
    >>> None != re.search(
    ...     r'/item/1234/update-form/$',
    ...     _update_url('item', 1234)
    ... )
    True

    """
    return reverse(
        'elts.views.{}_id_update_form'.format(resource),
        args = [resource_id]
    )

def _delete_url(resource, resource_id):
    """Generate the path for deleting ``resource`` number ``resource_id``.

    >>> import re
    >>> None != re.search(
    ...     r'/item/1234/delete-form/$',
    ...     _delete_url('item', 1234)
    ... )
    True

    """
    return reverse(
        'elts.views.{}_id_delete_form'.format(resource),
        args = [resource_id]
    )

def _restful_links(resource, resource_id):
    """Generate links for reading, updating and deleting ``resource`` number
    ``resource_id``.

    """
    return \
        '<a href="{}">View</a> - ' \
        '<a href="{}">Edit</a> - ' \
        '<a href="{}">Delete</a>'.format(
            _read_url(resource, resource_id),
            _update_url(resource, resource_id),
            _delete_url(resource, resource_id),
        )

class LendTable(tables.Table):
    """An HTML table displaying ``Lend`` objects.

    The ``actions`` column contains links for reading, updating and deleting
    ``Lend`` objects.

    """
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Non-column table attributes."""
        model = models.Lend

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` represents a row of data from the database (and,
        consequently, a row in the table).

        """
        return mark_safe(_restful_links('lend', record.id))

class ItemTable(tables.Table):
    """An HTML table displaying ``Item`` objects.

    The ``actions`` column contains links for reading, updating and deleting
    ``Item`` objects.

    """
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Non-column table attributes."""
        model = models.Item

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` represents a row of data from the database (and,
        consequently, a row in the table).

        """
        return mark_safe(_restful_links('item', record.id))

class TagTable(tables.Table):
    """An HTML table displaying ``Tag`` objects.

    The ``actions`` column contains links for reading, updating and deleting
    ``Tag`` objects.

    """
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Non-column table attributes."""
        model = models.Tag

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` represents a row of data from the database (and,
        consequently, a row in the table).

        """
        return mark_safe(_restful_links('tag', record.id))
