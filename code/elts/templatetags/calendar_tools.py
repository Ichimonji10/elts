"""Tools for displaying information in a calendar."""
from django.template import Library
import calendar

# Functions decorated with @register.filter can be used as filters.
register = Library() # pylint: disable=C0103

@register.filter
def month_and_year(date):
    """Return a string stating the month and year.

    ``date`` is a ``datetime.date`` object.

    >>> from datetime import date
    >>> month_and_year(date(2013, 01, 01))
    'January 2013'

    """
    return date.strftime("%B %Y")

@register.filter
def day_names(_calendar):
    # pylint: disable=C0301
    """Return an array of day names.

    ``_calendar`` is a ``calendar.Calendar`` object.

    >>> import calendar
    >>> day_names(calendar.Calendar(0))
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    >>> day_names(calendar.Calendar(1))
    ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday']

    """
    return [
        calendar.day_name[day_number]
        for day_number
        in _calendar.iterweekdays()
    ]
