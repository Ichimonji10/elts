"""Data models at the core of ELTS."""
from django.db import models

# Model reference: https://docs.djangoproject.com/en/dev/ref/models/fields/
#
# The database tables are laid out as follows:
#
# Item-----+-------+------------+
# |        |       |            |
# ItemTag  Lend    Reservation  Note
# |        |       |            |
# Tag      Person--+------------+
#
# The classes below are laid out in accordance with the diagram, from left to
# right, then from top to bottom.

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
    description = models.TextField(blank = True)
    due_back_date = models.DateField(blank = True)

class ItemTag(models.Model):
    """Junction table relating items and tags."""
    item_id = models.ForeignKey('Item', to_field = 'id', primary_key = True)
    tag_id = models.ForeignKey('Tag',  to_field = 'id', primary_key = True)

class Lend(models.Model):
    """Tracks the lending of an item to a person."""
    id = models.AutoField(primary_key=True)
    datetime_out = models.DateTimeField()
    datetime_in = models.DateTimeField(blank = True)
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
    note_text = models.TextField()
    item_id = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid = models.ForeignKey('Person', to_field = 'ad_guid')

class Tag(models.Model):
    """A categorization for an item. (e.g. "laptop")"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30, unique = True) # implies db_index

class Person(models.Model):
    """A person.

    Items can be lent to or reserved for a person.

    The canonical source of information about people is an active directory
    server. However, for performance reasons, some information should be
    cached. That information is cached here.

    """
    ad_guid = models.CharField(max_length = 16, primary_key = True)
    full_name = models.CharField(max_length = 50, blank = True)
    email = models.CharField(max_length = 50, blank = True)
    # Can a CharField properly handle an AD GUID? GUIDs can have *any* value,
    # and the UTF-8 characterset may not be able to represent every possible
    # value. Some 16-byte (128-bit) long binary representation would be better.
