"""Unit tests for this django app's views.

The test cases in this module are called from ``tests.py``.

Each test case  in this module tests a single view. For example,
``ItemCreateFormTestCase`` tests just the ``item_create_form`` view.

Each test case is a subclass of ``django.test.TestCase``.
"``django.test.TestCase`` [...] is a subclass of ``unittest.TestCase`` that runs
each test inside a transaction to provide isolation".

Despite naming conventions which would indicate otherwise, no tests in this
module send PUT or DELETE requests. Instead, tests simply construct POST
requests which act like PUT or DELETE requests by virtue of passing the
'_method' argument.

"""
from datetime import date
from django.core.urlresolvers import reverse
from django.test import TestCase
from elts import factories, models
import string

# pylint: disable=E1103
# Instance of 'WSGIRequest' has no 'status_code' member (but some types could
# not be inferred) (maybe-no-member)
#
# pylint: disable=E1101
# Class 'Item' has no 'objects' member (no-member)
# Class 'ItemFactory' has no 'attributes' member (no-member)

def _login(client):
    """Create a user and use it to log in ``client``."""
    user, password = factories.create_user()
    return client.login(username = user.username, password = password)

def _test_logout(instance, uri = None):
    """Logout ``instance.client``, then GET ``uri``.

    ``instance`` is an instance of a ``TestCase`` subclass. In other words, a
    caller typically passes ``self`` to this method.

    ``uri`` is a string such as ``item/15/delete-form/``. If no value is
    provided, ``uri`` defaults to ``instance.URI``.

    This method asserts that ``instance.client`` is redirected to the
    ``elts.views.login`` view with the ``next`` URL argument set to ``uri``.

    """
    if uri is None:
        uri = instance.URI
    instance.client.logout()
    response = instance.client.get(uri)
    target = string.join(
        [reverse('elts.views.login'), '?' 'next={}'.format(uri)],
        ''
    )
    instance.assertRedirects(response, target)

class IndexTestCase(TestCase):
    """Tests for the ``/`` URI.

    The ``/`` URI is available through the ``elts.views.index`` function.

    """
    URI = reverse('elts.views.index')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CalendarTestCase(TestCase):
    """Tests for the ``calendar/`` URI.

    The ``calendar/`` URI is available through the ``elts.views.calendar``
    function.

    """
    URI = reverse('elts.views.calendar')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CategoryTestCase(TestCase):
    """Tests for the ``category/`` URI.

    The ``category/`` URI is available through the ``elts.views.category``
    function.

    """
    URI = reverse('elts.views.category')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        num_categories = models.Category.objects.count()
        response = self.client.post(
            self.URI,
            factories.CategoryFactory.attributes()
        )
        self.assertEqual(models.Category.objects.count(), num_categories + 1)
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_failure(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(
            self.URI,
            {'name': factories.invalid_category_name()}
        )
        self.assertRedirects(
            response,
            reverse('elts.views.category_create_form')
        )

class CategoryCreateFormTestCase(TestCase):
    """Tests for the ``category/create-form/`` URI.

    The ``category/create-form/`` URI is available through the
    ``elts.views.category_create_form`` function.

    """
    URI = reverse('elts.views.category_create_form')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CategoryIdTestCase(TestCase):
    """Tests for the ``category/<id>/`` URI.

    The ``category/<id>/`` URI is available through the
    ``elts.views.category_id`` function.

    """
    FUNCTION = 'elts.views.category_id'

    def setUp(self):
        """Authenticate the test client, create a category and set ``self.uri``.

        The category created is accessible as ``self.category``.

        """
        _login(self.client)
        self.category = factories.CategoryFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.category.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUT ``self.uri``."""
        data = factories.CategoryFactory.attributes()
        data['_method'] = 'PUT'
        response = self.client.post(self.uri, data)
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_failure(self):
        """PUT ``self.uri``, incorrectly."""
        response = self.client.post(
            self.uri,
            {'name': factories.invalid_category_name(), '_method': 'PUT'}
        )
        self.assertRedirects(
            response,
            reverse(
                'elts.views.category_id_update_form',
                args = [self.category.id]
            )
        )

class CategoryIdDeleteFormTestCase(TestCase):
    """Tests for the ``category/<id>/delete-form/`` URI.

    The ``category/<id>/delete-form/`` URI is available through the
    ``elts.views.category_id_delete_form`` function.

    """
    FUNCTION = 'elts.views.category_id_delete_form'

    def setUp(self):
        """Authenticate the test client, create a category and set ``self.uri``.

        The category created is accessible as ``self.category``.

        """
        _login(self.client)
        self.category = factories.CategoryFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.category.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class CategoryIdUpdateFormTestCase(TestCase):
    """Tests for the ``category/<id>/update-form/`` URI.

    The ``category/<id>/update-form/`` URI is available through the
    ``elts.views.category_id_update_form`` function.

    """
    FUNCTION = 'elts.views.category_id_update_form'

    def setUp(self):
        """Authenticate the test client, create a category and set ``self.uri``.

        The category created is accessible as ``self.category``.

        """
        _login(self.client)
        self.category = factories.CategoryFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.category.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.category.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class ItemTestCase(TestCase):
    """Tests for the ``item/`` URI.

    The ``item/`` URI is available through the ``elts.views.item`` function.

    """
    URI = reverse('elts.views.item')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        num_items = models.Item.objects.count()
        response = self.client.post(
            self.URI,
            factories.ItemFactory.attributes()
        )
        self.assertEqual(models.Item.objects.count(), num_items + 1)
        self.assertRedirects(
            response,
            reverse(
                'elts.views.item_id',
                args = [models.Item.objects.latest('id').id]
            )
        )

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_failure(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(
            response,
            reverse('elts.views.item_create_form')
        )

class ItemCreateFormTestCase(TestCase):
    """Tests for the ``item/create-form/`` URI.

    The ``item/create-form/`` URI is available through the
    ``elts.views.item_create_form`` function.

    """
    URI = reverse('elts.views.item_create_form')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class ItemIdTestCase(TestCase):
    """Tests for the ``item/<id>/`` URI.

    The ``item/<id>/`` URI is available through the ``elts.views.item_id``
    function.

    """
    FUNCTION = 'elts.views.item_id'

    def setUp(self):
        """Authenticate the test client, create an item, and set ``self.uri``.

        The item created is accessible as ``self.item``.

        """
        _login(self.client)
        self.item = factories.ItemFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.item.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        data = factories.ItemFactory.attributes()
        data['_method'] = 'PUT'
        response = self.client.post(self.uri, data)
        self.assertRedirects(response, self.uri)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('elts.views.item'))

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_failure(self):
        """PUT ``self.uri``, incorrectly."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertRedirects(
            response,
            reverse('elts.views.item_id_update_form', args = [self.item.id])
        )

