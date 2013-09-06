"""Unit tests for this django app's forms.

The test cases in this module are called from ``tests.py``.

Each test case in this module tests a single form. For example, the
``ItemFormTestCase`` tests just the ``ItemForm`` form.

Each test case is a subclass of ``django.test.TestCase``.
"``django.test.TestCase`` [...] is a subclass of ``unittest.TestCase`` that runs
each test inside a transaction to provide isolation".

"""
from django.test import TestCase
from elts.factories import random_utf8_str
from elts import forms, models
import random

class ItemFormTestCase(TestCase):
    """Tests for ``ItemForm``."""
    @classmethod
    def _name(cls):
        """Returns a value for the ``name`` form field."""
        return random_utf8_str(1, models.Item.MAX_LEN_NAME)

    @classmethod
    def _description(cls):
        """Returns a value for the ``description`` form field."""
        return random_utf8_str(1, models.Item.MAX_LEN_DESCRIPTION)

    @classmethod
    def _is_lendable(cls):
        """Returns a value for the ``is_lendable`` form field."""
        return random.choice([True, False])

    @classmethod
    def _tags(cls):
        """Returns a value for the ``tags`` form field."""
        random.randint(1, 100) # FIXME: what's the max for an ID val?

    def test_valid(self):
        """Creates a valid ItemForm."""
        form = forms.ItemForm({'name': self._name()})
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_missing_name(self):
        """Creates an ItemForm without setting ``name``."""
        form = forms.ItemForm({})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_has_description(self):
        """Creates an ItemForm and sets ``description``."""
        form = forms.ItemForm({
            'name': self._name(),
            'description': self._description()
        })
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_has_is_lendable(self):
        """Creates an ItemForm and sets ``is_lendable``."""
        form = forms.ItemForm({
            'name': self._name(),
            'is_lendable': self._is_lendable()
        })
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_has_tags(self):
        """Creates an ItemForm and sets ``tags``."""
        form = forms.ItemForm({
            'name': self._name(),
            'tags': self._tags()
        })
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

class TagFormTestCase(TestCase):
    """Tests for ``TagForm``."""
    @classmethod
    def _name(cls):
        """Returns a value for the ``name`` form field."""
        return random_utf8_str(1, models.Tag.MAX_LEN_NAME)

    @classmethod
    def _description(cls):
        """Returns a value for the ``description`` form field."""
        return random_utf8_str(1, models.Tag.MAX_LEN_DESCRIPTION)

    def test_valid(self):
        """Creates a valid TagForm."""
        form = forms.TagForm({'name': self._name()})
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_missing_name(self):
        """Creates a TagForm without setting ``name``."""
        form = forms.TagForm({})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_invalid_name(self):
        """Creates a TagForm and sets an invalid ``name``."""
        form = forms.TagForm({
            'name': random_utf8_str(models.Tag.MAX_LEN_NAME + 1)
        })
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_has_description(self):
        """Creates a TagForm and sets ``description``."""
        form = forms.TagForm({
            'name': self._name(),
            'description': self._description()
        })
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_invalid_description(self):
        """Creates a TagForm and sets an invalid ``description``."""
        form = forms.TagForm({
            'name': self._name(),
            'description': random_utf8_str(models.Tag.MAX_LEN_DESCRIPTION + 1)
        })
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

class ItemNoteFormTestCase(TestCase):
    """Tests for ``ItemNoteForm``."""
    @classmethod
    def _note_text(cls):
        """Returns a value for the ``note_text`` form field."""
        return random_utf8_str(1, models.ItemNote.MAX_LEN_NOTE_TEXT)

    def test_valid(self):
        """Creates a valid ItemNoteForm."""
        form = forms.ItemNoteForm({'note_text': self._note_text()})
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_missing_note_text(self):
        """Creates an ItemNoteForm without setting ``note_text``."""
        form = forms.ItemNoteForm({})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_invalid_note_text(self):
        """Creates an ItemNoteForm and sets an invalid note_text.``"""
        form = forms.ItemNoteForm({
            'note_text': random_utf8_str(models.ItemNote.MAX_LEN_NOTE_TEXT + 1)
        })
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

class UserNoteFormTestCase(TestCase):
    """Tests for ``UserNoteForm``."""
    @classmethod
    def _note_text(cls):
        """Returns a value for the ``note_text`` form field."""
        return random_utf8_str(1, models.UserNote.MAX_LEN_NOTE_TEXT)

    def test_valid(self):
        """Creates a valid UserNoteForm."""
        form = forms.UserNoteForm({'note_text': self._note_text()})
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_missing_note_text(self):
        """Creates an UserNoteForm without setting ``note_text``."""
        form = forms.UserNoteForm({})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_invalid_note_text(self):
        """Creates an UserNoteForm and sets an invalid note_text.``"""
        form = forms.UserNoteForm({
            'note_text': random_utf8_str(models.UserNote.MAX_LEN_NOTE_TEXT + 1)
        })
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

class LendNoteFormTestCase(TestCase):
    """Tests for ``LendNoteForm``."""
    @classmethod
    def _note_text(cls):
        """Returns a value for the ``note_text`` form field."""
        return random_utf8_str(1, models.LendNote.MAX_LEN_NOTE_TEXT)

    @classmethod
    def _is_complaint(cls):
        """Returns a value for the ``is_complaint`` form field."""
        return random.choice([True, False])

    def test_valid(self):
        """Creates a valid LendNoteForm."""
        form = forms.LendNoteForm({'note_text': self._note_text()})
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_missing_note_text(self):
        """Creates an LendNoteForm without setting ``note_text``."""
        form = forms.LendNoteForm({})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_invalid_note_text(self):
        """Creates an LendNoteForm and sets an invalid note_text.``"""
        form = forms.LendNoteForm({
            'note_text': random_utf8_str(models.LendNote.MAX_LEN_NOTE_TEXT + 1)
        })
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_has_is_complaint(self):
        """Creates a LendNoteForm and sets ``is_complaint``."""
        form = forms.LendNoteForm({
            'note_text': self._note_text(),
            'is_complaint': self._is_complaint()
        })
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

class LoginFormTestCase(TestCase):
    """Tests for ``LoginForm``."""
    @classmethod
    def _username(cls):
        """Returns a value for the ``username`` form field."""
        return random_utf8_str(1, 1000)

    @classmethod
    def _password(cls):
        """Returns a value for the ``password`` form field."""
        return random_utf8_str(1, 1000)

    def test_valid(self):
        """Creates a valid LoginForm."""
        form = forms.LoginForm({
            'username': self._username(),
            'password': self._password()
        })
        self.assertTrue(form.is_valid()) # pylint: disable=E1101

    def test_missing_username(self):
        """Creates a LoginForm without setting ``username``."""
        form = forms.LoginForm({'password': self._password()})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101

    def test_missing_password(self):
        """Creates a LoginForm without setting ``password``."""
        form = forms.LoginForm({'username': self._username()})
        self.assertFalse(form.is_valid()) # pylint: disable=E1101
