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
from datetime import date, datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from elts import models
from factory import Sequence, SubFactory
from factory.compat import UTC
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyAttribute, FuzzyDate, FuzzyDateTime
import random

# See ``_random_username`` for details on why this charset was chosen.
USERNAME_CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_@+.-'

def _random_username(prefix = ''):
    """Generates a random username for a User.

    For details on why usernames are composed from USERNAME_CHARSET, see:
    https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.username

    >>> username = _random_username()
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

def _random_integer(lower, upper):
    """Returns a random integer between ``lower`` and ``upper``, inclusive.

    If ``lower >= upper``, returns ``lower``.

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

def random_utf8_str(min_len = 0, max_len = 0):
    """Returns a string consisting of random UTF-8 characters.

    If ``min_len >= max_len``, returns a string exactly ``min_len`` characters
    long. Otherwise, returns a string between ``min_len`` and ``max_len`` chars
    long, inclusive.

    See also: http://docs.python.org/2/library/functions.html#unichr

    """
    string = ''
    for i in range(_random_integer(min_len, max_len)):
        string += unichr(random.randrange(0, 65535))
    return string

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
    username = Sequence(lambda n: _random_username(n))
    password = FuzzyAttribute(lambda: make_password(random_utf8_str(1, 20)))

def create_user():
    """Build and save a User.

    Returns an array of two objects: a User and a it's unencrypted password.

    >>> user, password = create_user()
    >>> user.check_password(password)
    True
    >>> user.id is None
    False

    """
    # This function promises that it will return an unencrypted password, but an
    # unencrypted password cannot be fetched from a User object. The solution is
    # to make an unencrypted password and _then_ create the User object.
    password = random_utf8_str(1, 20)
    user = UserFactory.create(password = make_password(password))  # pylint: disable=E1101
    return [user, password]

class ItemFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.Item`` object.

    >>> ItemFactory.build().full_clean()
    >>> ItemFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Item
    name = FuzzyAttribute(lambda: random_utf8_str(1, models.Item.MAX_LEN_NAME))

class TagFactory(DjangoModelFactory):
    """Instantiate an ``elts.models.Tag`` object.

    >>> TagFactory.build().full_clean()
    >>> TagFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Tag
    name = FuzzyAttribute(lambda: random_utf8_str(models.Tag.MAX_LEN_NAME))

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
    note_text = FuzzyAttribute(
        lambda: random_utf8_str(models.Note.MAX_LEN_NOTE_TEXT)
    )

# FIXME: Dates are not handled nicely. See docstring.
class LendFactory(DjangoModelFactory):
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
    #
    # Variable assignments within factory classes are interpreted as db column
    # assignments. However, private variables (like ``_lo``) are exempt from
    # this treatment.
    _lo = datetime.min
    _hi = datetime.max
    out = FuzzyDateTime(
        datetime(1900, _lo.month, _lo.day, tzinfo = UTC),
        datetime(2100, _hi.month, _hi.day, tzinfo = UTC)
    )

class FutureLendFactory(LendFactory):
    """An ``elts.models.Lend`` object whose ``due_out`` attribute is set.

    >>> lend = FutureLendFactory.create()
    >>> lend.full_clean()
    >>> lend.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    #
    # Variable assignments within factory classes are interpreted as db column
    # assignments. However, private variables (like ``_lo``) are exempt from
    # this treatment.
    _lo = date.min
    _hi = date.max
    due_out = FuzzyDate(
        date(1900, _lo.month, _lo.day),
        date(2100, _hi.month, _hi.day)
    )

def random_lend_factory():
    """Return a subclass of LendFactory.

    >>> cls = random_lend_factory()
    >>> cls.__name__ in ['PastLendFactory', 'FutureLendFactory']
    True

    """
    return random.choice([PastLendFactory, FutureLendFactory])
