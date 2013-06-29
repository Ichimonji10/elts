"""Data models at the core of ELTS.

`manage.py` can be used to generate a diagram of the tables defined herein. See
the readme for details.

If a model does not specify a primary key, django automatically generates a
column named `id`. Django will not generate `id` if you pass `primary_key =
True` to some other column.

"""
from django.db import models

# pylint: disable=R0903
# "Too few public methods (0/2)" 
# It is both common and OK for a model to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method" 
# It is both common and OK for a model to have no __init__ method.

class Item(models.Model):
    """An item which can be lent out to a person.

    If an item is unavailable for normal use (e.g. a laptop's screen is broken),
    ``is_lendable`` should be marked as false.

    """
    name = models.CharField(max_length = 50, db_index = True)
    description = models.TextField(max_length = 2000, blank = True)
    tags = models.ManyToManyField('Tag', blank = True)
    is_lendable = models.BooleanField(default = True)

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return self.name

class Lend(models.Model):
    """Tracks the lending of an item to a person.

    This model tracks the following pieces of information:
    
    * To whom should an item be lent out?
    * Which item is being lent out?
    * When does the item go out?
    * When does the item come back?
    * When is an item scheduled to go out? (optional)
    * When is an item scheduled to come back? (optional)

    """
    item_id = models.ForeignKey('Item')
    person_id = models.ForeignKey('Person')
    out_reservation = models.DateField(blank = True)
    out_actual = models.DateTimeField(blank = True)
    back_reservation = models.DateField(blank = True)
    back_actual = models.DateTimeField(blank = True)

class Tag(models.Model):
    """A one-word description of an item. For example: "laptop"

    Tags are related to Items via a many-to-many relationship. Here, the
    ``Item`` class contains the relevant declaration. See:
    https://docs.djangoproject.com/en/dev/topics/db/models/#many-to-many-relationships

    """
    name = models.CharField(max_length = 30, unique = True) # implies db_index
    description = models.TextField(max_length = 2000, blank = True)

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return self.name

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
    )
    full_name = models.CharField(max_length = 50, blank = True)
    email = models.CharField(max_length = 50, blank = True)
    # Can a CharField properly handle an AD GUID? GUIDs can have *any* value,
    # and the UTF-8 characterset may not be able to represent every possible
    # value. Some 16-byte (128-bit) long binary representation would be better.

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return self.full_name

class Note(models.Model):
    """A note about _something_.

    This model is abstract. A child class (say, ``ItemNote``) should include a
    foreign key (say, ``item_id``) pointing to some other table (say, ``Item``).

    The funny looking value for ``related_name`` allows reverse queries to be
    performed on ``Person`` objects. For example:

        Person.elts_<child_class_name>_set.all()

    See also:
    https://docs.djangoproject.com/en/dev/topics/db/models/#meta-inheritance
    https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects

    ``auto_now_add`` is useful for automatic creation timestamps. See:
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField

    """
    note_text = models.TextField(max_length = 5000)
    note_date = models.DateTimeField(auto_now_add = True)
    # FIXME
    #author_id = models.ForeignKey(
    #    'Person',
    #    related_name = '%(app_label)s_%(class)s_set',
    #)

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        if 80 >= len(str(self.note_text)):
            return self.note_text
        else:
            return u'{}...'.format(str(self.note_text)[0:77])

    class Meta:
        """Make this model abstract."""
        abstract = True

class ItemNote(Note):
    """A note about an ``Item``."""
    item_id = models.ForeignKey('Item')

class PersonNote(Note):
    """A note about an ``Person``."""
    person_id = models.ForeignKey('Person')

class LendNote(Note):
    """A note about an ``Lend``."""
    lend_id = models.ForeignKey('Lend')
    is_complaint = models.BooleanField(default = False)
