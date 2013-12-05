"""Factory Boy factory definitions.

These factory definitions are used as an alternative to plain old Django
fixtures. Rather than simply defining a static set of test data, factories can
be used to generate disgustingly random data. (perfect for testing!)

Notes
=====

"All factories for a Django Model should use the DjangoModelFactory base class."
Otherwise, weird failures will occur. Read the Factory Boy docs here:
http://factoryboy.readthedocs.org/en/latest/

Python 2 does not provide a standard method of tracking timezone data in
datetime objects. Rather than writing a custom implementation of this feature,
the factory_boy implementation of timezone data is used. It's beautiful. See:
* https://github.com/rbarrois/factory_boy/blob/master/factory/compat.py
* http://docs.python.org/2/library/datetime.html

"""
from datetime import date, datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from elts import models
from factory import Sequence, SubFactory, post_generation
from factory.compat import UTC
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyAttribute, FuzzyDate, FuzzyDateTime
import random

# See ``user_username`` for details on why this charset was chosen.
USERNAME_CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_@+.-'

class UserFactory(DjangoModelFactory):
    """Builds a ``django.contrib.auth.models.User`` object.

    The user built has a random username and password. Both the username and
    password consist of a set of UTF-8 characters.

    >>> UserFactory.build().full_clean()
    >>> UserFactory.create().id is None
    False
    >>> UserFactory.build(
    ...     password = make_password('hackme')
    ... ).check_password('hackme')
    True

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = User
    username = Sequence(lambda n: user_username(n)) # pylint: disable=W0108
    password = FuzzyAttribute(lambda: user_password()) # pylint: disable=W0108

def user_username(prefix = ''):
    """Return a value suitable for the ``User.username`` model attribute.

    For details on why usernames are composed from USERNAME_CHARSET, see:
    https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.username

    >>> username = user_username()
    >>> len(username) in range(1, 31)
    True
    >>> username[0] in USERNAME_CHARSET
    True
    >>> username[-1] in USERNAME_CHARSET
    True

    """
    username = str(prefix)
    for i in range(random.randint(1, 30 - len(username))):
        username += random.choice(USERNAME_CHARSET)
    return username

def user_password():
    """Return a value suitable for the ``User.password`` model attribute."""
    return make_password(_random_utf8_str(1, 20))

def create_user():
    """Build and save a User.

    Return an array of two objects: a User and a it's unencrypted password.

    >>> user, password = create_user()
    >>> user.check_password(password)
    True
    >>> user.id is None
    False

    """
    # This function promises that it will return an unencrypted password, but an
    # unencrypted password cannot be fetched from a User object. The solution is
    # to make an unencrypted password and _then_ create the User object.
    password = _random_utf8_str(1, 20)
    user = UserFactory.create(password = make_password(password))  # pylint: disable=E1101
    return [user, password]

#-------------------------------------------------------------------------------

class ItemFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.Item`` object.

    >>> ItemFactory.build().full_clean()
    >>> ItemFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Item
    name = FuzzyAttribute(lambda: item_name()) # pylint: disable=W0108

def item_name():
    """Return a value suitable for the ``Item.name`` model attribute.

    >>> from elts.models import Item
    >>> name = item_name()
    >>> isinstance(name, unicode)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Item.MAX_LEN_NAME
    True

    """
    return _random_utf8_str(1, models.Item.MAX_LEN_NAME)

def item_description():
    """Return a value suitable for the ``Item.description`` model attribute.

    >>> from elts.models import Item
    >>> description = item_description()
    >>> isinstance(description, unicode)
    True
    >>> len(description) >= 1
    True
    >>> len(description) <= Item.MAX_LEN_DESCRIPTION
    True

    """
    return _random_utf8_str(1, models.Item.MAX_LEN_DESCRIPTION)

def item_tags():
    """Return a list of objects for the ``Item.tags`` model attribute.

    >>> from elts.models import Tag
    >>> tags = item_tags()
    >>> isinstance(tags, list)
    True
    >>> if len(tags) > 0:
    ...     isinstance(tags[0], Tag)
    ... else:
    ...     True
    True

    """
    return [
        TagFactory.create()  # pylint: disable=E1101
        for i
        in range(0, random.randint(0, 3)) # upper limit is arbitrary
    ]

def item_is_lendable():
    """Return a value suitable for the ``Item.is_lendable`` model attribute.

    >>> item_is_lendable() in [True, False]
    True

    """
    return random.choice([True, False])

#-------------------------------------------------------------------------------

class TagFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.Tag`` object.

    >>> TagFactory.build().full_clean()
    >>> TagFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Tag
    name = FuzzyAttribute(lambda: tag_name()) # pylint: disable=W0108

def tag_name():
    """Return a value suitable for the ``Tag.name`` model attribute.

    >>> from elts.models import Tag
    >>> name = tag_name()
    >>> isinstance(name, unicode)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Tag.MAX_LEN_NAME
    True

    """
    return _random_utf8_str(1, models.Tag.MAX_LEN_NAME)

def invalid_tag_name():
    """Return a value unsuitable for the ``Tag.name`` model attribute.

    >>> from elts.models import Tag
    >>> name = invalid_tag_name()
    >>> isinstance(name, unicode)
    True
    >>> len(name) == Tag.MAX_LEN_NAME + 1
    True

    """
    return _random_utf8_str(models.Tag.MAX_LEN_NAME + 1)

def tag_description():
    """Return a value suitable for the ``Tag.description`` model attribute.

    >>> from elts.models import Tag
    >>> description = tag_description()
    >>> isinstance(description, unicode)
    True
    >>> len(description) >= 1
    True
    >>> len(description) <= Tag.MAX_LEN_DESCRIPTION
    True

    """
    return _random_utf8_str(1, models.Tag.MAX_LEN_DESCRIPTION)

def invalid_tag_description():
    """Return a value suitable for the ``Tag.description`` model attribute.

    >>> from elts.models import Tag
    >>> description = invalid_tag_description()
    >>> isinstance(description, unicode)
    True
    >>> len(description) == Tag.MAX_LEN_DESCRIPTION + 1
    True

    """
    return _random_utf8_str(models.Tag.MAX_LEN_DESCRIPTION + 1)

#-------------------------------------------------------------------------------

class LendFactory(DjangoModelFactory):
    # pylint: disable=C0301
    """Base attributes for an ``elts.models.Lend`` object.

    Using random data for dates and datetimes can produce exceptions. They
    usually look like this:

        ERROR: test_put (elts.test_views.LendIdTestCase)
        PUT ``self.uri``.
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/srv/http/elts/code/elts/test_views.py", line 844, in test_put
            response = self.client.post(self.uri, data)
          [...]
          File "/usr/lib/python2.7/site-packages/django/utils/timezone.py", line 71, in utcoffset
            if self._isdst(dt):
          File "/usr/lib/python2.7/site-packages/django/utils/timezone.py", line 89, in _isdst
            stamp = _time.mktime(tt)
        ValueError: year out of range

    Or this:

        ERROR: test_get (elts.test_views.LendIdTestCase)
        GET ``self.uri``.
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/srv/http/elts/code/elts/test_views.py", line 837, in test_get
            response = self.client.get(self.uri)
          [...]
          File "/usr/lib/python2.7/site-packages/django/utils/timezone.py", line 223, in template_localtime
            return localtime(value) if should_convert else value
          File "/usr/lib/python2.7/site-packages/django/utils/timezone.py", line 237, in localtime
            value = value.astimezone(timezone)
        OverflowError: date value out of range

    A proper solution is not known at this time, and it is hard to consistently
    produce this error. In the meantime, a simple hack is used: set the lower
    and upper bound for dates to year 1900 and 2100, respectively. This is not
    as ideal as using a value like date.min.year, but it should provide a good
    enough range of test values while still avoiding random exceptions.

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Lend
    ABSTRACT_FACTORY = True
    item_id = SubFactory(ItemFactory)
    user_id = SubFactory(UserFactory)