class ItemIdDeleteFormTestCase(TestCase):
    """Tests for the ``item/<id>/delete-form/`` URI.

    The ``item/<id>/delete-form/`` URI is available through the
    ``elts.views.item_id_delete_form`` function.

    """
    FUNCTION = 'elts.views.item_id_delete_form'

    def setUp(self):
        """Authenticate the test client, create an item, and set ``self.uri``.

        The item created is accessible as ``self.item``.

        """
        _login(self.client)
        self.item = factories.ItemFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.item.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class ItemIdUpdateFormTestCase(TestCase):
    """Tests for the ``item/<id>/update-form/`` URI.

    The ``item/<id>/update-form/`` URI is available through the
    ``elts.views.item_id_update_form`` function.

    """
    FUNCTION = 'elts.views.item_id_update_form'

    def setUp(self):
        """Authenticate the test client, create an item, and set ``self.uri``.

        The item created is accessible as ``self.item``.

        """
        _login(self.client)
        self.item = factories.ItemFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.item.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class ItemNoteTestCase(TestCase):
    """Tests for the ``item-note/`` URI.

    The ``item-note/`` URI is available through the ``elts.views.item_note``
    function.

    """
    URI = reverse('elts.views.item_note')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.uri``."""
        item_id = factories.ItemFactory.create()
        num_item_notes = models.ItemNote.objects.count()
        response = self.client.post(
            self.URI,
            {'note_text': factories.note_note_text(), 'item_id': item_id.id}
        )
        self.assertEqual(models.ItemNote.objects.count(), num_item_notes + 1)
        self.assertRedirects(
            response,
            reverse('elts.views.item_id', args = [item_id.id])
        )

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_failure_v1(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertEqual(response.status_code, 422)

    def test_post_failure_v2(self):
        """POST ``self.URI``, incorrectly."""
        item_id = factories.ItemFactory.create()
        num_item_notes = models.ItemNote.objects.count()
        response = self.client.post(
            self.URI,
            {
                'note_text': factories.invalid_note_note_text(),
                'item_id': item_id.id
            }
        )
        self.assertEqual(models.ItemNote.objects.count(), num_item_notes)
        self.assertRedirects(
            response,
            reverse('elts.views.item_id', args = [item_id.id])
        )

class ItemNoteIdTestCase(TestCase):
    """Tests for the ``item-note/<id>/`` URI.

    The ``item-note/<id>/`` URI is available through the
    ``elts.views.item_note_id`` function.

    """
    FUNCTION = 'elts.views.item_note_id'

    def setUp(self):
        """Log in the test client, create an item note, and set ``self.uri``.

        The item note created is accessible as ``self.item_note``.

        """
        _login(self.client)
        self.item_note = factories.ItemNoteFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.item_note.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUT ``self.uri``."""
        data = factories.ItemNoteFactory.attributes()
        data['_method'] = 'PUT'
        response = self.client.post(self.uri, data)
        self.assertRedirects(
            response,
            reverse('elts.views.item_id', args = [self.item_note.item_id.id])
        )

    def test_delete(self):
        """DELETE ``self.uri``."""
        item_id = self.item_note.item_id.id
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertRedirects(
            response,
            reverse('elts.views.item_id', args = [item_id])
        )

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 404)

    def test_put_failure(self):
        """PUT ``self.uri``, incorrectly."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertRedirects(
            response,
            reverse(
                'elts.views.item_note_id_update_form',
                args = [self.item_note.item_id.id]
            )
        )

class ItemNoteIdUpdateFormTestCase(TestCase):
    """Tests for the ``item-note/<id>/update-form/`` URI.

    The ``item-note/<id>/update-form/`` URI is available through the
    ``elts.views.item_note_id_update_form`` function.

    """
    FUNCTION = 'elts.views.item_note_id_update_form'

    def setUp(self):
        """Log in the test client, create an item note, and set ``self.uri``.

        The item note created is accessible as ``self.item_note``.

        """
        _login(self.client)
        self.item_note = factories.ItemNoteFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.item_note.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class ItemNoteIdDeleteFormTestCase(TestCase):
    """Tests for the ``item-note/<id>/delete-form/`` URI.

    The ``item-note/<id>/delete-form/`` URI is available through the
    ``elts.views.item_note_id_delete_form`` function.

    """
    FUNCTION = 'elts.views.item_note_id_delete_form'

    def setUp(self):
        """Log in the test client, create an item note, and set ``self.uri``.

        The item note created is accessible as ``self.item_note``.

        """
        _login(self.client)
        self.item_note = factories.ItemNoteFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.item_note.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class LendTestCase(TestCase):
    """Tests for the ``lend/`` URI.

    The ``lend/`` URI is available through the ``elts.views.lend`` function.

    """
    URI = reverse('elts.views.lend')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        num_lends = models.Lend.objects.count()
        response = self.client.post(
            self.URI,
            {
                'item_id': factories.ItemFactory.create().id,
                'user_id': factories.UserFactory.create().id,
                'due_out': str(date.today()),
            }
        )
        self.assertEqual(models.Lend.objects.count(), num_lends + 1)
        self.assertRedirects(
            response,
            reverse(
                'elts.views.lend_id',
                args = [models.Lend.objects.latest('id').id]
            )
        )

    def test_post_failure(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(response, reverse('elts.views.lend_create_form'))

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class LendCreateFormTestCase(TestCase):
    """Tests for the ``lend/create-form/`` URI.

    The ``lend/create-form/`` URI is available through the
    ``elts.views.lend_create_form`` function.

    """
    URI = reverse('elts.views.lend_create_form')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class LendIdTestCase(TestCase):
    """Tests for the ``lend/<id>/`` URI.

    The ``lend/<id>/`` URI is available through the ``elts.views.lend_id``
    function.

    """
    FUNCTION = 'elts.views.lend_id'

    def setUp(self):
        """Authenticate the test client, create an lend, and set ``self.uri``.

        The lend created is accessible as ``self.lend``.

        """
        _login(self.client)
        self.lend = factories.random_lend_factory().create()
        self.uri = reverse(self.FUNCTION, args = [self.lend.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        data = self.lend.http_dict()
        data['_method'] = 'PUT'
        response = self.client.post(self.uri, data)
        self.assertRedirects(response, self.uri)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('elts.views.lend'))

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_failure(self):
        """PUT ``self.uri``, incorrectly."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertRedirects(
            response,
            reverse('elts.views.lend_id_update_form', args = [self.lend.id])
        )

