"""Unit tests for this django app.

``django.utils.unittest`` is an alias for Django's bundled copy of unittest2,
backported for Python 2.5 compatibility. If you have Python2.7 (ergo unittest2)
installed already, that will be used instead. Further, "``django.test.TestCase``
[...] is a subclass of ``unittest.TestCase`` that runs each test inside a
transaction to provide isolation".

For details, see:
https://docs.djangoproject.com/en/1.5/topics/testing/overview/#writing-tests

"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import unittest
from elts import factories
import doctest

class LoginTestCase(TestCase):
    def test_get_login_page(self):
        """GET the login view."""
        response = self.client.get(reverse('elts.views.login'))
        self.assertEqual(response.status_code, 200)

    def test_post_login(self): # FIXME
        """POST and DELETE the login view."""
        user = factories.UserFactory.create()
        response = self.client.post(
            reverse('elts.views.login'),
            {'username': user.username, 'password': user.password}
        )
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_post_login_failure(self):
        """POST the login view, incorrectly."""
        response = self.client.post(
            reverse('elts.views.login'),
            {'username': '', 'password': ''}
        )
        self.assertRedirects(response, reverse('elts.views.login'))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoginTestCase))
    suite.addTest(doctest.DocTestSuite(factories))
    return suite
