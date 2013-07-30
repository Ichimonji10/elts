"""Unit tests for this django app's forms.

The test cases in this module are called from ``tests.py``.

Each test case in this module tests a single form. For example, the
``ItemFormTestCase`` tests just the ``ItemForm`` form.

Each test case is a subclass of ``django.test.TestCase``.
"``django.test.TestCase`` [...] is a subclass of ``unittest.TestCase`` that runs
each test inside a transaction to provide isolation".

"""
from django.test import TestCase
from elts import factories
from elts import forms
import random

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
