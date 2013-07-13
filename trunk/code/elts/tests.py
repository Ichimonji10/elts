"""Unit tests for this django app.

``django.utils.unittest`` is an alias for Django's bundled copy of unittest2,
backported for Python 2.5 compatibility. If you have Python2.7 (ergo unittest2)
installed already, that will be used instead. Further, "``django.test.TestCase``
[...] is a subclass of ``unittest.TestCase`` that runs each test inside a
transaction to provide isolation".

For details, see:
https://docs.djangoproject.com/en/1.5/topics/testing/overview/#writing-tests

"""
from django.test import TestCase
from django.utils.unittest import TestLoader, TestSuite

class LoginTestCase(TestCase):
    def test_get_login_page(self):
        self.assertTrue(True)
        # fetch login page with self.user, assert 200 return code, etc

class SampleTestCase(TestCase):
    def test_addition(self):
        self.assertEqual(2 + 2, 4)

def suite():
    return TestSuite([
        TestLoader().loadTestsFromTestCase(LoginTestCase),
        TestLoader().loadTestsFromTestCase(SampleTestCase),
    ])
