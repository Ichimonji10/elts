"""django-tables2 class definitions.

django-tables2 can be used to generate HTML tables from data sets. Those tables
can then be displayed in templates. See:
https://github.com/bradleyayers/django-tables2

"""
from django.core.urlresolvers import reverse
from elts import models
import django_tables2 as tables
from django.utils.safestring import mark_safe

class LendTable(tables.Table):
    """A table of Lend objects."""
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not fields."""
        model = models.Lend

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` is 'the entire record for the row from the table data.' In
        other words, ``record`` represents a row of data from the database.

        """
        return mark_safe(
            '<a href="{}">View</a> - '
            '<a href="{}">Edit</a> - '
            '<a href="{}">Delete</a>'.format(
            reverse('elts.views.lend_id', args = [record.id]),
            reverse('elts.views.lend_id_update_form', args = [record.id]),
            reverse('elts.views.lend_id_delete_form', args = [record.id]),
        ))

class ItemTable(tables.Table):
    """A table of Item objects."""
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not fields."""
        model = models.Item

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` is 'the entire record for the row from the table data.' In
        other words, ``record`` represents a row of data from the database.

        """
        return mark_safe(
            '<a href="{}">View</a> - '
            '<a href="{}">Edit</a> - '
            '<a href="{}">Delete</a>'.format(
            reverse('elts.views.item_id', args = [record.id]),
            reverse('elts.views.item_id_update_form', args = [record.id]),
            reverse('elts.views.item_id_delete_form', args = [record.id]),
        ))

class TagTable(tables.Table):
    """A table of Tag objects."""
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not fields."""
        model = models.Tag

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` is 'the entire record for the row from the table data.' In
        other words, ``record`` represents a row of data from the database.

        """
        return mark_safe(
            '<a href="{}">View</a> - '
            '<a href="{}">Edit</a> - '
            '<a href="{}">Delete</a>'.format(
            reverse('elts.views.tag_id', args = [record.id]),
            reverse('elts.views.tag_id_update_form', args = [record.id]),
            reverse('elts.views.tag_id_delete_form', args = [record.id]),
        ))
