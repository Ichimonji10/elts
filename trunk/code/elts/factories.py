"""Factory Boy factory definitions.

These factory definitions are used as an alternative to plain old Django
fixtures. Note especially that "All factories for a Django Model should use the
DjangoModelFactory base class." Otherwise, weird failures occur. Read more about
Factory Boy here: http://factoryboy.readthedocs.org/en/latest/

"""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from elts import models
from factory.django import DjangoModelFactory
from factory import Sequence
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
    """Creates a ``django.contrib.auth.models.User`` object.

    The created object has a random username and password. Neither is usable by
    a normal human.

    >>> UserFactory.build().full_clean()
    >>> user = UserFactory.build(
    ...     username = 'user0',
    ...     password = make_password('hackme')
    ... )
    >>> user.full_clean()
    >>> user.username
    'user0'
    >>> user.check_password('hackme')
    True

    """
    FACTORY_FOR = User
    username = Sequence(lambda n: _random_username(n))
    password = make_password(random_utf8_str(20))

def create_user():
    """Build and save a User.

    Returns an array of two objects: a User and a it's unencrypted password.

    >>> user, password = create_user()
    >>> user.check_password(password)
    True
    >>> user.id is None
    False

    """
    password = random_utf8_str(20)
    user = UserFactory.create(password = make_password(password))
    return [user, password]
