from django.db import models

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

class Item(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length = 50, db_index = True)
    description     = models.TextField()
    due_back_date   = models.DateField()

class ItemTag(models.Model):
    item_id = models.ForeignKey('Item', to_field = 'id')
    tag_id  = models.ForeignKey('Tag',  to_field = 'id')

class Lend(models.Model):
    id              = models.AutoField(primary_key=True)
    datetime_out    = models.DateTimeField()
    datetime_in     = models.DateTimeField()
    item_id         = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid  = models.ForeignKey('Person', to_field = 'ad_guid')

class Reservation(models.Model):
    id              = models.AutoField(primary_key=True)
    date_in         = models.DateField()
    date_out        = models.DateField()
    item_id         = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid  = models.ForeignKey('Person', to_field = 'ad_guid')

class Note(models.Model):
    id              = models.AutoField(primary_key=True)
    note_date       = models.DateTimeField()
    note_text       = models.TextField()
    item_id         = models.ForeignKey('Item', to_field = 'id')
    person_ad_guid  = models.ForeignKey('Person', to_field = 'ad_guid')

class Tag(models.Model):
    id      = models.AutoField(primary_key=True)
    name    = models.CharField(max_length = 30, unique = True);

class Person(models.Model):
    ad_guid     = models.CharField(max_length = 16, primary_key = True)
    full_name   = models.CharField(max_length = 50);
    email       = models.CharField(max_length = 50);
    # Can a CharField properly handle an AD GUID? GUIDs can have *any* value,
    # and the UTF-8 characterset may not be able to represent every possible
    # value. Some 16-byte (128-bit) long binary representation would be better.
