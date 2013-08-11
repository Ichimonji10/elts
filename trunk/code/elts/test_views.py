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
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.test import TestCase
from elts import factories, models
import string

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
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        self.item.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        self.item.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
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
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        self.item.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        self.item.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        self.item.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
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
        num_item_notes = models.ItemNote.objects.count()
        response = self.client.post(
            self.URI,
            {
                'note_text': \
                factories.random_utf8_str(models.Note.MAX_LEN_NOTE_TEXT),
                'item_id': factories.ItemFactory.create().id
            }
        )
        self.assertEqual(models.ItemNote.objects.count(), num_item_notes + 1)
        self.assertRedirects(
            response,
            reverse(
                'elts.views.item_id',
                args = [models.ItemNote.objects.latest('id').item_id.id]
            )
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

    def test_post_failure(self):
        """POST ``self.URI``, incorrectly."""
        response = self.client.post(self.URI, {})
        self.assertEqual(response.status_code, 422)

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
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        self.item_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
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
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        self.item_note.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        self.item_note.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        self.item_note.delete()
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
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        self.tag.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        self.tag.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
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
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.post(self.uri, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.post(self.uri, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

    def test_post_bad_id(self):
        self.tag.delete()
        response = self.client.post(self.uri, {})
        self.assertEqual(response.status_code, 404)

    def test_get_bad_id(self):
        self.tag.delete()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_put_bad_id(self):
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)

    def test_delete_bad_id(self):
        self.tag.delete()
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 404)
