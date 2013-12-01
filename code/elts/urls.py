"""URLs and HTTP operations provided by the ``elts`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. See ``views.py`` for details about the
functions that handle these URLs.

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
``item-note/<id>/``                             *        *
``item-note/<id>/delete-form/``          *
``item-note/<id>/update-form/``          *
``lend/``                       *        *
``lend/create-form/``                    *
``lend/<id>/``                           *      *        *
``lend/<id>/delete-form``                *
``lend/<id>/update-form``                *
``lend-note/``                  *
``lend-note/<id>/``                             *        *
``lend-note/<id>/delete-form/``          *
``lend-note/<id>/update-form/``          *
``login/``                      *        *               *
``tag/``                        *        *
``tag/create-form/``                     *
``tag/<id>/                              *      *        *
``tag/<id>/delete-form/``                *
``tag/<id>/update-form/``                *
=============================== ======== ====== ======== ========

REST
====

The URLs in this application are organized in a typical RESTful manner. This
means that a URL consists soley of nouns. For example, ``/item/15/delete/`` is
an invalid URL, as "delete" is not a noun. (It is OK to send an HTTP DELETE
message to ``/item/15/``) Being RESTful also means that URLs are decomposable.
If ``/tag/15/update-form/`` is available, then ``/tag/15/``, ``/tag/``, and
``/`` should also be available. There is much to the RESTful design philosophy
beyond these few points, and the curious are encouraged to do some research.

Client Compatibility
====================

Currently, web browsers are the *only* type of supported client. It is desirable
to extend ELTS so that it can support other types of clients, but no concrete
plans are in place to do so.

Web Browser Hacks
=================

Web browsers only support ``POST`` and ``GET`` operations; ``PUT`` and
``DELETE`` operations cannot be performed. To accomodate this limitation, a
hidden form field named "_method" is present in forms. For example:

    <input type="hidden" name="_method" value="PUT" />

"""
from django.conf.urls import patterns, url

urlpatterns = patterns( # pylint: disable=C0103
    'elts.views',
    url(r'^$',                             'index'),
    url(r'^calendar/$',                    'calendar'),
    url(r'^item/$',                        'item'),
    url(r'^item/create-form/$',            'item_create_form'),
    url(r'^item/(\d+)/$',                  'item_id'),
    url(r'^item/(\d+)/delete-form/$',      'item_id_delete_form'),
    url(r'^item/(\d+)/update-form/$',      'item_id_update_form'),
    url(r'^item-note/$',                   'item_note'),
    url(r'^item-note/(\d+)/$',             'item_note_id'),
    url(r'^item-note/(\d+)/delete-form/$', 'item_note_id_delete_form'),
    url(r'^item-note/(\d+)/update-form/$', 'item_note_id_update_form'),
    url(r'^lend/$',                        'lend'),
    url(r'^lend/create-form/$',            'lend_create_form'),
    url(r'^lend/(\d+)/$',                  'lend_id'),
    url(r'^lend/(\d+)/delete-form/$',      'lend_id_delete_form'),
    url(r'^lend/(\d+)/update-form/$',      'lend_id_update_form'),
    url(r'^lend-note/$',                   'lend_note'),
    url(r'^lend-note/(\d+)/$',             'lend_note_id'),
    url(r'^lend-note/(\d+)/delete-form/$', 'lend_note_id_delete_form'),
    url(r'^lend-note/(\d+)/update-form/$', 'lend_note_id_update_form'),
    url(r'^login/$',                       'login'),
    url(r'^tag/$',                         'tag'),
    url(r'^tag/create-form/$',             'tag_create_form'),
    url(r'^tag/(\d+)/$',                   'tag_id'),
    url(r'^tag/(\d+)/delete-form/$',       'tag_id_delete_form'),
    url(r'^tag/(\d+)/update-form/$',       'tag_id_update_form'),
)
