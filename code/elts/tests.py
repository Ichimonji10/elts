"""Collect this app's doctests into a single suite.

Do not attempt to find other types of tests, such as unit tests. For details on
testing with Django, see:
https://docs.djangoproject.com/en/1.6/topics/testing/overview/

"""
from doctest import DocTestSuite
from templatetags import calendar_tools
import factories, forms, tables, views

def load_tests(loader, tests, ignore):
    """Create a suite of doctests from this Django application."""
    tests.addTests(DocTestSuite(factories))
    tests.addTests(DocTestSuite(forms))
    tests.addTests(DocTestSuite(tables))
    tests.addTests(DocTestSuite(calendar_tools))
    tests.addTests(DocTestSuite(views))
    return tests
