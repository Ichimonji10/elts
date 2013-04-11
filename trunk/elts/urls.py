"""URLs for the ELTS application.

The following is a summary of available URLs and the operations that can be
performed on them.

                                  POST    GET   PUT     DELETE
                                  create  read  update  delete
/                                         *
/calendar                                 *
/items                            *       *
/items/<number>                           *     *       *
/items/<number>/edit_form                 *
/reservations                     *       *
/reservations/<number>                    *     *       *
/reservations/<number>/edit_form          *
/lends                                    *
/lends/<number>                           *
/tags                             *       *
/tags/<number>                            *     *       *

A general description of the URLs used in this app follows.

/
    The default index page. At the very least, it should show which items are
    going out and due back in today.

/calendar
    A calendar displaying all reservations and lends.

/items
    A list of all items. It is possible to search for specific items from this
    URL. For example, `/item?tag=laptop` would display items with the tag
    "laptop".

/reservations
    A list of all item reservations.

/lends
    A list of all item lends.

/tags
    A list of all item tags. (A tag may be attached to zero or more items.)

"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'elts.views.index'),
)