class LendIdDeleteFormTestCase(TestCase):
    """Tests for the ``lend/<id>/delete-form/`` URI.

    The ``lend/<id>/delete-form/`` URI is available through the
    ``elts.views.lend_id_delete_form`` function.

    """
    FUNCTION = 'elts.views.lend_id_delete_form'

    def setUp(self):
        """Authenticate the test client, create an lend, and set ``self.uri``.

        The lend created is accessible as ``self.lend``.

        """
        _login(self.client)
        self.lend = factories.random_lend_factory().create()
        self.uri = reverse(self.FUNCTION, args = [self.lend.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class LendIdUpdateFormTestCase(TestCase):
    """Tests for the ``lend/<id>/update-form/`` URI.

    The ``lend/<id>/update-form/`` URI is available through the
    ``elts.views.lend_id_update_form`` function.

    """
    FUNCTION = 'elts.views.lend_id_update_form'

    def setUp(self):
        """Authenticate the test client, create an lend, and set ``self.uri``.

        The lend created is accessible as ``self.lend``.

        """
        _login(self.client)
        self.lend = factories.random_lend_factory().create()
        self.uri = reverse(self.FUNCTION, args = [self.lend.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.lend.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class LendNoteTestCase(TestCase):
    """Tests for the ``lend-note/`` URI.

    The ``lend-note/`` URI is available through the ``elts.views.lend_note``
    function.

    """
    URI = reverse('elts.views.lend_note')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.uri``."""
        lend_id = factories.random_lend_factory().create()
        num_lend_notes = models.LendNote.objects.count()
        response = self.client.post(
            self.URI,
            {'note_text': factories.note_note_text(), 'lend_id': lend_id.id}
        )
        self.assertEqual(models.LendNote.objects.count(), num_lend_notes + 1)
        self.assertRedirects(
            response,
            reverse('elts.views.lend_id', args = [lend_id.id])
        )

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_failure_v1(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertEqual(response.status_code, 422)

    def test_post_failure_v2(self):
        """POST ``self.URI``, incorrectly."""
        lend_id = factories.random_lend_factory().create()
        num_lend_notes = models.LendNote.objects.count()
        response = self.client.post(
            self.URI,
            {
                'note_text': factories.invalid_note_note_text(),
                'lend_id': lend_id.id
            }
        )
        self.assertEqual(models.LendNote.objects.count(), num_lend_notes)
        self.assertRedirects(
            response,
            reverse('elts.views.lend_id', args = [lend_id.id])
        )

class LendNoteIdTestCase(TestCase):
    """Tests for the ``lend-note/<id>/`` URI.

    The ``lend-note/<id>/`` URI is available through the
    ``elts.views.lend_note_id`` function.

    """
    FUNCTION = 'elts.views.lend_note_id'

    def setUp(self):
        """Log in the test client, create an lend note, and set ``self.uri``.

        The lend note created is accessible as ``self.lend_note``.

        """
        _login(self.client)
        self.lend_note = factories.LendNoteFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.lend_note.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """PUT ``self.uri``."""
        data = factories.LendNoteFactory.attributes()
        data['_method'] = 'PUT'
        response = self.client.post(self.uri, data)
        self.assertRedirects(
            response,
            reverse('elts.views.lend_id', args = [self.lend_note.lend_id.id])
        )

    def test_delete(self):
        """DELETE ``self.uri``."""
        lend_id = self.lend_note.lend_id.id
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertRedirects(
            response,
            reverse('elts.views.lend_id', args = [lend_id])
        )

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 404)

    def test_put_failure(self):
        """PUT ``self.uri``, incorrectly."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertRedirects(
            response,
            reverse(
                'elts.views.lend_note_id_update_form',
                args = [self.lend_note.lend_id.id]
            )
        )

class LendNoteIdUpdateFormTestCase(TestCase):
    """Tests for the ``lend-note/<id>/update-form/`` URI.

    The ``lend-note/<id>/update-form/`` URI is available through the
    ``elts.views.lend_note_id_update_form`` function.

    """
    FUNCTION = 'elts.views.lend_note_id_update_form'

    def setUp(self):
        """Log in the test client, create an lend note, and set ``self.uri``.

        The lend note created is accessible as ``self.lend_note``.

        """
        _login(self.client)
        self.lend_note = factories.LendNoteFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.lend_note.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class LendNoteIdDeleteFormTestCase(TestCase):
    """Tests for the ``lend-note/<id>/delete-form/`` URI.

    The ``lend-note/<id>/delete-form/`` URI is available through the
    ``elts.views.lend_note_id_delete_form`` function.

    """
    FUNCTION = 'elts.views.lend_note_id_delete_form'

    def setUp(self):
        """Log in the test client, create an lend note, and set ``self.uri``.

        The lend note created is accessible as ``self.lend_note``.

        """
        _login(self.client)
        self.lend_note = factories.LendNoteFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.lend_note.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.lend_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class LoginTestCase(TestCase):
    """Tests for the the ``login/`` URI.

    The ``login/`` URI is available through the ``elts.views.login`` function.

    """
    URI = reverse('elts.views.login')

    def test_post(self):
        """POST ``self.URI``."""
        user, password = factories.create_user()
        response = self.client.post(
            self.URI,
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, reverse('elts.views.index'))

    def test_post_failure(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(response, self.URI)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        _login(self.client)
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertRedirects(response, self.URI)

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

    The ``tag/`` URI is available through the ``elts.views.tag`` function.

    """
    URI = reverse('elts.views.tag')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        num_tags = models.Tag.objects.count()
        response = self.client.post(self.URI, factories.TagFactory.attributes())
        self.assertEqual(models.Tag.objects.count(), num_tags + 1)
        self.assertRedirects(
            response,
            reverse(
                'elts.views.tag_id',
                args = [models.Tag.objects.latest('id').id]
            )
        )

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_failure(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertRedirects(
            response,
            reverse('elts.views.tag_create_form')
        )

class TagCreateFormTestCase(TestCase):
    """Tests for the ``tag/create-form/`` URI.

    The ``tag/create-form/`` URI is available through the
    ``elts.views.tag_create_form`` function.

    """
    URI = reverse('elts.views.tag_create_form')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self)

    def test_post(self):
        """POST ``self.URI``."""
        response = self.client.post(self.URI)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.URI``."""
        response = self.client.get(self.URI)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.URI``."""
        response = self.client.post(self.URI, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class TagIdTestCase(TestCase):
    """Tests for the ``tag/<id>/`` URI.

    The ``tag/<id>/`` URI is available through the ``elts.views.tag_id``
    function.

    """
    FUNCTION = 'elts.views.tag_id'

    def setUp(self):
        """Authenticate the test client, create a tag, and set ``self.uri``.

        The tag created is accessible as ``self.tag``.

        """
        _login(self.client)
        self.tag = factories.TagFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.tag.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        data = factories.TagFactory.attributes()
        data['_method'] = 'PUT'
        response = self.client.post(self.uri, data)
        self.assertRedirects(response, self.uri)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('elts.views.tag'))

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_failure(self):
        """PUT ``self.uri``, incorrectly."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertRedirects(
            response,
            reverse('elts.views.tag_id_update_form', args = [self.tag.id])
        )

class TagIdUpdateFormTestCase(TestCase):
    """Tests for the ``tag/<id>/update-form/`` URI.

    The ``tag/<id>/update-form/`` URI is available through the
    ``elts.views.tag_id_update_form`` function.

    """
    FUNCTION = 'elts.views.tag_id_update_form'

    def setUp(self):
        """Authenticate the test client, create an tag, and set ``self.uri``.

        The tag created is accessible as ``self.tag``.

        """
        _login(self.client)
        self.tag = factories.TagFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.tag.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

class TagIdDeleteFormTestCase(TestCase):
    """Tests for the ``tag/<id>/delete-form/`` URI.

    The ``tag/<id>/delete-form/`` URI is available through the
    ``elts.views.tag_id_delete_form`` function.

    """
    FUNCTION = 'elts.views.tag_id_delete_form'

    def setUp(self):
        """Authenticate the test client, create an tag, and set ``self.uri``.

        The tag created is accessible as ``self.tag``.

        """
        _login(self.client)
        self.tag = factories.TagFactory.create()
        self.uri = reverse(self.FUNCTION, args = [self.tag.id])

    def test_logout(self):
        """Call ``_test_logout()``."""
        _test_logout(self, self.uri)

    def test_post(self):
        """POST ``self.uri``."""
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.uri``."""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """PUT ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """DELETE ``self.uri``."""
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        """POST ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        """GET ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        """PUT ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        """DELETE ``self.uri`` with a bad ID."""
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)
