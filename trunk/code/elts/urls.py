"""URLs and HTTP operations provided by the ``elts`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. Details about each URL, including arguments,
are given after the table.

=========================== ======== ====== ======== ========
URL                         POST     GET    PUT      DELETE
                            (create) (read) (update) (delete)
=========================== ======== ====== ======== ========
``/``                                *
``calendar/``                        *
``item/``                   *        *
``item/create-form/``                *
``item/lend/``                       *
``item/<id>/``                       *      *        *
``item/<id>/update-form/``           *
``item/<id>/lend/``                  *
``item/<id>/reservation/``  *        *      *        *
``item/<id>/tag/``          *        *      *        *
``tag/``                    *        *
``tag/<id>/                          *      *        *
=========================== ======== ====== ======== ========

``/``
    ``GET`` returns a home page containing a summary of information in ELTS,
    such as which items are due back on that day.

``calendar/``
    ``GET`` returns a calendar displaying reservations and lends within a
    certain time period, such as the current week or month.

``item/``
    ``POST`` creates a new item. If the request cannot be completed, the user is
    informed of the reason(s). Optionally, the information submitted by the
    client may be repeated back to them.

    ``GET`` returns a list of all items. One argument may be given: ``tag``. For
    example, if ``tag=xyz``, a list of all items who have the tag with "xyz" is
    returned.  ``tag`` may be specified more than once, in order to narrow the
    search. If the tag given does not exist, TODO: clarify this

``item/create-form/``
    ``GET`` returns a form for creating an item.

``item/<id>/update-form/``
    ``GET`` returns a form for updating an item. If item ``id`` does not exist,
    user is redirected to ``item/<id>/``

``tag/``
    ``POST`` creates a new tag. If the request cannot be completed, the user is
    informed of the reason(s). Optionally, the information submitted by the user
    may be repeated back to them.

    ``GET`` returns a list of all tags.

"""
from django.conf.urls import patterns, url

# pylint: disable=C0103
# "Invalid name "urlpatterns" for type constant (should match
# (([A-Z_][A-Z0-9_]*)|(__.*__))$)"
urlpatterns = patterns('elts.views',
    url(r'^$',                         'index'),
    url(r'^calendar/$',                'calendar'),
    url(r'^item/$',                    'item'),
    url(r'^item/create-form/$',        'item_create_form'),
    url(r'^item/(\d+)/$',              'item_id'),
    url(r'^item/(\d+)/update-form/$',  'item_id_update_form'),
    url(r'^tag/$',                     'tag'),
    url(r'^tag/create-form/$',         'tag_create_form'),
    url(r'^tag/(\d+)/$',               'tag_id'),
    url(r'^tag/(\d+)/update-form/$',   'tag_id_update_form'),
)
