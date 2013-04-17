"""URLs for the ELTS application.

The following is a summary of available URLs and the operations that can be
performed on them.

URL "nouns"
===========

/
    The default index page. It includes a "dashboard" of immediately relevant
    information, such as which items are going out and due in today.

/calendar
    A calendar displaying all reservations and lends.

/item
    A list of all items.

/reservation
    A list of all item reservations.

/lend
    A list of all item lends.

/tag
    A list of all item tags. (A tag may be attached to zero or more items.)

=====================  ======  ====  ======  ======
URL                    POST    GET   PUT     DELETE
                       create  read  update  delete
=====================  ======  ====  ======  ======
/                              *
/calendar                      *
/item                  *       *
/item/<number>                 *     *       *
/reservation           *       *
/reservation/<number>          *     *       *
/lend                          *
/lend/<number>                 *
/tag                   *       *
/tag/<number>                  *     *       *
=====================  ======  ====  ======  ======

URL "verbs"
===========

/item?tag=xyz
    TODO

/item/<number>?mode=edit
    TODO

/reservation/<number>?mode=edit
    TODO

===============================  ======  ====  ======  ======
URL                              POST    GET   PUT     DELETE
                                 create  read  update  delete
===============================  ======  ====  ======  ======
/item?tag=xyz                            *
/item/<number>?mode=edit                 *
/reservation/<number>?mode=edit          *
===============================  ======  ====  ======  ======

"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'elts.views.index'),
)