class PastLendFactory(LendFactory):
    """An ``elts.models.Lend`` object whose ``out`` attribute is set.

    >>> lend = PastLendFactory.create()
    >>> lend.full_clean()
    >>> lend.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    out = FuzzyAttribute(lambda: lend_out()) # pylint: disable=W0108

class FutureLendFactory(LendFactory):
    """An ``elts.models.Lend`` object whose ``due_out`` attribute is set.

    >>> lend = FutureLendFactory.create()
    >>> lend.full_clean()
    >>> lend.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    due_out = FuzzyAttribute(lambda: lend_due_out()) # pylint: disable=W0108

def random_lend_factory():
    """Return a subclass of LendFactory.

    >>> cls = random_lend_factory()
    >>> cls.__name__ in ['PastLendFactory', 'FutureLendFactory']
    True

    """
    return random.choice([PastLendFactory, FutureLendFactory])

def lend_due_out():
    """Return a value suitable for the ``Lend.due_out`` attribute.

    >>> from datetime import date
    >>> isinstance(lend_due_out(), date)
    True

    """
    lower = date.min
    upper = date.max
    return FuzzyDate(
        date(1900, lower.month, lower.day),
        date(2100, upper.month, upper.day)
    ).fuzz()

def lend_due_back():
    """Return a value suitable for the ``Lend.due_back`` attribute.

    >>> from datetime import date
    >>> isinstance(lend_due_back(), date)
    True

    """
    return lend_due_out()

def lend_out():
    """Return a value suitable for the ``Lend.out`` attribute.

    >>> from datetime import datetime
    >>> isinstance(lend_out(), datetime)
    True

    """
    lower = datetime.min
    upper = datetime.max
    return FuzzyDateTime(
        datetime(1900, lower.month, lower.day, tzinfo = UTC),
        datetime(2100, upper.month, upper.day, tzinfo = UTC)
    ).fuzz()

def lend_back():
    """Return a value suitable for the ``Lend.back`` attribute.

    >>> from datetime import datetime
    >>> isinstance(lend_back(), datetime)
    True

    """
    return lend_out()

#-------------------------------------------------------------------------------

class CategoryFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.Category`` object.

    >>> category = CategoryFactory.create()
    >>> category.full_clean()
    >>> category.id is None
    False
    >>> CategoryFactory.create(tags = []).tags.count()
    0

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Category
    user = SubFactory(UserFactory)
    name = FuzzyAttribute(lambda: category_name()) # pylint: disable=W0108

    @post_generation
    def tags(self, create, extracted, **kwargs):
        """Assign a value to the ``Category.tags`` model attribute.

        The ``@post_generation`` decorator ensures that this method is only
        called after the ``create()`` method is called. If an iterable is passed
        to the constructor, its values will be used when populating the ``tags``
        many-to-many relationship. Otherwise, the values returned by
        ``category_tags()`` are used.

        """
        if not create:
            # build() was called. ``self`` has not been saved.
            return
        if extracted is not None:
            for tag in extracted:
                self.tags.add(tag)

def category_name():
    """Return a value for the ``Category.name`` model attribute.

    >>> from elts.models import Category
    >>> name = category_name()
    >>> isinstance(name, unicode)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Category.MAX_LEN_NAME
    True

    """
    return _random_utf8_str(1, models.Category.MAX_LEN_NAME)

# FIXME: The python2.7 JSON encoder doesn't properly handle UTF-8 characters,
# and it will often either mis-count the number of characters in a line or
# thrown an exception. Upgrade to python 3.
def invalid_category_name():
    """Return a value unsuitable for the ``Category.name`` model attribute.

    >>> from elts.models import Category
    >>> name = invalid_category_name()
    >>> isinstance(name, unicode)
    True
    >>> len(name) == Category.MAX_LEN_NAME + 1
    True

    """
    return u'x' * (models.Category.MAX_LEN_NAME + 1)
    #return _random_utf8_str(models.Category.MAX_LEN_NAME + 1)

def category_tags():
    """Return values for the ``Category.tags`` model attribute.

    >>> from elts.models import Tag
    >>> tags = category_tags()
    >>> isinstance(tags, list)
    True
    >>> if len(tags) > 0:
    ...     isinstance(tags[0], Tag)
    ... else:
    ...     True
    True

    """
    return item_tags()

#-------------------------------------------------------------------------------

class ItemNoteFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.ItemNote`` object.

    >>> item_note = ItemNoteFactory.create()
    >>> item_note.full_clean()
    >>> item_note.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.ItemNote
    author_id = SubFactory(UserFactory)
    item_id = SubFactory(ItemFactory)
    note_text = FuzzyAttribute(lambda: note_note_text()) # pylint: disable=W0108

class LendNoteFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.LendNote`` object.

    >>> lend_note = LendNoteFactory.create()
    >>> lend_note.full_clean()
    >>> lend_note.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.LendNote
    author_id = SubFactory(UserFactory)
    lend_id = SubFactory(random_lend_factory())
    note_text = FuzzyAttribute(lambda: note_note_text()) # pylint: disable=W0108

def note_note_text():
    """Return a value suitable for the ``Note.note_text`` model attribute.

    >>> from elts.models import Note
    >>> note = note_note_text()
    >>> isinstance(note, unicode)
    True
    >>> len(note) >= 1
    True
    >>> len(note) <= Note.MAX_LEN_NOTE_TEXT
    True

    """
    return _random_utf8_str(1, models.Note.MAX_LEN_NOTE_TEXT)

# FIXME: The python2.7 JSON encoder doesn't properly handle UTF-8 characters,
# and it will often either mis-count the number of characters in a line or
# thrown an exception. Upgrade to python 3.
def invalid_note_note_text():
    """Return a value suitable for the ``Note.note_text`` model attribute.

    >>> from elts.models import Note
    >>> note = invalid_note_note_text()
    >>> isinstance(note, unicode)
    True
    >>> len(note) == Note.MAX_LEN_NOTE_TEXT + 1
    True

    """
    return u'x' * (models.Note.MAX_LEN_NOTE_TEXT + 1)
    #return _random_utf8_str(models.Note.MAX_LEN_NOTE_TEXT + 1)

def lend_note_is_complaint():
    """Return a value for the ``LendNote.is_complaint()`` model attribute.

    >>> lend_note_is_complaint() in [True, False]
    True

    """
    return random.choice([True, False])

#-------------------------------------------------------------------------------

def _random_integer(lower, upper):
    """Return a random integer between ``lower`` and ``upper``, inclusive.

    If ``lower >= upper``, return ``lower``.

    >>> _random_integer(0, 0)
    0
    >>> _random_integer(5, 5)
    5
    >>> _random_integer(5, 0)
    5
    >>> _random_integer(0, 5) in range(0, 6)
    True

    """
    if(lower >= upper):
        return lower
    return random.randint(0, upper - lower) + lower

def _random_utf8_str(min_len = 0, max_len = 0):
    """Return a string consisting of random UTF-8 characters.

    If ``min_len >= max_len``, return a string exactly ``min_len`` characters
    long. Otherwise, return a string between ``min_len`` and ``max_len`` chars
    long, inclusive.

    See also: http://docs.python.org/2/library/functions.html#unichr

    """
    string = ''
    for i in range(_random_integer(min_len, max_len)):
        string += unichr(random.randrange(0, 65535))
    return string
