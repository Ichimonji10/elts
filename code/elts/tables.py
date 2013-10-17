"""django-tables2 class definitions.

django-tables2 can be used to generate HTML tables from data sets. Those tables
can then be displayed in templates. See:
https://github.com/bradleyayers/django-tables2

"""
import django_tables2 as tables
from elts import models

class LendTable(tables.Table):
    """A table of Lend objects."""
    class Meta(object):
        """Table attributes that are not fields."""
        model = models.Lend

class ItemTable(tables.Table):
    """A table of Item objects."""
    class Meta(object):
        """Table attributes that are not fields."""
        model = models.Item

class TagTable(tables.Table):
    """A table of Tag objects."""
    class Meta(object):
        """Table attributes that are not fields."""
        model = models.Tag
