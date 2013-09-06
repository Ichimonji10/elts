"""Unit tests for this django app.

``django.utils.unittest`` is an alias for Django's bundled copy of unittest2,
backported for Python 2.5 compatibility. If you have Python2.7 (ergo unittest2)
installed already, that will be used instead.

For details on Django's testing tools, see:
https://docs.djangoproject.com/en/1.5/topics/testing/overview/

"""
from doctest import DocTestSuite
from elts import factories, test_forms, test_views
from unittest import TestSuite, TestLoader

def suite():
    """Collects test suites and doctests in this Django app into a single suite.

    In Django 1.6, this will no longer be necessary. Django will simply look for
    test cases in any file whose name begins with "test".

    """
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromModule(test_forms))
    test_suite.addTest(TestLoader().loadTestsFromModule(test_views))
    test_suite.addTest(DocTestSuite(factories))
    return test_suite
