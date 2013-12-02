"""Unit tests for this django app's forms.

The test cases in this module are called from ``tests.py``.

Each test case in this module tests a single form. For example, the
``ItemFormTestCase`` tests just the ``ItemForm`` form.

Each test case is a subclass of ``django.test.TestCase``.
"``django.test.TestCase`` [...] is a subclass of ``unittest.TestCase`` that runs
each test inside a transaction to provide isolation".

"""
from datetime import timedelta
from django.test import TestCase
from elts import factories
from elts import forms
import random
import unittest

# pylint: disable=E1101
# Class 'PastLendFactory' has no 'create' member (no-member)
# Instance of 'ItemForm' has no 'is_valid' member (no-member)
# Instance of 'ItemFormTestCase' has no 'assertTrue' member (no-member)
#
# pylint: disable=R0904
# Classes inheriting from TestCase will have 60+ too many public methods, and
# that's not something I have control over. Ignore it.

class ItemFormTestCase(TestCase):
    """Tests for ``ItemForm``."""
    def test_valid(self):
        """Create a valid ItemForm."""
        form = forms.ItemForm({'name': factories.item_name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Create an ItemForm without setting ``name``."""
        form = forms.ItemForm({})
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Create an ItemForm and set ``description``."""
        form = forms.ItemForm({
            'name': factories.item_name(),
            'description': factories.item_description(),
        })
        self.assertTrue(form.is_valid())

    def test_has_is_lendable(self):
        """Create an ItemForm and set ``is_lendable``."""
        form = forms.ItemForm({
            'name': factories.item_name(),
            'is_lendable': factories.item_is_lendable(),
        })
        self.assertTrue(form.is_valid())

    def test_has_tags(self):
        """Create an ItemForm and set ``tags``."""
        form = forms.ItemForm({
            'name': factories.item_name(),
            'tags': factories.item_tags(),
        })
        self.assertTrue(form.is_valid())

class TagFormTestCase(TestCase):
    """Tests for ``TagForm``."""
    def test_valid(self):
        """Create a valid TagForm."""
        form = forms.TagForm({'name': factories.tag_name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Create a TagForm without setting ``name``."""
        form = forms.TagForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_name(self):
        """Create a TagForm and set an invalid ``name``."""
        form = forms.TagForm({
            'name': factories.invalid_tag_name()
        })
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Create a TagForm and set ``description``."""
        form = forms.TagForm({
            'name': factories.tag_name(),
            'description': factories.tag_description(),
        })
        self.assertTrue(form.is_valid())

    def test_invalid_description(self):
        """Create a TagForm and set an invalid ``description``."""
        form = forms.TagForm({
            'name': factories.tag_name(),
            'description': factories.invalid_tag_description(),
        })
        self.assertFalse(form.is_valid())

class ItemNoteFormTestCase(TestCase):
    """Tests for ``ItemNoteForm``."""
    def test_valid(self):
        """Create a valid ItemNoteForm."""
        form = forms.ItemNoteForm({'note_text': factories.note_note_text()})
        self.assertTrue(form.is_valid())

    def test_missing_note_text(self):
        """Create an ItemNoteForm without setting ``note_text``."""
        form = forms.ItemNoteForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_note_text(self):
        """Create an ItemNoteForm and set an invalid note_text.``"""
        form = forms.ItemNoteForm({
            'note_text': factories.invalid_note_note_text()
        })
        self.assertFalse(form.is_valid())

class UserNoteFormTestCase(TestCase):
    """Tests for ``UserNoteForm``."""
    def test_valid(self):
        """Create a valid UserNoteForm."""
        form = forms.UserNoteForm({'note_text': factories.note_note_text()})
        self.assertTrue(form.is_valid())

    def test_missing_note_text(self):
        """Create an UserNoteForm without setting ``note_text``."""
        form = forms.UserNoteForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_note_text(self):
        """Create an UserNoteForm and set an invalid note_text.``"""
        form = forms.UserNoteForm({
            'note_text': factories.invalid_note_note_text()
        })
        self.assertFalse(form.is_valid())

class LendNoteFormTestCase(TestCase):
    """Tests for ``LendNoteForm``."""
    def test_valid(self):
        """Create a valid LendNoteForm."""
        form = forms.LendNoteForm({'note_text': factories.note_note_text()})
        self.assertTrue(form.is_valid())

    def test_missing_note_text(self):
        """Create an LendNoteForm without setting ``note_text``."""
        form = forms.LendNoteForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_note_text(self):
        """Create an LendNoteForm and set an invalid note_text.``"""
        form = forms.LendNoteForm({
            'note_text': factories.invalid_note_note_text()
        })
        self.assertFalse(form.is_valid())

    def test_has_is_complaint(self):
        """Create a LendNoteForm and set ``is_complaint``."""
        form = forms.LendNoteForm({
            'note_text': factories.note_note_text(),
            'is_complaint': factories.lend_note_is_complaint()
        })
        self.assertTrue(form.is_valid())

class LendFormTestCase(TestCase):
    """Tests for ``LendForm``.

    A minimal ``LendForm`` has ``user_id``, ``item_id`` and either ``due_out``
    or ``out`` set.

    """
    @classmethod
    def _copy_user_and_item(cls, lend):
        """Copy ``lend.user_id.id`` and ``lend.item_id.id`` to a dict."""
        return {
            'user_id': lend.user_id.id,
            'item_id': lend.item_id.id
        }

    def test_valid_v1(self):
        """Create a valid LendForm with ``due_out`` set."""
        form = forms.LendForm({
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
            'due_out': factories.lend_due_out()
        })
        self.assertTrue(form.is_valid())

    def test_valid_v2(self):
        """Create a valid LendForm with ``out`` set."""
        form = forms.LendForm({
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
            'out': factories.lend_out()
        })
        self.assertTrue(form.is_valid())

    def test_missing_user_id(self):
        """Create a LendForm without setting ``user_id``."""
        form = forms.LendForm({
            'item_id': factories.ItemFactory.create().id,
            'due_out': factories.lend_due_out(),
            'out': factories.lend_out()
        })
        self.assertFalse(form.is_valid())

    def test_missing_item_id(self):
        """Create a LendForm without setting ``item_id``."""
        form = forms.LendForm({
            'user_id': factories.UserFactory.create().id,
            'due_out': factories.lend_due_out(),
            'out': factories.lend_out()
        })
        self.assertFalse(form.is_valid())

    def test_missing_out_and_due_out(self):
        """Create a LendForm without setting ``out`` or ``due_out``."""
        form = forms.LendForm({
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
        })
        self.assertFalse(form.is_valid())

    def test_if_back_then_out(self):
        """If ``back`` is set, ``out`` must also be set."""
        data = {
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
            'due_out': factories.lend_due_out(), # due_out or out is required
            'back': factories.lend_back(),
        }
        self.assertFalse(forms.LendForm(data).is_valid())
        data['out'] = data['back'] - timedelta(days = 1)
        self.assertTrue(forms.LendForm(data).is_valid())

    def test_if_due_back_then_due_out(self):
        """If ``due_back`` is set, ``due_out`` must also be set."""
        data = {
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
            'out': factories.lend_out(), # due_out or out is required
            'due_back': factories.lend_due_back(),
        }
        self.assertFalse(forms.LendForm(data).is_valid())
        data['due_out'] = data['due_back'] - timedelta(days = 1)
        self.assertTrue(forms.LendForm(data).is_valid())

    def test_due_out_before_due_back(self):
        """``due_out`` must occur before ``due_back``."""
        data = {
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
            'due_out': factories.lend_due_out(),
        }
        data['due_back'] = data['due_out'] - timedelta(days = 1)
        self.assertFalse(forms.LendForm(data).is_valid())
        data['due_back'] = data['due_out'] + timedelta(days = 1)
        self.assertTrue(forms.LendForm(data).is_valid())

    def test_out_before_back(self):
        """``out`` must occur before ``back``."""
        data = {
            'user_id': factories.UserFactory.create().id,
            'item_id': factories.ItemFactory.create().id,
            'out': factories.lend_out(),
        }
        data['back'] = data['out'] - timedelta(days = 1)
        self.assertFalse(forms.LendForm(data).is_valid())
        data['back'] = data['out'] + timedelta(days = 1)
        self.assertTrue(forms.LendForm(data).is_valid())

    def test_conflict_v1(self):
        """Check whether ``due_out`` conflicts with an existing lend.

        In this scenario:
        * old_lend.due_out != Null
        * old_lend.due_back == Null

        Then, ``new_lend['due_out']`` is set to before and during ``old_lend``.

        """
        old_lend = factories.FutureLendFactory.create()
        new_lend = self._copy_user_and_item(old_lend)

        # before old_lend
        new_lend['due_out'] = old_lend.due_out - timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['due_out'] = old_lend.due_out
        self.assertFalse(forms.LendForm(new_lend).is_valid())
        new_lend['due_out'] = old_lend.due_out + timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

    def test_conflict_v2(self):
        """Check whether ``due_out`` conflicts with an existing lend.

        In this scenario:
        * old_lend.due_out != Null
        * old_lend.due_back != Null

        Then, ``new_lend['due_out']`` is set to before, during and after
        ``old_lend``.

        """
        old_lend = factories.FutureLendFactory.create()
        old_lend.due_back = old_lend.due_out
        old_lend.save()
        new_lend = self._copy_user_and_item(old_lend)

        # before old_lend
        new_lend['due_out'] = old_lend.due_out - timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['due_out'] = old_lend.due_out
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # after old_lend
        new_lend['due_out'] = old_lend.due_back + timedelta(days = 1)
        self.assertTrue(forms.LendForm(new_lend).is_valid())

    def test_conflict_v3(self):
        """Check whether ``due_back`` conflicts with an existing lend.

        In this scenario:
        * old_lend.due_out != Null
        * old_lend.due_back == Null
        * new_lend.due_out < old_lend.due_out

        Then, ``new_lend['due_back']`` is set to before and during ``old_lend``.

        """
        old_lend = factories.FutureLendFactory.create()
        new_lend = self._copy_user_and_item(old_lend)
        new_lend['due_out'] = old_lend.due_out - timedelta(days = 2)

        # before old_lend
        new_lend['due_back'] = old_lend.due_out - timedelta(days = 1)
        self.assertTrue(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['due_back'] = old_lend.due_out
        self.assertFalse(forms.LendForm(new_lend).is_valid())
        new_lend['due_back'] = old_lend.due_out + timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

    def test_conflict_v4(self):
        """Check whether ``due_back`` conflicts with an existing lend.

        In this scenario:
        * old_lend.due_out != Null
        * old_lend.due_back != Null
        * new_lend.due_out < old_lend.due_out

        Then, ``new_lend['due_back']`` is set to before, during and after
        ``old_lend``.

        """
        old_lend = factories.FutureLendFactory.create()
        old_lend.due_back = old_lend.due_out
        old_lend.save()
        new_lend = self._copy_user_and_item(old_lend)
        new_lend['due_out'] = old_lend.due_out - timedelta(days = 2)

        # before old_lend
        new_lend['due_back'] = old_lend.due_out - timedelta(days = 1)
        self.assertTrue(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['due_back'] = old_lend.due_out
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # after old_lend
        new_lend['due_back'] = old_lend.due_back + timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

    def test_conflict_v5(self):
        """Check whether ``out`` conflicts with an existing lend.

        In this scenario:
        * old_lend.out != Null
        * old_lend.back == Null

        Then, ``new_lend['out']`` is set to before and during ``old_lend``.

        """
        old_lend = factories.PastLendFactory.create()
        new_lend = self._copy_user_and_item(old_lend)

        # before old_lend
        new_lend['out'] = old_lend.out - timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['out'] = old_lend.out
        self.assertFalse(forms.LendForm(new_lend).is_valid())
        new_lend['out'] = old_lend.out + timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

    def test_conflict_v6(self):
        """Check whether ``out`` conflicts with an existing lend.

        In this scenario:
        * old_lend.out != Null
        * old_lend.back != Null

        Then, ``new_lend['out']`` is set to before, during and after
        ``old_lend``.

        """
        old_lend = factories.PastLendFactory.create()
        old_lend.back = old_lend.out
        old_lend.save()
        new_lend = self._copy_user_and_item(old_lend)

        # before old_lend
        new_lend['out'] = old_lend.out - timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['out'] = old_lend.out
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # after old_lend
        new_lend['out'] = old_lend.back + timedelta(days = 1)
        self.assertTrue(forms.LendForm(new_lend).is_valid())

    def test_conflict_v7(self):
        """Check whether ``back`` conflicts with an existing lend.

        In this scenario:
        * old_lend.out != Null
        * old_lend.back == Null
        * new_lend.out < old_lend.out

        Then, ``new_lend['back']`` is set to before and during ``old_lend``.

        """
        old_lend = factories.PastLendFactory.create()
        new_lend = self._copy_user_and_item(old_lend)
        new_lend['out'] = old_lend.out - timedelta(days = 1)

        # before old_lend
        new_lend['back'] = old_lend.out - timedelta(days = 1)
        self.assertTrue(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['back'] = old_lend.out
        self.assertFalse(forms.LendForm(new_lend).is_valid())
        new_lend['back'] = old_lend.out + timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

    def test_conflict_v8(self):
        """Check whether ``back`` conflicts with an existing lend.

        In this scenario:
        * old_lend.out != Null
        * old_lend.back != Null
        * new_lend.out < old_lend.out

        Then, ``new_lend['back']`` is set to before, during and after
        ``old_lend``.

        """
        old_lend = factories.PastLendFactory.create()
        old_lend.back = old_lend.out
        old_lend.save()
        new_lend = self._copy_user_and_item(old_lend)
        new_lend['out'] = old_lend.out - timedelta(days = 1)

        # before old_lend
        new_lend['back'] = old_lend.out - timedelta(days = 1)
        self.assertTrue(forms.LendForm(new_lend).is_valid())

        # during old_lend
        new_lend['back'] = old_lend.out
        self.assertFalse(forms.LendForm(new_lend).is_valid())

        # after old_lend
        new_lend['back'] = old_lend.back + timedelta(days = 1)
        self.assertFalse(forms.LendForm(new_lend).is_valid())

class LoginFormTestCase(TestCase):
    """Tests for ``LoginForm``."""
    def test_valid(self):
        """Create a valid LoginForm."""
        form = forms.LoginForm({
            'username': factories.user_username(),
            'password': factories.user_password(),
        })
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        """Create a LoginForm without setting ``username``."""
        form = forms.LoginForm({'password': factories.user_password()})
        self.assertFalse(form.is_valid())

    def test_missing_password(self):
        """Create a LoginForm without setting ``password``."""
        form = forms.LoginForm({'username': factories.user_username()})
        self.assertFalse(form.is_valid())
