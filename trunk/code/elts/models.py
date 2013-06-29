"""Data models at the core of ELTS.

``manage.py`` can be used to generate a diagram of the tables defined herein.
See the readme for details.

If a model does not specify a primary key, django automatically generates a
column named ``id``. Django will not generate ``id`` if you pass ``primary_key =
True`` to some other column.

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
    """An item.

    If an item is unavailable for lending (e.g. a laptop's screen is broken),
    ``is_lendable`` should be set to false.

    """
    name = models.CharField(max_length = 50, db_index = True)
    description = models.TextField(max_length = 2000, blank = True)
    tags = models.ManyToManyField('Tag', blank = True)
    is_lendable = models.BooleanField(default = True)

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return self.name

class Lend(models.Model):
    """Tracks the lending of an ``Item`` to a ``User``.

    This model tracks the following pieces of information:
    
    * To whom should an item be lent out?
    * Which item is being lent out?
    * When does the item go out?
    * When does the item come back?
    * When is an item scheduled to go out? (optional)
    * When is an item scheduled to come back? (optional)

    """
    item_id = models.ForeignKey('Item')
    user_id = models.ForeignKey('User')
    out_reservation = models.DateField(blank = True)
    out_actual = models.DateTimeField(blank = True)
    back_reservation = models.DateField(blank = True)
    back_actual = models.DateTimeField(blank = True)

class Tag(models.Model):
    """A descriptive label for an ``Item``.

    Tags are related to Items via a many-to-many relationship. Here, the
    ``Item`` class contains the relevant declaration. See:
    https://docs.djangoproject.com/en/dev/topics/db/models/#many-to-many-relationships

    """
    name = models.CharField(max_length = 30, unique = True) # implies db_index
    description = models.TextField(max_length = 2000, blank = True)

    def __unicode__(self):
        """Used by Python and Django when coercing a model instance to a str."""
        return self.name

# Begin ``User`` model definitions =============================================

class User(models.Model):
    """An ELTS user.

    No data (besides an ``id`` column) is stored in this model, and that is
    intentional. This model exists simply to implement inheritance. This makes
    it possible to, for example, lend an item to a ``User``, regardless of
    exactly which type of ``User`` it is.

    """
    pass

class LocalUser(User):
    """An ELTS user whose info is stored locally."""
    username = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50) # FIXME
    fname = models.CharField(max_length = 50, blank = True)
    lname = models.CharField(max_length = 50, blank = True)
    email = models.CharField(max_length = 50, blank = True)
    telephone = models.CharField(max_length = 50, blank = True) # FIXME

class ActiveDirectoryUser(User):
    """An ELTS user whose info is stored in an Active Directory server."""
    ad_guid = models.CharField(max_length = 128) # FIXME

# Begin ``Note`` model definitions =============================================

class Note(models.Model):
    """An arbitrary note about something.

    This model is abstract, and ``Note`` objects cannot be instantiated
    directly. Instead, more specific child classes should be created. For
    example:

        class ItemNote(Note):
            item_id = ForeignKey('Item')

    The funny looking value for ``related_name`` allows reverse queries to be
    performed on ``User`` objects. For example:

        User.elts_<child_class_name>_set.all()

    See also:
    https://docs.djangoproject.com/en/dev/topics/db/models/#meta-inheritance
    https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects

    ``auto_now_add`` is useful for automatic creation timestamps. See:
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField

    """
    note_text = models.TextField(max_length = 5000)
    note_date = models.DateTimeField(auto_now_add = True)
    author_id = models.ForeignKey(
        'User',
        related_name = '%(app_label)s_%(class)s_set',
    )

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

class UserNote(Note):
    """A note about an ``User``."""
    user_id = models.ForeignKey('User')

class LendNote(Note):
    """A note about an ``Lend``."""
    lend_id = models.ForeignKey('Lend')
    is_complaint = models.BooleanField(default = False)
