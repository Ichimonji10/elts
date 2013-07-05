"""URLs and HTTP operations provided by the ``elts`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. Details about each URL, including arguments,
are given after the table.

=============================== ======== ====== ======== ========
URL                             POST     GET    PUT      DELETE
                                (create) (read) (update) (delete)
=============================== ======== ====== ======== ========
``/``                                    *
``calendar/``                            *
``item/``                       *        *
``item/create-form/``                    *
``item/<id>/``                           *      *        *
``item/<id>/delete-form/``               *
``item/<id>/update-form/``               *
``item-note/``                  *
``item-note/<id>``                              *        *
``item-note/<id>/delete-form/``          *
``item-note/<id>/update-form/``          *
``tag/``                        *        *
``tag/<id>/                              *      *        *
``tag/<id>/delete-form/``                *
``tag/<id>/update-form/``                *
=============================== ======== ====== ======== ========

The URLs in this application are organized in a typical RESTful manner. This
means that a URL consists soley of nouns. For example, if trying to delete tag
15, the URL ``/item/15/delete/`` would be incorrect. Instead, a client should
make a ``DELETE`` HTTP request to ``/item/15/``. Being RESTful also means that
URLs are decomposable. If ``/tag/15/lend/`` is available, then ``/tag/15/``,
``/tag/``, and ``/`` should also be available. There is much to the RESTful
design philosophy beyond these few points, and the curious are encouraged to do
some research.

Currently, web browsers are the *only* type of supported client. It is desirable
to extend ELTS so that it can support other types of clients, but no concrete
plans are in place to do so.

Web browsers only support ``POST`` and ``GET`` operations; ``PUT`` and
``DELETE`` operations cannot be performed. To accomodate this limitation, a
hidden form field named "method_override" is present in forms. For example:

    <input type="hidden" name="method_override" value="PUT" />

"""
from django.conf.urls import patterns, url

# pylint: disable=C0103
# "Invalid name "urlpatterns" for type constant (should match
# (([A-Z_][A-Z0-9_]*)|(__.*__))$)"
urlpatterns = patterns('elts.views',
    url(r'^$',                             'index'),
    url(r'^calendar/$',                    'calendar'),
    url(r'^item/$',                        'item'),
    url(r'^item/create-form/$',            'item_create_form'),
    url(r'^item/(\d+)/$',                  'item_id'),
    url(r'^item/(\d+)/update-form/$',      'item_id_update_form'),
    url(r'^item/(\d+)/delete-form/$',      'item_id_delete_form'),
    url(r'^tag/$',                         'tag'),
    url(r'^tag/create-form/$',             'tag_create_form'),
    url(r'^tag/(\d+)/$',                   'tag_id'),
    url(r'^tag/(\d+)/update-form/$',       'tag_id_update_form'),
    url(r'^tag/(\d+)/delete-form/$',       'tag_id_delete_form'),
    url(r'^item-note/$',                   'item_note'),
    url(r'^item-note/(\d+)/$',             'item_note_id'),
    url(r'^item-note/(\d+)/update-form/$', 'item_note_id_update_form'),
    url(r'^item-note/(\d+)/delete-form/$', 'item_note_id_delete_form'),
)
