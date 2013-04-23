"""URLs and URL operations provided by the ELTS app.

The following documents what URLs are available for use, what types of requests
can be sent to each, and what type of information is returned from each.

URL "nouns"
===========

================================ ======== ====== ======== ========
URI                              POST     GET    PUT      DELETE
                                 (create) (read) (update) (delete)
================================ ======== ====== ======== ========
`/`                                       *
`/calendar/`                              *
`/item/`                         *        *
`/item/create-form/`                      *
`/item/<id>/`                             *      *        *
`/item/<id>/update-form/`                 *
`/reservation/`                  *        *
`/reservation/create-form/`               *
`/reservation/<id>/`                      *      *        *
`/reservation/<id>/update-form/`          *
`/lend/`                                  *
`/lend/<id>/`                             *
`/tag/`                          *        *
`/tag/create-form/`                       *
`/tag/<id>/`                              *      *        *
`/tag/<id>/update-form/`                  *
================================ ======== ====== ======== ========

`/`
    `GET` returns the default home page. This page summarizes information such
    as which items are due out and in on that day.

`/calendar/`
    `GET` returns a calendar displaying all reservations and lends within a
    certain time period, such as the current week or month.

`/item/`
    `POST` creates a new item.

    `GET` returns a list of all items.

`/item/create-form/`
    `GET` returns a form for creating a new item.

`/item/<id>/`
    `<id>` is an integer number which identifies a specific item.

    `GET` returns information about item `<id>`.

    `PUT` updates information about item `<id>`.

    `DELETE` deletes item `<id>`.

`/item/<id>/update-form/`
    `GET` returns a form for updating item `<id>`.

`/reservation/`
    `POST` creates a new reservation.

    `GET` returns a list of all reservations.

`/reservation/create-form/`
    `GET` returns a form for creating a new reservation.

`/reservation/<id>/`
    `<id>` is an integer number which identifies a specific reservation.

    `GET` returns information about reservation `<id>`.

    `PUT` updates information about reservation `<id>`.

    `DELETE` deletes reservation `<id>`.

`/reservation/<id>/update-form/`
    `GET` returns a form for updating reservation `<id>`.

`/lend/`
    `GET` returns a list of all lends.

`/lend/<id>/`
    `<id>` is an integer number which identifies a specific lend.

    `GET` returns information about lend `<id>`.

`/tag/`
    `POST` creates a new tag.

    `GET` returns a list of all tags.

`/tag/create-form/`
    `GET` returns a form for creating a new tag.

`/tag/<id>/`
    `<id>` is an integer number which identifies a specific tag.

    `GET` returns information about tag `<id>`.

    `PUT` updates information about tag `<id>`.

    `DELETE` deletes tag `<id>`.

`/tag/<id>/update-form/`
    `GET` returns a form for updating tag `<id>`.

URL "verbs"
===========

===============================  ========  ======  ========  ========
URL                              POST      GET     PUT       DELETE
                                 (create)  (read)  (update)  (delete)
===============================  ========  ======  ========  ========
/item?tag=xyz                              *
===============================  ========  ======  ========  ========

GET /item?tag=xyz
    Returns all items that have are tagged as "xyz".

"""
from django.conf.urls import patterns, url

# pylint: disable=C0103
# "Invalid name "urlpatterns" for type constant (should match
# (([A-Z_][A-Z0-9_]*)|(__.*__))$)"
urlpatterns = patterns('elts.views',
    url(r'^$',              'index'),
    url(r'^calendar/$',     'calendar'),
    url(r'^item/$',         'item'),
    url(r'^item/create-form/$', 'item_create_form'),
    url(r'^reservation/$',  'reservation'),
    url(r'^lend/$',         'lend'),
    url(r'^tag/$',          'tag'),
)
