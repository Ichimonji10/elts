"""URLs and URL operations provided by the ELTS app.

The following documents what URLs are available for use, what messages can be
sent to each, and what type of information is returned from each.

URL "nouns"
===========

====================== ======== ====== ======== ========
URL                    POST     GET    PUT      DELETE
                       (create) (read) (update) (delete)
====================== ======== ====== ======== ========
\/                              *
/calendar/                      *
/item/                 *        *
/item/<number>/                 *      *        *
/reservation/          *        *
/reservation/<number>/          *      *        *
/lend/                          *
/lend/<number>/                 *
/tag/                  *        *
/tag/<number>                   *      *        *
====================== ======== ====== ======== ========

GET /
    Returns the default home page. This page is a summarizes information such as
    which items are going out and due in on that day.

GET /calendar
    Returns a calendar displaying all reservations and lends within a certain
    time period, such as the current week or month.

POST /item
    TODO

GET /item
    Returns a list of all items. (FIXME: might this be paginated?)

GET /item/<number>
    TODO

PUT /item/<number>
    TODO

DELETE /item/<number>
    TODO

POST /reservation
    TODO

GET /reservation
    Returns a list of all item reservations.

GET /reservation/<number>
    TODO

PUT /reservation/<number>
    TODO

DELETE /reservation/<number>
    TODO

GET /lend
    Returns a list of all items currently being lent out. (FIXME: might this
    also show past lends, with pagination?)

GET /lend/<number>
    TODO

POST /tag
    TODO

GET /tag
    Returns a list of all item tags, even including tags that aren't attached to
    any items.

GET /tag/<number>
    TODO

PUT /tag/<number>
    TODO

DELETE /tag/<number>
    TODO

URL "verbs"
===========

===============================  ========  ======  ========  ========
URL                              POST      GET     PUT       DELETE
                                 (create)  (read)  (update)  (delete)
===============================  ========  ======  ========  ========
/item?tag=xyz                              *
/item/<number>?mode=edit                   *
/reservation/<number>?mode=edit            *
===============================  ========  ======  ========  ========

GET /item?tag=xyz
    Returns all items that have are tagged as "xyz".

GET /item/<number>?mode=edit
    Returns detailed information about a single item, and makes all fields
    editable.

GET /reservation/<number>?mode=edit
    Returns detailed information about a single reservation, and makes all
    fields editable.

"""
from django.conf.urls import patterns, url

# pylint: disable=C0103
# "Invalid name "urlpatterns" for type constant (should match
# (([A-Z_][A-Z0-9_]*)|(__.*__))$)"
urlpatterns = patterns('elts.views',
    url(r'^$',              'index'),
    url(r'^calendar/$',     'calendar'),
    url(r'^item/$',         'item'),
    url(r'^reservation/$',  'reservation'),
    url(r'^lend/$',         'lend'),
    url(r'^tag/$',          'tag'),
)
