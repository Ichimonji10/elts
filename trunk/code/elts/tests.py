"""Unit tests for this django app.

``django.utils.unittest`` is an alias for Django's bundled copy of unittest2,
backported for Python 2.5 compatibility. If you have Python2.7 (ergo unittest2)
installed already, that will be used instead. Further, "``django.test.TestCase``
[...] is a subclass of ``unittest.TestCase`` that runs each test inside a
transaction to provide isolation".

For details, see:
https://docs.djangoproject.com/en/1.5/topics/testing/overview/#writing-tests

"""
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import unittest
from elts import factories
import doctest

def _login(client):
    """Create a user and use it to log in ``client``."""
    user, password = factories.create_user()
    return client.login(username = user.username, password = password)

class IndexTestCase(TestCase):
    """Tests for the ``/`` URI.

    The ``/`` URI is reachable through the 'elts.views.index' function.

    """
    FUNCTION = 'elts.views.index'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.FUNCTION``."""
        response = self.client.post(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

class CalendarTestCase(TestCase):
    """Tests for the ``calendar/`` URI.

    The ``calendar/`` URI is reachable through the 'elts.views.calendar'
    function.

    """
    FUNCTION = 'elts.views.calendar'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.FUNCTION``."""
        response = self.client.post(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

class ItemTestCase(TestCase):
    """Tests for the ``item/`` URI.

    The ``item/`` URI is available through elts.views.item.

    """
    FUNCTION = 'elts.views.item'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post_failure(self):
        """POSTs ``self.FUNCTION``, incorrectly."""
        response = self.client.post(reverse(self.FUNCTION), {})
        self.assertRedirects(
            response,
            reverse('{}_create_form'.format(self.FUNCTION))
        )

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

class ItemCreateFormTestCase(TestCase):
    """Tests for the ``item/create-form/`` URI.

    The ``item/create-form/`` URI is available through
    elts.views.item_create_form.

    """
    FUNCTION = 'elts.views.item_create_form'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.FUNCTION``."""
        response = self.client.post(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

class ItemNoteTestCase(TestCase):
    """Tests for the ``item-note/`` URI.

    The ``item-note/`` URI is available through 'elts.views.item_note'.

    """
    FUNCTION = 'elts.views.item_note'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post_failure(self):
        """POSTs ``self.FUNCTION``, incorrectly."""
        response = self.client.post(reverse(self.FUNCTION), {})
        self.assertEqual(response.status_code, 422)

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

class LoginTestCase(TestCase):
    """Tests for the the ``login/`` URI.

    The ``login/`` URI is reachable through the 'elts.views.login' function.

    """
    FUNCTION = 'elts.views.login'

    def test_post(self):
        """POSTs ``self.FUNCTION``."""
        user, password = factories.create_user()
        response = self.client.post(
            reverse(self.FUNCTION),
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_post_failure(self):
        """POSTs ``self.FUNCTION``, incorrectly."""
        response = self.client.post(reverse(self.FUNCTION), {})
        self.assertRedirects(response, reverse(self.FUNCTION))

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION), {})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        _login(self.client)
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertRedirects(response, reverse(self.FUNCTION))

    def test_delete_via_post(self):
        """DELETEs ``self.FUNCTION`` via a POST request."""
        _login(self.client)
        response = self.client.post(
            reverse(self.FUNCTION),
            {'method_override': 'DELETE'}
        )
        self.assertRedirects(response, reverse(self.FUNCTION))

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
    FUNCTION = 'elts.views.tag'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post_failure(self):
        """POSTs ``self.FUNCTION``, incorrectly."""
        response = self.client.post(reverse(self.FUNCTION), {})
        self.assertRedirects(
            response,
            reverse('{}_create_form'.format(self.FUNCTION))
        )

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

class TagCreateFormTestCase(TestCase):
    """Tests for the ``tag/create-form/`` URI.

    The ``tag/create-form/`` URI can be reached through
    'elts.views.tag_create_form'.

    """
    FUNCTION = 'elts.views.tag_create_form'

    def setUp(self):
        """Authenticates the client before each test."""
        _login(self.client)

    def test_post(self):
        """POSTs ``self.FUNCTION``."""
        response = self.client.post(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GETs ``self.FUNCTION``."""
        response = self.client.get(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUTs ``self.FUNCTION``."""
        response = self.client.put(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETEs ``self.FUNCTION``."""
        response = self.client.delete(reverse(self.FUNCTION))
        self.assertEqual(response.status_code, 405)

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
    suite.addTest(doctest.DocTestSuite(factories))
    return suite
