"""Unit tests for this django app's views.

The test cases in this module are called from ``tests.py``.

Each test case  in this module tests a single view. For example,
``ItemCreateFormTestCase`` tests just the ``item_create_form`` view.

Each test case is a subclass of ``django.test.TestCase``.
"``django.test.TestCase`` [...] is a subclass of ``unittest.TestCase`` that runs
each test inside a transaction to provide isolation".

"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from elts import factories
import string

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