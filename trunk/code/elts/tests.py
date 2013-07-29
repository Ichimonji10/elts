"""Unit tests for this django app.

``django.utils.unittest`` is an alias for Django's bundled copy of unittest2,
backported for Python 2.5 compatibility. If you have Python2.7 (ergo unittest2)
installed already, that will be used instead. Further, "``django.test.TestCase``
[...] is a subclass of ``unittest.TestCase`` that runs each test inside a
transaction to provide isolation".

For details on Django's testing tools, see:
https://docs.djangoproject.com/en/1.5/topics/testing/overview/#writing-tests

Each class in this module typically contains tests for only one URI. For
example, a class might test just /index or /item/create-form.

"""
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import unittest
from elts import factories
from elts import forms
import doctest
import string
import random

def _login(client):
    """Create a user and use it to log in ``client``."""
    user, password = factories.create_user()
    return client.login(username = user.username, password = password)

def _test_logout(instance):
    """Logout, then GET ``instance.URI``.
    
    ``instance`` is an instance of a ``TestCase`` subclass. In other words, a
    caller typically passes ``self`` to this method.

    """
    instance.client.logout()
    response = instance.client.get(instance.URI)
    target = string.join([
        reverse('elts.views.login'),
        '?'
        'next={}'.format(instance.URI),
    ], '')
    instance.assertRedirects(response, target)

class IndexTestCase(TestCase):
    """Tests for the ``/`` URI.

    The ``/`` URI is reachable through the 'elts.views.index' function.

    """
    URI = reverse('elts.views.index')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class CalendarTestCase(TestCase):
    """Tests for the ``calendar/`` URI.

    The ``calendar/`` URI is reachable through the 'elts.views.calendar'
    function.

    """
    URI = reverse('elts.views.calendar')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class ItemTestCase(TestCase):
    """Tests for the ``item/`` URI.

    The ``item/`` URI is available through elts.views.item.

    """
    URI = reverse('elts.views.item')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post_failure(self):
        """POSTs ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(
            response,
            reverse('elts.views.item_create_form')
        )

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class ItemCreateFormTestCase(TestCase):
    """Tests for the ``item/create-form/`` URI.

    The ``item/create-form/`` URI is available through
    elts.views.item_create_form.

    """
    URI = reverse('elts.views.item_create_form')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class ItemNoteTestCase(TestCase):
    """Tests for the ``item-note/`` URI.

    The ``item-note/`` URI is available through 'elts.views.item_note'.

    """
    URI = reverse('elts.views.item_note')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post_failure(self):
        """POSTs ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertEqual(response.status_code, 422)

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class LoginTestCase(TestCase):
    """Tests for the the ``login/`` URI.

    The ``login/`` URI is reachable through the 'elts.views.login' function.

    """
    URI = reverse('elts.views.login')

    def test_post(self):
        """POSTs ``self.URI``."""
        user, password = factories.create_user()
        response = self.client.post(
            self.URI,
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_post_failure(self):
        """POSTs ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(response, self.URI)

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI, {})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        _login(self.client)
        response = self.client.delete(self.URI)
        self.assertRedirects(response, self.URI)

    def test_delete_via_post(self):
        """DELETEs ``self.URI`` via a POST request."""
        _login(self.client)
        response = self.client.post(
            self.URI,
            {'method_override': 'DELETE'}
        )
        self.assertRedirects(response, self.URI)

    def test_login(self):
        """Tests ``self.client.login()``."""
        user, password = factories.create_user()
        self.assertTrue(
            self.client.login(username = user.username, password = password)
        )

    def test__login(self):
        """Test ``_login()``."""
        self.assertTrue(_login(self.client))

class TagTestCase(TestCase):
    """Tests for the ``tag/`` URI.

    The ``tag/`` URI can be reached through 'elts.views.tag'

    """
    URI = reverse('elts.views.tag')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post_failure(self):
        """POSTs ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(
            response,
            reverse('elts.views.tag_create_form')
        )

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class TagCreateFormTestCase(TestCase):
    """Tests for the ``tag/create-form/`` URI.

    The ``tag/create-form/`` URI can be reached through
    'elts.views.tag_create_form'.

    """
    URI = reverse('elts.views.tag_create_form')

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.URI``."""
        response = self.client.put(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.URI``."""
        response = self.client.delete(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_logout(self):
        """Calls ``_test_logout()``."""
        _test_logout(self)

class ItemFormTestCase(TestCase):
    """Tests for ``ItemForm``."""
    @classmethod
    def _name(self):
        """Returns a value for the ``name`` form field."""
        return factories.random_utf8_str(1, 50)

    @classmethod
    def _description(self):
        """Returns a value for the ``description`` form field."""
        return factories.random_utf8_str(1, 2000)

    @classmethod
    def _is_lendable(self):
        """Returns a value for the ``is_lendable`` form field."""
        return random.choice([True, False])

    @classmethod
    def _tags(self):
        """Returns a value for the ``tags`` form field."""
        random.choice([1, 2, 3])

    def test_valid(self):
        """Creates a valid ItemForm."""
        form = forms.ItemForm({'name': self._name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Creates an ItemForm without setting ``name``."""
        form = forms.ItemForm({})
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Creates an ItemForm and sets ``description``."""
        form = forms.ItemForm({
            'name': self._name(),
            'description': self._description()
        })
        self.assertTrue(form.is_valid())

    def test_has_is_lendable(self):
        """Creates an ItemForm and sets ``is_lendable``."""
        form = forms.ItemForm({
            'name': self._name(),
            'is_lendable': self._is_lendable()
        })
        self.assertTrue(form.is_valid())

    def test_has_tags(self):
        """Creates an ItemForm and sets ``tags``."""
        form = forms.ItemForm({
            'name': self._name(),
            'tags': self._tags()
        })
        self.assertTrue(form.is_valid())

class TagFormTestCase(TestCase):
    """Tests for ``TagForm``."""
    @classmethod
    def _name(self):
        """Returns a value for the ``name`` form field."""
        return factories.random_utf8_str(1, 30)

    @classmethod
    def _description(self):
        """Returns a value for the ``description`` form field."""
        return factories.random_utf8_str(1, 2000)

    def test_valid(self):
        """Creates a valid TagForm."""
        form = forms.TagForm({'name': self._name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Creates a TagForm without setting ``name``."""
        form = forms.TagForm({})
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Creates a TagForm and sets ``description``."""
        form = forms.TagForm({
            'name': self._name(),
            'description': self._description()
        })

# FIXME: move test definitions to view_tests.py and form_tests.py as
# appropriate.
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(IndexTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(CalendarTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ItemTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ItemCreateFormTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ItemNoteTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoginTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TagTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TagCreateFormTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ItemFormTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TagFormTestCase))
    suite.addTest(doctest.DocTestSuite(factories))
    return suite
