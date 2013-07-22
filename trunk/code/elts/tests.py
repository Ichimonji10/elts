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

class LoginTestCase(TestCase):
    def test_get_login(self):
        """GET the login view."""
        response = self.client.get(reverse('elts.views.login'))
        self.assertEqual(response.status_code, 200)

    def test_post_login(self):
        """POST the login view."""
        password = factories.random_utf8_str(20)
        user = factories.UserFactory.create(password = make_password(password))
        response = self.client.post(
            reverse('elts.views.login'),
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, reverse('elts.views.index'))
        # FIXME: check for presence of user ID
        # FIXME: add DELETE test

    def test_post_login_failure(self):
        """POST the login view, incorrectly."""
        response = self.client.post(
            reverse('elts.views.login'),
            {'username': '', 'password': ''}
        )
        self.assertRedirects(response, reverse('elts.views.login'))

class IndexTestCase(TestCase):
    def test_get_index(self):
        """GET the index view."""
        response = self.client.get(reverse('elts.views.index'))
        self.assertEqual(response.status_code, 200)

class CalendarTestCase(TestCase):
    def test_get_calendar(self):
        """GET the calendar view."""
        response = self.client.get(reverse('elts.views.calendar'))
        self.assertEqual(response.status_code, 200)

class ItemTestCase(TestCase):
    def test_get_item(self):
        """GET the item view."""
        response = self.client.get(reverse('elts.views.item'))
        self.assertEqual(response.status_code, 200)

    def test_get_item_create_form(self):
        """GET the item_create_form view."""
        response = self.client.get(reverse('elts.views.item_create_form'))
        self.assertEqual(response.status_code, 200)

class TagTestCase(TestCase):
    def test_get_tag(self):
        """GET the tag view."""
        response = self.client.get(reverse('elts.views.tag'))
        self.assertEqual(response.status_code, 200)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(IndexTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(CalendarTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ItemTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoginTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TagTestCase))
    suite.addTest(doctest.DocTestSuite(factories))
    return suite
