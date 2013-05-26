"""Data models at the core of ELTS.

The database tables are laid out as follows::

    Item-----+-------+------------+
    |        |       |            |
    ItemTag  Lend    Reservation  Note
    |        |       |            |
    Tag      Person--+------------+

"""
from django.db import models

# TODO: Flesh out many-to-many relationships by adding ``ManyToManyField``s to
# models.

# pylint: disable=R0903
# "Too few public methods (0/2)" 
# It is both common and OK for a model to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method" 
# It is both common and OK for a model to have no __init__ method.

class Item(models.Model):
    """An item which can be lent out to a person."""
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50, db_index = True)
    description = models.TextField(max_length = 500, blank = True)
    due_back_date = models.DateField(blank = True, null = True)
    tags = models.ManyToManyField('Tag', through = 'ItemTag', blank = True)

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return str(self.name)

class ItemTag(models.Model):
    """Junction table relating items and tags.

    Unfortunately, Django does not support multi-column primary keys. The
    work-around is to specify that the relevant columns should be
    ``unique_together``. More detailed info is available `here`_.

    .. _here: https://docs.djangoproject.com/en/dev/faq/models/#do-django-models-support-multiple-column-primary-keys

    """
    id = models.AutoField(primary_key = True)
    item_id = models.ForeignKey('Item', to_field = 'id')
    tag_id = models.ForeignKey('Tag',  to_field = 'id')

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return "{} <=> {}".format(self.item_id, self.tag_id)

    class Meta:
        unique_together = (('item_id', 'tag_id'),)

class Lend(models.Model):
    """Tracks the lending of an item to a person."""
    id = models.AutoField(primary_key=True)
    datetime_out = models.DateTimeField(verbose_name = 'date and time out')
    datetime_in = models.DateTimeField(
        verbose_name = 'date and time in',
        blank = True,
    )
    item_id = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid = models.ForeignKey('Person', to_field = 'ad_guid')

class Reservation(models.Model):
    """Reserves the lending of an item to a person in the future."""
    id = models.AutoField(primary_key=True)
    date_in = models.DateField()
    date_out = models.DateField()
    item_id = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid = models.ForeignKey('Person', to_field = 'ad_guid')

class Note(models.Model):
    """An arbitrary, descriptive note about an item."""
    id = models.AutoField(primary_key=True)
    note_date = models.DateTimeField()
    note_text = models.TextField(max_length = 5000)
    item_id = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid = models.ForeignKey('Person', to_field = 'ad_guid')

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        if 80 >= len(str(self.note_text)):
            return str(self.note_text)
        else:
            return "{}...".format(str(self.note_text)[0:77])

class Tag(models.Model):
    """A one-word description of an item. For example: "laptop"

    Tags are related to Items via a many-to-many relationship. Here, the
    ``Item`` class contains the relevant declaration. See:
    https://docs.djangoproject.com/en/dev/topics/db/models/#many-to-many-relationships

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30, unique = True) # implies db_index

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return str(self.name)

class Person(models.Model):
    """A person.

    Items can be lent to or reserved for a person.

    The canonical source of information about people is an active directory
    server. However, for performance reasons, some information should be
    cached. That information is cached here.

    """
    ad_guid = models.CharField(
        verbose_name = 'active directory guid',
        max_length = 16,
        primary_key = True,
    )
    full_name = models.CharField(max_length = 50, blank = True)
    email = models.CharField(max_length = 50, blank = True)
    # Can a CharField properly handle an AD GUID? GUIDs can have *any* value,
    # and the UTF-8 characterset may not be able to represent every possible
    # value. Some 16-byte (128-bit) long binary representation would be better.

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return str(self.full_name)
