"""Tools for displaying information in a calendar."""
from django.template import Library
from elts import models
import datetime

# Functions decorated with @register.filter can be used as filters.
register = Library() # pylint: disable=C0103

@register.filter
def month_and_year(date_):
    """Return a string stating the month and year.

    ``date_`` is a ``datetime.date`` object.

    >>> from datetime import date
    >>> month_and_year(date(2013, 1, 1))
    'January 2013'

    """
    return date_.strftime("%B %Y")

@register.filter
def day_name_abbrev(date_):
    """Return the abbreviated day name of ``date_``.

    ``date_`` is a ``datetime.date`` object.

    >>> from datetime import date
    >>> for i in range(1, 10):
    ...     day_name_abbrev(date(2013, 1, i))
    ...
    'Tue'
    'Wed'
    'Thu'
    'Fri'
    'Sat'
    'Sun'
    'Mon'
    'Tue'
    'Wed'

    """
    return date_.strftime('%a')

@register.filter
def month_days(date_):
    """Return an iterator for whichever month ``date_`` resides in.

    ``date_`` is a ``datetime.date`` object.

    One ``datetime.date`` object is yielded for each day of the month,
    regardless of when ``date_`` occurs within that month.

    >>> from datetime import date
    >>> sum(1 for _ in month_days(date(2013, 1, 1)))
    31
    >>> sum(1 for _ in month_days(date(2013, 1, 20)))
    31
    >>> sum(1 for _ in month_days(date(2013, 2, 1)))
    28

    """
    day = datetime.date(date_.year, date_.month, 1)
    one_day = datetime.timedelta(days = 1)
    while(day.month == date_.month):
        yield day
        day += one_day

@register.filter
def lends_due_out(date_):
    """Return a QuerySet of lends due out on ``date_``.

    ``date_`` is a ``datetime.date`` object.

    """
    return models.Lend.objects.filter(due_out = date_)

@register.filter
def lends_due_back(date_):
    """Return a QuerySet of lends due back on ``date_``.

    ``date_`` is a ``datetime.date`` object.

    """
    return models.Lend.objects.filter(due_back = date_)
