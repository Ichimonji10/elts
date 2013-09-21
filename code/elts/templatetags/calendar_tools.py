"""Tools for displaying information in a calendar."""
from django.template import Library

# A function decorated with @register.filter can be used as a filter.
register = Library() # pylint: disable=C0103

@register.filter
def calendar_title(date):
    """Return a string which can be used as a calendar title.

    ``date`` is a ``datetime.date`` object.

    >>> from datetime import date
    >>> calendar_title(date(2013, 01, 01))
    'January 2013'

    """
    return date.strftime("%B %Y")
