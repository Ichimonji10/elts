"""Tools for manipulating models."""
from django.template import Library
from django.db.models.fields import FieldDoesNotExist

# Functions decorated with @register.filter can be used as filters.
register = Library() # pylint: disable=C0103

@register.filter
def label(model, field_name):
    """Return the ``verbose_name`` of ``model``'s ``field_name``.

    ``model`` is an instance of a model.

    ``field_name`` is the name of a field defined on that model.

    """
    try:
        return model._meta.get_field(field_name).verbose_name
    except FieldDoesNotExist:
        return ''
