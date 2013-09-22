"""Unit tests for this django app's forms.

The test cases in this module are called from ``tests.py``.

Each test case in this module tests a single form. For example, the
``ItemFormTestCase`` tests just the ``ItemForm`` form.

Each test case is a subclass of ``django.test.TestCase``.
"``django.test.TestCase`` [...] is a subclass of ``unittest.TestCase`` that runs
each test inside a transaction to provide isolation".

"""
from datetime import datetime
from django.test import TestCase
from elts.factories import random_utf8_str, UserFactory, ItemFactory
from elts import forms, models
import random

# pylint: disable=E1101
# Class 'ItemFactory' has no 'create' member (no-member)
# Instance of 'ItemForm' has no 'is_valid' member (no-member)
# Instance of 'ItemFormTestCase' has no 'assertTrue' member (no-member)

class ItemFormTestCase(TestCase):
    """Tests for ``ItemForm``."""
    @classmethod
    def _name(cls):
        """Return a value for the ``name`` form field."""
        return random_utf8_str(1, models.Item.MAX_LEN_NAME)

    @classmethod
    def _description(cls):
        """Return a value for the ``description`` form field."""
        return random_utf8_str(1, models.Item.MAX_LEN_DESCRIPTION)

    @classmethod
    def _is_lendable(cls):
        """Return a value for the ``is_lendable`` form field."""
        return random.choice([True, False])

    @classmethod
    def _tags(cls):
        """Return a value for the ``tags`` form field."""
        random.randint(1, 100) # FIXME: what's the max for an ID val?

    def test_valid(self):
        """Create a valid ItemForm."""
        form = forms.ItemForm({'name': self._name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Create an ItemForm without setting ``name``."""
        form = forms.ItemForm({})
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Create an ItemForm and set ``description``."""
        form = forms.ItemForm({
            'name': self._name(),
            'description': self._description()
        })
        self.assertTrue(form.is_valid())

    def test_has_is_lendable(self):
        """Create an ItemForm and set ``is_lendable``."""
        form = forms.ItemForm({
            'name': self._name(),
            'is_lendable': self._is_lendable()
        })
        self.assertTrue(form.is_valid())

    def test_has_tags(self):
        """Create an ItemForm and set ``tags``."""
        form = forms.ItemForm({
            'name': self._name(),
            'tags': self._tags()
        })
        self.assertTrue(form.is_valid())

class TagFormTestCase(TestCase):
    """Tests for ``TagForm``."""
    @classmethod
    def _name(cls):
        """Return a value for the ``name`` form field."""
        return random_utf8_str(1, models.Tag.MAX_LEN_NAME)

    @classmethod
    def _description(cls):
        """Return a value for the ``description`` form field."""
        return random_utf8_str(1, models.Tag.MAX_LEN_DESCRIPTION)

    def test_valid(self):
        """Create a valid TagForm."""
        form = forms.TagForm({'name': self._name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Create a TagForm without setting ``name``."""
        form = forms.TagForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_name(self):
        """Create a TagForm and set an invalid ``name``."""
        form = forms.TagForm({
            'name': random_utf8_str(models.Tag.MAX_LEN_NAME + 1)
        })
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Create a TagForm and set ``description``."""
        form = forms.TagForm({
            'name': self._name(),
            'description': self._description()
        })
        self.assertTrue(form.is_valid())

    def test_invalid_description(self):
        """Create a TagForm and set an invalid ``description``."""
        form = forms.TagForm({
            'name': self._name(),
            'description': random_utf8_str(models.Tag.MAX_LEN_DESCRIPTION + 1)
        })
        self.assertFalse(form.is_valid())

class ItemNoteFormTestCase(TestCase):
    """Tests for ``ItemNoteForm``."""
    @classmethod
    def _note_text(cls):
        """Return a value for the ``note_text`` form field."""
        return random_utf8_str(1, models.ItemNote.MAX_LEN_NOTE_TEXT)

    def test_valid(self):
        """Create a valid ItemNoteForm."""
        form = forms.ItemNoteForm({'note_text': self._note_text()})
        self.assertTrue(form.is_valid())

    def test_missing_note_text(self):
        """Create an ItemNoteForm without setting ``note_text``."""
        form = forms.ItemNoteForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_note_text(self):
        """Create an ItemNoteForm and set an invalid note_text.``"""
        form = forms.ItemNoteForm({
            'note_text': random_utf8_str(models.ItemNote.MAX_LEN_NOTE_TEXT + 1)
        })
        self.assertFalse(form.is_valid())

class UserNoteFormTestCase(TestCase):
    """Tests for ``UserNoteForm``."""
    @classmethod
    def _note_text(cls):
        """Return a value for the ``note_text`` form field."""
        return random_utf8_str(1, models.UserNote.MAX_LEN_NOTE_TEXT)

    def test_valid(self):
        """Create a valid UserNoteForm."""
        form = forms.UserNoteForm({'note_text': self._note_text()})
        self.assertTrue(form.is_valid())

    def test_missing_note_text(self):
        """Create an UserNoteForm without setting ``note_text``."""
        form = forms.UserNoteForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_note_text(self):
        """Create an UserNoteForm and set an invalid note_text.``"""
        form = forms.UserNoteForm({
            'note_text': random_utf8_str(models.UserNote.MAX_LEN_NOTE_TEXT + 1)
        })
        self.assertFalse(form.is_valid())

class LendNoteFormTestCase(TestCase):
    """Tests for ``LendNoteForm``."""
    @classmethod
    def _note_text(cls):
        """Return a value for the ``note_text`` form field."""
        return random_utf8_str(1, models.LendNote.MAX_LEN_NOTE_TEXT)

    @classmethod
    def _is_complaint(cls):
        """Return a value for the ``is_complaint`` form field."""
        return random.choice([True, False])

    def test_valid(self):
        """Create a valid LendNoteForm."""
        form = forms.LendNoteForm({'note_text': self._note_text()})
        self.assertTrue(form.is_valid())

    def test_missing_note_text(self):
        """Create an LendNoteForm without setting ``note_text``."""
        form = forms.LendNoteForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_note_text(self):
        """Create an LendNoteForm and set an invalid note_text.``"""
        form = forms.LendNoteForm({
            'note_text': random_utf8_str(models.LendNote.MAX_LEN_NOTE_TEXT + 1)
        })
        self.assertFalse(form.is_valid())

    def test_has_is_complaint(self):
        """Create a LendNoteForm and set ``is_complaint``."""
        form = forms.LendNoteForm({
            'note_text': self._note_text(),
            'is_complaint': self._is_complaint()
        })
        self.assertTrue(form.is_valid())

class LendFormTestCase(TestCase):
    """Tests for ``LendForm``."""
    def test_valid(self):
        """Create a valid LendForm."""
        form = forms.LendForm({
            'item_id': ItemFactory.create().id,
            'user_id': UserFactory.create().id,
        })
        self.assertTrue(form.is_valid())

    def test_missing_user_id(self):
        """Create a LendForm with setting ``user_id``."""
        form = forms.LendForm({'item_id': ItemFactory.create().id})
        self.assertFalse(form.is_valid())

    def test_missing_item_id(self):
        """Create a LendForm with setting ``item_id``."""
        form = forms.LendForm({'user_id': ItemFactory.create().id})
        self.assertFalse(form.is_valid())

    def test_has_due_out(self):
        """Create a LendForm and set ``due_out``."""
        form = forms.LendForm({
            'item_id': ItemFactory.create().id,
            'user_id': UserFactory.create().id,
            'due_out': datetime.today(),
        })
        self.assertTrue(form.is_valid())

    def test_has_due_back(self):
        """Create a LendForm and set ``due_back``."""
        form = forms.LendForm({
            'item_id': ItemFactory.create().id,
            'user_id': UserFactory.create().id,
            'due_back': datetime.today(),
        })
        self.assertTrue(form.is_valid())

class LoginFormTestCase(TestCase):
    """Tests for ``LoginForm``."""
    @classmethod
    def _username(cls):
        """Return a value for the ``username`` form field."""
        return random_utf8_str(1, 1000)

    @classmethod
    def _password(cls):
        """Return a value for the ``password`` form field."""
        return random_utf8_str(1, 1000)

    def test_valid(self):
        """Create a valid LoginForm."""
        form = forms.LoginForm({
            'username': self._username(),
            'password': self._password()
        })
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        """Create a LoginForm without setting ``username``."""
        form = forms.LoginForm({'password': self._password()})
        self.assertFalse(form.is_valid())

    def test_missing_password(self):
        """Create a LoginForm without setting ``password``."""
        form = forms.LoginForm({'username': self._username()})
        self.assertFalse(form.is_valid())
